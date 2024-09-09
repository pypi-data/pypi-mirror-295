#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 实用系统工具 """

__all__ = [
    'get_os', 'time_flag', 'time_delta', 'exec_cmd', 'dict2obj', 'update_obj', 'split_str', 'is_none', 'format_bool',
    'format_none', 'set_or_not', 'get_obj_value', 'judge_errs', 'dict_sort', 'chunk_str', 'comp_ver', 'format_vars'
]

import re
import sys
import json
import time
import operator
import platform
import subprocess
from typing import Any, Tuple, Optional, Union


def get_os() -> str:
    """ 获取操作系统类型
    
    Returns: 
        str: 操作系统类型 ``win|unix``
    """

    if platform.system().find('Windows') != -1:
        return 'win'
    else:
        return 'unix'


def time_flag(time_format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """ 获取当前时间的格式化输出 """

    return time.strftime(time_format, time.localtime())


def time_delta(days: int, time_str: str = '', time_format: str = '%Y-%m-%d') -> str:
    """ 用于简单的日期天数加减, 支持传入指定日期 """

    _time = time.mktime(time.strptime(time_str, time_format)) if time_str else time.time()
    return time.strftime(time_format, time.localtime(_time + 60 * 60 * 24 * days))


def exec_cmd(cmd: Union[str, list],
             shell: bool = True,
             live: bool = False,
             input: Optional[str] = None,
             timeout: Optional[int] = None,
             encoding: Optional[str] = None,
             errors: str = 'strict') -> Tuple[int, str, str]:
    """ 调用系统指令, 返回指令输出, 不建议执行复杂指令

    Args: 
        cmd (Union[str, list]): 待执行指令
        shell (bool): 是否使用系统shell执行, 默认为True, 如果cmd为列表, 需要置为False
        live (bool): 是否实时输出, 默认为False, 如果为True, 则返回值中标准输出和错误输出为None
        input (Optional[str]): 指令执行时交互输入, 如 ``'keyword\\n'``, 不建议使用
        timeout (Optional[int]): 指令执行超时时间, 默认不限制, 建议使用
        encoding (Optional[str]): 输出编码, 默认根据系统判断: win(gbk)/unix(utf-8), 建议默认
        errors (str): 遇到错误时处理模式, 默认为 ``strict``, 可选: ``strict/ignore/replace``
    
    Returns: 
        Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
        
    Raises: 
        TimeoutExpired: 超时情况抛出异常, 中断程序
    """

    encoding = encoding or 'gbk' if get_os() == 'win' else 'utf-8'
    pipe = subprocess.PIPE

    common_args = {'shell': shell, 'encoding': encoding, 'errors': encoding, 'stdin': pipe}

    if live:
        ps = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, **common_args)
    else:
        ps = subprocess.Popen(cmd, stdout=pipe, stderr=pipe, **common_args)

    try:
        stdout, stderr = ps.communicate(input, timeout)
    except subprocess.TimeoutExpired:
        ps.kill()
        raise
    return ps.returncode, (stdout or '').strip(), (stderr or '').strip()


class _Dict2Object():
    """ 仅允许 ``dict2obj`` 方法调用, dict2obj返回对象类型 """

    def __init__(self, data: dict) -> None:
        self._updateobj(data)

    def __str__(self) -> str:
        """ 格式化输出配置对象 """

        _body = ['.{} = {},'.format(k, str(v) if type(v) == type(self) else repr(v)) for k, v in self.__dict__.items()]
        _data = '<_Dict2Object {:#x}\n{}\n>'.format(id(self), '\n'.join(_body)).splitlines()
        _data[1:-1] = ['    {}'.format(x) for x in _data[1:-1]]
        return '\n'.join(_data)

    def _updateobj(self, data: dict) -> None:
        """ 仅允许 ``update_obj`` 方法调用 """

        if type(data) == type(self):
            data = data.__dict__
        self.__dict__.update(data)

    def obj2dict(self) -> dict:
        """ 将配置对象转化为字典 """

        return {k: v.obj2dict() if type(v) == type(self) else v for k, v in self.__dict__.items()}


