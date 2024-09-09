#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 提供基本hash工具: md5/sha1/sha256 """

__all__ = ['md5', 'sha1', 'sha256']

import os
import hashlib
from typing import Any, Optional


def _hash(file_path: str, myhash: Any) -> Optional[str]:
    """ 仅内部调用, 根据指定hash工具, 返回对应的hash值"""

    if not os.path.isfile(file_path):
        return
    with open(file_path, 'rb') as fp:
        while True:
            b = fp.read(8096)
            if not b:
                break
            myhash.update(b)
    return myhash.hexdigest()


def md5(file_path: str) -> Optional[str]:
    """ 计算文件的md5: 合法文件, 返回指定文件md5值; 非法文件, 返回 ``None`` """

    return _hash(file_path, hashlib.md5())


def sha1(file_path: str) -> Optional[str]:
    """ 计算文件的sha1: 合法文件, 返回指定文件sha1值; 非法文件, 返回 ``None`` """

    return _hash(file_path, hashlib.sha1())


def sha256(file_path: str) -> Optional[str]:
    """ 计算文件的sha256: 合法文件, 返回指定文件sha256值; 非法文件, 返回 ``None`` """

    return _hash(file_path, hashlib.sha256())
