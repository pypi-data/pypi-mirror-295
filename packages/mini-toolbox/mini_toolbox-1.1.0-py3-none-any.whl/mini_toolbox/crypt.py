#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 用于字符串加解密, 支持DES/RSA

__all__ = ['CryptTools']

import os
import rsa
from base64 import b64encode, b64decode
from binascii import a2b_hex, b2a_hex
from pyDes import des, PAD_PKCS5
from typing import Optional


class CryptTools():
    """ 用于字符串加解密, 支持DES/RSA

    Args: 
        key (Optional[str]): 自定义密钥, 用于DES认证
        priv (str): 自定义私钥文件路径, 用于RSA认证, 默认为当前路径下: ``priv.pem``
    """

    def __init__(self, key: Optional[str] = None, priv: str = 'priv.pem'):
        self.k = des(str(key).ljust(8, '%')[:8], padmode=PAD_PKCS5)
        self.priv = priv
        self.encoding = 'utf-8'

    def des_encrypt(self, s: str) -> str:
        """ DES 加密

        Args: 
            s (str): 原始字符串
            
        Returns: 
            str: 加密后字符串
        """

        return b64encode(b2a_hex(self.k.encrypt(s))).decode(self.encoding)

    def des_decrypt(self, s: str) -> str:
        """ DES 解密

        Args: 
            s (str): 加密后字符串
            
        Returns: 
            str: 原始字符串
        """

        return self.k.decrypt(a2b_hex(b64decode(s))).decode(self.encoding)

    def rsa_encrypt(self, s: str) -> str:
        """ RSA 加密, 私钥保存至 ``priv`` 文件

        Args:
            s (str): 原始字符串
        
        Returns:
            str: 加密后字符串
        """

        pub_key, priv_key = rsa.newkeys(512)

        os.makedirs(os.path.dirname(self.priv) or '.', exist_ok=True)
        with open(self.priv, 'wb') as fp:
            fp.write(priv_key.save_pkcs1())

        return b64encode(rsa.encrypt(s.encode(self.encoding), pub_key)).decode(self.encoding)

    def rsa_decrypt(self, s: str) -> str:
        """ RSA 解密, 私钥读取自 ``priv`` 文件

        Args:
            s (str): 加密后字符串
        
        Returns:
            str: 原始字符串
        """

        with open(self.priv, 'rb') as fp:
            priv_data = fp.read()
        priv_key = rsa.PrivateKey.load_pkcs1(priv_data)

        return rsa.decrypt(b64decode(s), priv_key).decode(self.encoding)
