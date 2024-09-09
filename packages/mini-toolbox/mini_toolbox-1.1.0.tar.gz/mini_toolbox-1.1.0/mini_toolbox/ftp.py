#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 用于FTP相关操作 """

__all__ = ['FtpTools']

import os
from ftplib import FTP
from typing import Optional
from .logger import logger
from .path import mkdirs, gen_path, split_path


class FtpTools():
    """ 用于FTP相关操作
    
    支持文件/目录的上传和下载, 由于存在安全风险, 不支持删除, 仅支持重写
    
        
    Example:
        FTP download / upload 语法示例::
        
            copy /haha/hehe  .        # hehe   拷贝为 ./hehe       # 后为. 则后补/
            copy /haha/hehe  ./       # hehe   拷贝为 ./hehe
            copy /haha/hehe  ./haha   # hehe   拷贝为 ./haha
            copy /haha/hehe  ./haha/  # hehe   拷贝为 ./haha/hehe
            copy /haha/hehe/ ./       # hehe/* 拷贝为 ./*
            copy /haha/hehe/ ./haha   # hehe/* 拷贝为 ./haha/*     # 前有/ 则后补/
            copy /haha/hehe/ ./haha/  # hehe/* 拷贝为 ./haha/*
    
    Args: 
        host (str): 服务器地址
        port (int): 服务器端口
        user (str): 用户名
        passwd (str): 用户密码
        level (int): 日志等级, ``0/1/2`` 分别表示 ``隐藏/少量/大量``, 默认为0
    """

    def __init__(self, host: str, port: int = 0, user: str = '', passwd: str = '', level: int = 0):

        self.ftp = FTP()
        self.ftp.encoding = 'utf-8'
        self.ftp.set_debuglevel(level)
        self.ftp.connect(host, port, timeout=10)  # 登陆超时时间10s
        self.ftp.login(user, passwd)
        self.ftp.getwelcome()

    def _is_remote_file(self, path: str) -> Optional[bool]:
        """ 判断ftp路径是否为文件, 返回 ``None/True/False`` """

        pwd = self.ftp.pwd()
        is_file = None  # 默认路径不存在
        td, tf = split_path(path)

        try:
            self.ftp.cwd(path)  # 能直接进入则是目录
            is_file = False
        except:
            try:
                self.ftp.cwd(td)  # 能进入上级目录, 且目录中存在, 则是文件
                if tf in self.ftp.nlst():
                    is_file = True
            except:
                pass
        self.ftp.cwd(pwd)

        return is_file

    def _upload_dirs(self, remote_dir: str, log: bool = True) -> None:
        """ 仅内部调用, 处理目录上传, 入参为目录 """

        if log:
            logger.debug('目录上传中: {}'.format(remote_dir))

        pwd = self.ftp.pwd()
        for dir in remote_dir.split('/'):
            if len(dir.strip('.')) == 0:
                continue
            if dir not in self.ftp.nlst():
                self.ftp.mkd(dir)
            self.ftp.cwd(dir)
        self.ftp.cwd(pwd)

    def _upload_file(self, src_path: str, dst_path: str, overwrite: bool = True) -> None:
        """ 仅内部调用, 处理单个文件上传 """

        if self._is_remote_file(dst_path) is None or overwrite:
            try:
                with open(src_path, "rb") as fp:
                    logger.debug('文件上传中: {}'.format(src_path))
                    self.ftp.storbinary("STOR {}".format(dst_path), fp)
            except Exception as err:
                logger.error('文件上传失败: {}'.format(src_path))
                raise Exception(err)
        else:
            logger.debug('文件已存在, 跳过: {}'.format(src_path))

    def upload(self, src_path: str, dst_path: str, overwrite: bool = True) -> None:
        """ 从本地路径上传至服务器路径
        
        Args: 
            src_path (str): 源路径
            dst_path (str): 目标路径
            overwrite (bool): 如果相对路径存在 ``同名同类型`` 文件, 则重写, 默认为True
        """

        # 判断源路径是否存在
        if not os.path.exists(src_path):
            logger.error('源路径不存在: {}'.format(src_path))
            return

        # 首次遍历时, 使用src_file, 如果src_file为空, 则遍历src_dir中所有
        src_dir, src_file = split_path(src_path)

        # 如果src是目录, 则dst也是目录
        dst_path = dst_path + '/' if not src_file else dst_path

        # 根据dst_file判断是否需要改名
        dst_dir, dst_file = split_path(dst_path)

        # 切换路径
        os.chdir(src_dir)
        self._upload_dirs(dst_dir)
        self.ftp.cwd(dst_dir)

        logger.debug([src_dir, src_file, dst_dir, dst_file])

        # 处理 src_file 和 dst_file 都存在的情况, 需要重命名
        if src_file and dst_file:
            if not os.path.isdir(src_file):  # 是文件
                logger.debug('文件重命名上传中: {} -> {}'.format(src_file, dst_file))
                self._upload_file(src_file, dst_file, overwrite=overwrite)
                return
            else:
                # 创建重命名的远程文件夹, 并切换相对路径
                os.chdir(src_file)
                logger.debug('目录重命名上传中: {} -> {}'.format(src_file, dst_file))
                self._upload_dirs(dst_file, log=False)
                self.ftp.cwd(dst_file)
                src_file = '.'

        # 遍历后上传
        for item in gen_path(src_file):
            if not os.path.isdir(item):
                td, tp = split_path(item)

                self._upload_dirs(td)
                self._upload_file(item, item, overwrite=overwrite)
            else:
                self._upload_dirs(item)

    def download(self, src_path: str, dst_path: str, overwrite: bool = True) -> None:
        """ 从服务器路径下载至本地路径
        
        Args: 
            src_path (str): 源路径
            dst_path (str): 目标路径
            overwrite (bool): 如果相对路径存在 ``同名同类型`` 文件, 则重写, 默认为True
        """

        # 判断源路径是否存在
        if self._is_remote_file(src_path) is None:
            logger.error('源路径不存在: {}'.format(src_path))
            return

        # 首次遍历时, 使用src_file, 如果src_file为空, 则遍历src_dir中所有
        src_dir, src_file = split_path(src_path)

        # 如果src是目录, 则dst也是目录
        dst_path = dst_path + '/' if not src_file else dst_path

        # 根据dst_file判断是否需要改名
        dst_dir, dst_file = split_path(dst_path)

        # 创建路径
        mkdirs(dst_dir, is_file=False)

        # 切换路径
        self.ftp.cwd(src_dir)
        os.chdir(dst_dir)

        # 下载文件
        for item in self.ftp.nlst(src_file):
            # 备份当前所在路径
            src_pwd, dst_pwd = self.ftp.pwd(), os.getcwd()

            # 正在处理的相对路径
            std, stf = split_path(item)
            dtd = dst_file if dst_file and std else std
            dtf = dst_file if dst_file and not std else stf

            # 正在处理的绝对路径
            now_src = '/'.join((src_pwd, std, stf))
            now_dst = '/'.join((dst_pwd, dtd, dtf))

            # 如果item为多级路径, 则先新建目录dirname(item)
            if std:
                self.ftp.cwd(std)
                mkdirs(dtd, is_file=False)
                os.chdir(dtd)

            # 处理item路径, 如果是文件则下载, 如果是目录, 则递归download()
            if self._is_remote_file(stf):
                # 路径不存在, 或者需要重写
                if not os.path.exists(dtf) or overwrite:
                    try:
                        with open(dtf, "wb") as fp:
                            logger.debug('文件下载中: {}'.format(now_src))
                            self.ftp.retrbinary("RETR {}".format(stf), fp.write)
                    except Exception as err:
                        logger.error('文件下载失败: {}'.format(now_src))
                        raise Exception(err)
                else:
                    logger.debug('文件已存在, 跳过: {}'.format(now_src))
            else:
                logger.debug('目录下载中: {}'.format(now_src))
                mkdirs(dtf, is_file=False)
                self.download(now_src, now_dst, overwrite=overwrite)

            # 回到备份路径
            self.ftp.cwd(src_pwd)
            os.chdir(dst_pwd)

    def check_file(self, path: str) -> Optional[bool]:
        """ 判断ftp路径是否为文件, 返回 ``None/True/False``, None表示不存在 """

        return self._is_remote_file(path)
