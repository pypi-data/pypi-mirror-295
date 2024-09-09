#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" SVN常用指令封装

Warning:
    出于安全考虑, 不支持密码输入

Note:
    官方文档: `svn官方文档`_, `svn-book英文版`_, `svn-book中文版`_
    
.. _svn官方文档:
    https://svnbook.red-bean.com/

.. _svn-book英文版:
    https://svnbook.red-bean.com/en/1.7/svn-book.html

.. _svn-book中文版:
    https://svnbook.red-bean.com/nightly/zh/svn-book.html
"""

__all__ = [
    'svn_checkout', 'svn_export', 'svn_commit', 'svn_update', 'svn_clean', 'svn_copy', 'svn_delete', 'svn_list',
    'svn_info', 'svn_info_dict', 'svn_log', 'svn_log_list'
]

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any, Tuple, Optional, Union
from .logger import logger
from .utils import exec_cmd


def _utc2local(date: str, time_format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """ 仅内部调用, 将svn --xml中时间戳时区转为本地时区 """

    _date = datetime.strptime(date.replace("Z", "+0000"), '%Y-%m-%dT%H:%M:%S.%f%z')
    return _date.astimezone().strftime(time_format)


def svn_checkout(svn_url: str,
                 dst_dir: str,
                 rev: Union[int, str, None] = None,
                 params: Optional[str] = None,
                 live: bool = False) -> Tuple[int, str, str]:
    """ 检出代码
    
    Args: 
        svn_url (str): svn_url路径
        dst_path (str): 本地目的路径
        rev (Union[int, str, None]): 指定配置库提交版本, 默认为最新版本
        params (Optional[str]): 指定额外参数, 默认为空
        live (bool): 是否实时输出, 默认为False, 如果为True, 则返回值中标准输出和错误输出为空
    
    Returns: 
        Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
    """

    rev = '' if not rev else '-r {}'.format(rev)
    params = '' if not params else params
    cmd = 'svn co {} {} {} {}'.format(svn_url, dst_dir, rev, params)
    return exec_cmd(cmd, live=live)


def svn_export(svn_url: str,
               dst_dir: str,
               rev: Union[int, str, None] = None,
               params: Optional[str] = None,
               live: bool = False) -> Tuple[int, str, str]:
    """ 检出纯净代码副本, 不带.svn
    
    Args: 
        svn_url (str): svn_url路径
        dst_path (str): 本地目的路径
        rev (Union[int, str, None]): 指定配置库提交版本, 默认为最新版本
        params (Optional[str]): 指定额外参数, 默认为空
        live (bool): 是否实时输出, 默认为False, 如果为True, 则返回值中标准输出和错误输出为空
    
    Returns: 
        Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
    """

    rev = '' if not rev else '-r {}'.format(rev)
    params = '' if not params else params
    cmd = 'svn export {} {} {} {}'.format(svn_url, dst_dir, rev, params)
    return exec_cmd(cmd, live=live)


def svn_commit(local_path: str, msg: str, live: bool = False) -> Tuple[int, str, str]:
    """ 提交代码

    Args: 
        local_path (str): 仅支持svn本地路径
        msg (str): 提交日志信息, 必填
        live (bool): 是否实时输出, 默认为False, 如果为True, 则返回值中标准输出和错误输出为空
    
    Returns: 
        Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
    """
    local_path = '.' if not local_path else local_path
    msg = '' if not msg else '-m "{}"'.format(msg)

    stcode, stdout, stderr = exec_cmd('svn st {}'.format(local_path))
    if stcode != 0 or not stdout or stderr:
        return stcode, stdout, stderr

    for line in stdout.split('\n'):
        # 每行前7列包含描述项目状态的字符, 第8列总是一个空格.
        if line[0] == '?':  # 未跟踪文件
            exec_cmd('svn add {}'.format(line[8:]), live=live)
        elif line[0] == '!':  # 被删除文件
            exec_cmd('svn delete {}'.format(line[8:]), live=live)
    return exec_cmd('svn commit {} {}'.format(local_path, msg), live=live)


def svn_update(local_path: Optional[str] = None,
               rev: Union[int, str, None] = None,
               live: bool = False) -> Tuple[int, str, str]:
    """ 用于更新工作目录, 返回执行结果, 可以指定配置库提交版本
    
    Args: 
        local_path (Optional[str]): 仅支持svn本地路径, 默认为当前路径
        rev (Union[int, str, None]): 指定配置库提交版本, 默认为最新版本
        live (bool): 是否实时输出, 默认为False, 如果为True, 则返回值中标准输出和错误输出为空
    
    Returns: 
        Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
    """

    local_path = '.' if not local_path else local_path
    rev = '' if not rev else '-r {}'.format(rev)
    cmd = 'svn update {} {}'.format(local_path, rev)
    return exec_cmd(cmd, live=live)


def svn_clean(local_path: Optional[str] = None, live: bool = False) -> Tuple[int, str, str]:
    """ 用于清理工作目录, 返回执行结果 
    
    Args: 
        local_path (Optional[str]): 仅支持svn本地路径, 默认为当前路径
        live (bool): 是否实时输出, 默认为False, 如果为True, 则返回值中标准输出和错误输出为空
    
    Returns: 
        Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
    """

    local_path = '.' if not local_path else local_path
    cmd = 'svn cleanup {}'.format(local_path)
    return exec_cmd(cmd, live=live)


def svn_copy(src_path: str,
             dst_path: str,
             msg: str,
             rev: Union[int, str, None] = None,
             live: bool = False) -> Tuple[int, str, str]:
    """ 复制svn路径, 返回指令执行信息

    Args: 
        src_path (str): svn路径, 支持本地路径和url
        dst_path (str): svn路径, 支持本地路径和url
        msg (str): 日志信息, url路径时必填, 默认为空
        rev (Union[int, str, None]): 指定配置库提交版本, 默认为最新版本
        live (bool): 是否实时输出, 默认为False, 如果为True, 则返回值中标准输出和错误输出为空
        
    Returns: 
        Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
    """

    msg = '' if not msg else '-m "{}"'.format(msg)
    rev = '' if not rev else '-r {}'.format(rev)
    cmd = 'svn copy {} {} {} {} --parents'.format(src_path, dst_path, msg, rev)
    return exec_cmd(cmd, live=live)


def svn_delete(svn_path: str,
               msg: Optional[str] = None,
               force: bool = True,
               live: bool = False) -> Tuple[int, str, str]:
    """ 删除svn路径, 返回delete指令执行信息

    Args: 
        svn_path (str): svn路径, 支持本地路径和url
        msg (Optional[str]): 日志信息, url路径时必填, 默认为空
        force (bool): 本地存在修改时是否删除, 默认为True
        live (bool): 是否实时输出, 默认为False, 如果为True, 则返回值中标准输出和错误输出为空
        
    Returns: 
        Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
    """

    msg = '' if not msg else '-m "{}"'.format(msg)
    force = '' if not force else '--force'
    cmd = 'svn del {} {} {}'.format(svn_path, msg, force)
    logger.debug('CMD: {}'.format(cmd))
    return exec_cmd(cmd, live=live)


def svn_list(svn_path: str,
             params: str = '-vR',
             rev: Union[int, str, None] = None,
             live: bool = False) -> Tuple[int, str, str]:
    """ 返回list指令执行信息

    Args: 
        svn_path: (str) svn路径, 支持本地路径和url
        params: (str) 指定额外参数, 默认为空
        rev: (Union[int, str, None]) 指定配置库提交版本, 默认为最新版本
        live (bool): 是否实时输出, 默认为False, 如果为True, 则返回值中标准输出和错误输出为空
        
    Returns: 
        Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
    """

    rev = '' if not rev else '-r {}'.format(rev)
    cmd = 'svn list {} {} {}'.format(params, svn_path, rev)
    return exec_cmd(cmd, live=live)


def svn_info(svn_path: str,
             rev: Union[int, str, None] = None,
             params: Optional[str] = None,
             live: bool = False) -> Tuple[int, str, str]:
    """ 返回info指令执行信息

    Args: 
        svn_path: (str) svn路径, 支持本地路径和url
        rev: (Union[int, str, None]) 指定配置库提交版本, 默认为最新版本
        params: (Optional[str]) 指定额外参数, 默认为空
        live (bool): 是否实时输出, 默认为False, 如果为True, 则返回值中标准输出和错误输出为空
        
    Returns: 
        Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
    """

    rev = '' if not rev else '-r {}'.format(rev)
    params = '' if not params else params
    cmd = 'svn info {} {} {}'.format(svn_path, rev, params)
    return exec_cmd(cmd, live=live)


def svn_info_dict(svn_path: str, rev: Union[int, str, None] = None) -> Any:
    """ 返回字典化的info信息

    Args: 
        svn_path: (str) svn路径, 支持本地路径和url
        rev: (Union[int, str, None]) 指定配置库提交版本, 默认为最新版本
    
    Returns: 
        dict: 返回常用键值对, 包括: ``path/rev/kind/url/root/last_rev/last_author/last_date``
    
    Raises: 
        Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
    """

    rev = '' if not rev else '-r {}'.format(rev)
    cmd = 'svn info {} {} {}'.format(svn_path, rev, '--xml')

    stcode, stdout, stderr = exec_cmd(cmd, encoding='utf-8')
    if stcode != 0 or not stdout or stderr:
        return stcode, stdout, stderr

    root = ET.fromstring(stdout)
    dst_dict = {
        'path': root.find('entry').get('path'),
        'rev': root.find('entry').get('revision'),
        'kind': root.find('entry').get('kind'),
        'url': root.find('entry').find('url').text,
        'root': root.find('entry').find('repository').find('root').text,
        'last_rev': root.find('entry').find('commit').get('revision'),
        'last_author': root.find('entry').find('commit').find('author').text,
        'last_date': _utc2local(root.find('entry').find('commit').find('date').text),
    }
    return dst_dict


def svn_log(svn_path: str,
            num: Union[int, str, None] = None,
            rev: Union[int, str, None] = None,
            params: Optional[str] = None,
            live: bool = False) -> Tuple[int, str, str]:
    """ 返回log指令执行信息

    Args: 
        svn_path: (str) svn路径, 支持本地路径和url
        num: (Union[int, str, None]) 指定查询的日志数量, 默认为全部
        rev: (Union[int, str, None]) 指定配置库提交版本, 默认为最新版本
        params: (Optional[str]) 指定额外参数, 默认为空
        live (bool): 是否实时输出, 默认为False, 如果为True, 则返回值中标准输出和错误输出为空
        
    Returns: 
        Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
    """

    num = '' if not num else '-l {}'.format(num)
    rev = '' if not rev else '-r {}'.format(rev)
    params = '' if not params else params
    cmd = 'svn log {} {} {}'.format(svn_path, num, rev, params)
    return exec_cmd(cmd, live=live)


def svn_log_list(svn_path: str, num: Union[int, str, None] = None, rev: Union[int, str, None] = None) -> Any:
    """ 返回列表化的log信息

    Args: 
        svn_path: (str) svn路径, 支持本地路径和url
        num: (Union[int, str, None]) 指定查询的日志数量, 默认为全部
        rev: (Union[int, str, None]) 指定配置库提交版本, 默认为最新版本

    Returns: 
        List[dict]: 返回列表化的常用键值对, 包括: ``rev/author/date/msg``
    
    Raises: 
        Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
    """

    num = '' if not num else '-l {}'.format(num)
    rev = '' if not rev else '-r {}'.format(rev)
    cmd = 'svn log {} {} {} {}'.format(svn_path, num, rev, '--xml')

    stcode, stdout, stderr = exec_cmd(cmd, encoding='utf-8')
    if stcode != 0 or not stdout or stderr:
        return stcode, stdout, stderr

    root = ET.fromstring(stdout)
    dst_list = []
    for item in root.findall('logentry'):
        dst_list.append({
            'rev': item.get('revision'),
            'author': item.find('author').text,
            'date': _utc2local(item.find('date').text),
            'msg': item.find('msg').text,
        })
    return dst_list
