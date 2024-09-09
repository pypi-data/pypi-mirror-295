#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 用于操作mysql数据库

__all__ = ['MySQL']

import warnings

warnings.filterwarnings(action='ignore', message='Python .* is no longer supported by the Python core team')

import pymysql
from pymysql.cursors import DictCursor
from typing import Any, Union


class MySQL():
    """ 用于mysql数据库相关操作
    
    Args: 
        host (str): 服务器地址
        port (int): 服务器端口
        user (str): 用户名
        passwd (str): 用户密码
        database (str): 数据库名
    """

    def __init__(self, host: str, port: int = 3306, user: str = '', passwd: str = '', database: str = '') -> None:
        self.connDB = pymysql.connect(host=host,
                                      port=port,
                                      user=user,
                                      password=passwd,
                                      database=database,
                                      cursorclass=DictCursor,
                                      charset='utf8',
                                      connect_timeout=5)
        self.connDB.ping()

    def search_data(self, sql: str, data: Union[list, tuple, dict, None] = None) -> Any:
        """ 执行sql查询语句, 返回查询结果
        
        Args:
            sql (str): 待执行的sql语句
            data (Union[list, tuple, dict, None]): 替换sql语句中的变量, , 默认为空, \
            ``(list|tuple)`` 可以替换 ``%s``, ``dict`` 可以替换 ``%(name)``
        """
        with self.connDB.cursor() as cursor:
            cursor.execute(sql, data)
            return cursor.fetchall()

    def commit_data(self, sql: str, data: Union[list, tuple, dict, None] = None) -> Any:
        """ 执行sql语句, 并提交
        
        Args:
            sql (str): 待执行的sql语句
            data (Union[list, tuple, dict, None]): 替换sql语句中的变量, , 默认为空, \
            ``(list|tuple)`` 可以替换 ``%s``, ``dict`` 可以替换 ``%(name)``
        """

        with self.connDB.cursor() as cursor:
            cursor.execute(sql, data)
        self.connDB.commit()
