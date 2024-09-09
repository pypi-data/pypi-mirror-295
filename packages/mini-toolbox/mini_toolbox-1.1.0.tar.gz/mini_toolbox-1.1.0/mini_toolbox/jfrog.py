#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 用于操作JFrog仓库

__all__ = ['JFrog']

import os
from pyartifactory import Artifactory
from typing import Any, Tuple
from .logger import logger


class JFrog():
    """ 用于操作JFrog仓库
    
    Args:
        user (str): 用户名
        token (str): 用户token
    
    Note:
        实例方法入参说明: ``path`` 指任意路径; ``file`` 指文件路径; ``dir`` 指目录路径
    """

    def __init__(self, user: str, token: str, server: str):
        self.jfrog = Artifactory(url=server, auth=[user, token])

    def _url_join(self, path: str, *args, sep: str = '/') -> str:
        """ 仅内部调用, 用于拼接制品库url """

        for rel in args:
            path = path.strip(sep) + sep + rel.strip(sep)
        return path.strip(sep)

    def upload(self, src_path: str, dst_path: str) -> Any:
        """ 上传路径, 支持文件和目录
        
        Warning:
            覆盖模式, 请谨慎操作!
            src_path 和 dst_path路径类型需要一致, 即: 同为文件类型或同为目录类型
        """
        # 官方工具上传路径错乱, 重写目录递归上传方法
        if os.path.isdir(src_path):
            for root, _, files in os.walk(src_path):
                rel_root = root[len(src_path):].replace(os.path.sep, '/')  # 相对路径
                for file in files:
                    self.upload(os.path.join(root, file), self._url_join(dst_path, rel_root, file))
        else:
            logger.info('Upload: {} -> {}'.format(src_path, dst_path))
            self.jfrog.artifacts.deploy(src_path, dst_path)
        return self.info(dst_path)

    def download(self, src_path: str, dst_dir: str) -> Any:
        """ 下载路径, 支持文件和目录 """

        return self.jfrog.artifacts.download(src_path, dst_dir)

    def copy(self, src_path: str, dst_path: str) -> Any:
        """ 拷贝路径, 支持文件和目录 """

        return self.jfrog.artifacts.copy(src_path, dst_path)

    def move(self, src_path: str, dst_path: str) -> Any:
        """ 移动路径, 支持文件和目录 """

        return self.jfrog.artifacts.move(src_path, dst_path)

    def delete(self, path: str) -> Any:
        """ 删除路径, 支持文件和目录
        
        Warning:
            请谨慎操作!
        """

        return self.jfrog.artifacts.delete(path)

    def info(self, path: str) -> Any:
        """ 查看远程路径信息 """

        return self.jfrog.artifacts.info(path)

    def stat(self, path: str) -> Any:
        """ 查看远程路径状态 """

        return self.jfrog.artifacts.stats(path)

    def list(self, path: str, list_folders: bool = True, recursive: bool = True) -> Any:
        """ 递归显示全部的路径 """

        return self.jfrog.artifacts.list(path, list_folders=list_folders, recursive=recursive)

    def check(self, path: str) -> Tuple:
        """ 查看远程路径是否存在
        
        Args: 
            path (str): 远程路径
        
        Returns: 
            Tuple[bool, Any]: 路径存在, 返回(True, stat信息); 不存在返回(False, 错误信息)
        """

        try:
            return True, self.stat(path)
        except Exception as err:
            return False, err
