#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 用于ssh/sftp相关操作 """

__all__ = ['SshTools']

import warnings

warnings.filterwarnings(action='ignore', message='Python .* is no longer supported by the Python core team')

import os
import sys
import paramiko
from typing import Any, Tuple, Optional
from .logger import logger
from .path import split_path


class SshTools():
    """ 用于ssh/sftp相关操作, 支持密码和密钥登陆
    
    Note:
        官方文档: `ssh`_, `sftp`_
    
    Args: 
        host (str): 服务器地址
        port (int): 端口地址
        user (Optional[str]): 用户名, 默认为当前用户名
        passwd (Optional[str]): 密码, 优先级低于pkey_file
        pkey_file (Optional[str]): 指定私钥路径, 默认为.ssh/id_rsa
    
    .. _ssh:
        https://docs.paramiko.org/en/2.12/api/client.html
    
    .. _sftp:
        https://docs.paramiko.org/en/2.12/api/sftp.html
    """

    def __init__(self,
                 host: str,
                 port: int = 22,
                 user: Optional[str] = None,
                 passwd: Optional[str] = None,
                 pkey_file: Optional[str] = None):

        self.ssh = paramiko.SSHClient()
        # 允许连接不在~/.ssh/known_hosts文件中的主机
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.ssh.connect(host, port, username=user, password=passwd, key_filename=pkey_file, timeout=10)
        self.sftp = self.ssh.open_sftp()

    def _gen_dst_path(self, path: str, is_local: bool = True) -> None:
        """ 仅内部调用, 创建目标文件夹 """

        dir, file = split_path(path)

        if is_local:
            os.makedirs(dir, exist_ok=True)
        else:
            self.exec("mkdir -p {}".format(dir))

    def exec(self,
             cmd: str,
             input: Optional[str] = None,
             live=False,
             encoding='utf-8',
             errors: str = 'replace') -> Tuple[int, str, str]:
        """ 执行shell指令, 不建议执行复杂指令

        Args: 
            cmd(str): 待执行指令, 多条命令用 ``';'`` 分隔
            input(Optional[str]): 指令执行时交互输入, 如 ``'keyword\\n'``, 不建议使用
            live (bool): 是否实时输出, 默认为False, 如果为True, 则返回值中标准输出和错误输出为None
            encoding(str): 目标服务器输出的编码格式, 默认为 ``'utf-8'``
            errors (str): 遇到错误时处理模式, 默认为 ``replace``, 可选: ``strict/ignore/replace``
            
        Returns:
            Tuple[int, str, str]: 执行结果(状态码, 标准输出, 错误输出)
        """

        stdin, stdout, stderr = self.ssh.exec_command(cmd, get_pty=live)

        if input:
            stdin.write(input)
            stdin.flush()

        stcode = stdout.channel.recv_exit_status()
        if live:
            while True:
                v = stdout.channel.recv(1024)
                if not v:
                    break
                sys.stdout.write(v.decode(encoding, errors=errors))
                sys.stdout.flush()
            stdout, stderr = None, None
        else:
            stdout = stdout.read().decode(encoding, errors=errors).strip()
            stderr = stderr.read().decode(encoding, errors=errors).strip()

            if stderr:
                if stcode == 0:
                    logger.warn(stderr)
                else:
                    logger.error(stderr)

        return stcode, stdout, stderr

    def upload(self, src_file: str, dst_file: str) -> Any:
        """ 上传文件, 仅支持文件路径 """

        self._gen_dst_path(dst_file, is_local=False)
        return self.sftp.put(src_file, dst_file)

    def download(self, src_file: str, dst_file: str) -> Any:
        """ 下载文件, 仅支持文件路径 """

        self._gen_dst_path(dst_file, is_local=True)
        return self.sftp.get(src_file, dst_file)
