#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 文件、路径处理相关工具 """

__all__ = [
    'pushd', 'get_eol', 'file_time', 'path_type', 'path_join', 'url_join', 'split_path', 'gen_path', 'rm_file',
    'mkdirs', 'copy_file', 'move_file', 'merge_file', 'search_file', 'edit_file'
]

import os
import re
import time
import shutil
import contextlib
from typing import Tuple, Optional


@contextlib.contextmanager
def pushd(new_dir: str) -> None:
    """ 用于pushd指定目录, 通过with语句调用, with结束后隐式popd """

    prev_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(prev_dir)


def get_eol(path: str, encoding: str = 'utf-8') -> str:
    """ 获取文本文件的换行符, 默认为 ``\n`` """

    with open(path, 'r', encoding=encoding, newline='') as fp:
        origin = fp.readline()
    with open(path, 'r', encoding=encoding) as fp:
        trans = fp.readline()
    return origin[len(trans) - 1:] if trans and (origin != trans) else '\n'


def file_time(path: str, time_format: str = '%Y%m%d%H%M%S') -> str:
    """ 获取文件的最后修改时间戳 """

    flag = os.path.getmtime(path) if path_type(path) == 'file' else 0
    return time.strftime(time_format, time.localtime(flag))


def path_type(path: str) -> Optional[str]:
    """ 获取路径类型, 返回: ``'link'/'file'/'dir'/None`` """

    _func = {
        'link': os.path.islink,
        'dir': os.path.isdir,
        'file': os.path.isfile,
    }

    for key, value in _func.items():
        if value(path) == True:
            return key
    return None


def path_join(path: str, *args: str, sep: str = os.path.sep) -> str:
    """ 合并路径, 原版'/'开头路径前面的参数全部丢弃改为不丢弃 """

    _all = [path] + [x for x in args]
    _first, _middle, _last = [], [], []

    if len(_all) <= 1:
        _first = _all
    else:
        _first = [str(_all[0]).rstrip('/' + sep)]
        _last = [str(_all[-1]).lstrip('/' + sep)]

    if len(_all) > 2:
        _middle = [str(x).strip('/' + sep) for x in _all[1:-1]]

    return sep.join(filter(None, _first + _middle + _last))


def url_join(path: str, *args: str) -> str:
    """ 合并url路径"""

    return path_join(path, *args, sep='/')


def split_path(path: str) -> Tuple[str, str]:
    """ 拆分路径, 返回目录和文件名 """

    dir, file = os.path.split(path.strip())
    file = '' if file == '.' else file
    dir = '.' if dir == '' else dir
    return dir, file


def gen_path(path: str, only_file: bool = False, base_dir: str = '.') -> list:
    """ 按序递归生成有序且唯一的子路径列表

    Args: 
        path (str): 待分析的路径
        only_file (bool): 仅返回文件路径, 默认False
        base_dir (str): 基准路径, 优先切换至该路径, 默认 ``.``
        
    Returns: 
        list: 返回全部的子路径列表
    """

    if path.strip() == '':
        path = '.'

    _type = path_type(path)
    if not _type:
        return []
    if _type in ['file', 'link']:
        return [path]

    dst = []
    with pushd(base_dir):
        for root, dirs, files in os.walk(path):
            if not files and not dirs:
                if not only_file:
                    dst.append(root)
            for tf in files:
                dst.append(os.path.join(root, tf))

    return dst


def _onerror(func, path, exc_info):
    """ 仅内部调用, shutil.rmtree 的权限异常处理, 用法: shutil.rmtree(path, onerror=onerror) """

    import stat
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def rm_file(path: str) -> None:
    """ 删除文件路径, 仅支持处理三种文件类型: ``dir/file/link``
    
    Warning:
        递归删除很危险, 请慎重
    """

    file_type = path_type(path)
    if file_type in ['file', 'link']:
        os.remove(path)
    elif file_type in ['dir']:
        shutil.rmtree(path, onerror=_onerror)


def mkdirs(path: str, is_file: bool = False, remake: bool = False) -> str:
    """ 递归创建文件夹, 并返回目录路径
    
    Args: 
        path (str): 路径
        is_file (bool): 是否为文件路径, 默认为False,
        remake (bool): 是否重建目录, 默认False
        
    Returns: 
        str: 目录路径
    """

    dir = os.path.dirname(path.strip()) if is_file else path.strip()
    dir = dir or '.'

    if remake:
        rm_file(dir)

    os.makedirs(dir, exist_ok=True)
    return dir


def copy_file(src: str, dst: str, force: bool = True) -> None:
    """ 拷贝单文件路径, 源目路径类型需要一致, 仅支持处理三种文件类型: ``dir/file/link`` """

    # 如果存在: 强制更新或跳过
    if path_type(dst):
        if force:
            rm_file(dst)
        else:
            return

    # 拷贝文件
    mkdirs(dst, is_file=True)
    src_type = path_type(src)
    if src_type == 'link':
        linkto = os.readlink(src)
        os.symlink(linkto, dst)
    elif src_type == 'file':
        shutil.copy(src, dst)
    elif src_type == 'dir':
        shutil.copytree(src, dst)


def move_file(src: str, dst: str, force: bool = True) -> None:
    """ 移动单文件路径, 源目路径类型需要一致, 仅支持处理三种文件类型: ``dir/file/link`` """

    # 如果存在: 强制更新或跳过
    if path_type(dst):
        if force:
            rm_file(dst)
        else:
            return

    # 移动文件
    shutil.move(src, dst)


def merge_file(src: str, dst: str, force: bool = True):
    """ 合并源目路径, 源目路径类型需要一致, 仅支持处理三种文件类型: ``dir/file/link`` """

    src_type = path_type(src)
    if src_type != 'dir':
        copy_file(src, dst, force=force)
        return

    for item in gen_path('.', only_file=False, base_dir=src):
        _src = path_join(src, item[2:])
        _dst = path_join(dst, item[2:])
        _src_type, _dst_type = path_type(_src), path_type(_dst)
        if _src_type != 'dir':
            copy_file(_src, _dst, force=force)
        elif _dst_type != 'dir':
            mkdirs(_dst, is_file=False)


def search_file(path: str, regex: str) -> list:
    """ 递归搜索路径中正则匹配的文件名并返回搜索结果相对路径列表

    Args: 
        path (str): 待搜索路径
        regex (str): 正则表达式, 通过 ``re.search`` 搜索
        
    Returns: 
        list: 返回搜索结果列表
    """

    dst_list = []
    for tp in gen_path('.', only_file=True, base_dir=path):
        td, tf = split_path(tp)
        if re.search(regex, tf):
            dst_list.append(tp[2:])  # remove prefix ./ or .\
    return dst_list


def edit_file(path: str, sub_info: list, encoding: str = 'utf-8') -> None:
    """ 按规则修改文本行
    
    使用 ``re.serarch`` 搜索行关键字, 使用 ``re.sub`` 替换, \
    sub_info格式: ``[line_keyword, sub_from, sub_to]``
    """

    line_keyword, sub_from, sub_to = sub_info
    dst_data = []

    with open(path, 'r', encoding=encoding) as fp:
        src_data = fp.readlines()

    for item in src_data:
        if re.search(line_keyword, item):
            item = re.sub(sub_from, sub_to, item)
        dst_data.append(item)

    with open(path, 'w', encoding=encoding) as fp:
        for item in dst_data:
            fp.write(item)