def dict2obj(data: Union[dict, _Dict2Object]) -> _Dict2Object:
    """ 将字典转化为 ``_Dict2Object`` 数据对象 """

    if isinstance(data, _Dict2Object):
        return data
    elif not isinstance(data, dict):
        data = {}
    return json.loads(json.dumps(data), object_hook=_Dict2Object)


def update_obj(obj: _Dict2Object, data: Union[dict, _Dict2Object]) -> None:
    """ 更新 ``_Dict2Object`` 数据对象 """

    obj._updateobj(dict2obj(data))


def split_str(s: str, sep: str = ',') -> list:
    """ 拆分字符串, 返回原序去重去空列表 """

    tmp = list(filter(None, [x.strip() for x in str(s).split(sep)] if s else []))
    return sorted(set(tmp), key=tmp.index)


def is_none(param: Any) -> bool:
    """ 校验入参是否为空, 空返回True, 非空返回False """

    if not param:
        return True
    if isinstance(param, str):
        if not param.strip():
            return True
    if isinstance(param, list):
        if not list(filter(None, [str(x).strip() for x in param])):
            return True
    return False


def format_bool(s: str) -> bool:
    """ 将true/false字符串转化为bool类型 """

    return True if str(s).lower() == 'true' else False


def format_none(v: Any, default: bool = None) -> Any:
    """ 格式化空数据 """

    return v if v else default


def set_or_not(obj: object, key: str, value: Any) -> None:
    """ 如果值不为None, 则更新对象的属性值 """

    if value is not None:
        setattr(obj, key, value)


def get_obj_value(obj: object, path: str, default: Any = None) -> Any:
    """ 获取对象path的值, 如果不存在, 返回默认值 """

    try:
        for key in path.split('.'):
            obj = getattr(obj, key)
        return obj
    except:
        return default


def judge_errs(*args) -> list:
    """ 用于条件判断, 返回msg列表: ``(condition, msg, Optional(break(bool)),`` """

    errs = []
    for item in args:
        if item[0]:
            errs.append(item[1])
            if item[-1] == True:
                break
    return errs


def dict_sort(data: dict, reverse: bool = False) -> dict:
    """ 返回按键值排序的字典 """

    return {k: v for k, v in sorted(data.items(), key=lambda d: d[0], reverse=reverse)}


def chunk_str(src: str, size: int, sep: str = ',') -> list:
    """ 按指定大小拆分指定分隔符的字符串

    Args: 
        src (str): 待拆分的字符串
        size (int): 子字符串大小
        sep (str): 分隔符, 默认 ``,``
        
    Returns: 
        list: 返回拆分后的字符串列表
    """

    src, dst = split_str(src, sep=sep), []
    for item in [src[x:x + size] for x in range(0, len(src), size)]:
        dst.append(sep.join([str(x) for x in item]))
    return dst


def comp_ver(ver_a: str, ver_b: str, flag: str = '<') -> bool:
    """ 用于比较标准数字版本号, 版本号可以以 ``Vv`` 开头, ``.`` 分隔, 不支持存在其它字母 """

    ver_a = [int(x) for x in filter(None, ver_a.strip().lstrip('Vv').split('.'))]
    ver_b = [int(x) for x in filter(None, ver_b.strip().lstrip('Vv').split('.'))]
    flag_map = {'<': 'lt', '>': 'gt', '<=': 'le', '>=': 'ge', '!=': 'ne', '==': 'eq'}
    return getattr(operator, flag_map[flag])(ver_a, ver_b)


def format_vars(data: str, var_dict: dict) -> str:
    """ 用于格式化str模版, 替换{{VARIABLE}} """

    dst = []
    for token in re.split(r'({{.*?}})', data):
        _tmp, _key = token, token[2:-2]
        if token.startswith('{{'):
            _tmp = str(var_dict[_key]) if _key in var_dict else ''
        dst.append(_tmp)
    return ''.join(dst)
