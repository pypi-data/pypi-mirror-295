#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 用于解析配置文件, 包含json、toml, 由于用法很简单, 仅做部分封装 """

__all__ = ['json_dumps', 'json_dump', 'json_loads', 'json_load']

import os
import json
from typing import Any


def json_dumps(data: Any) -> str:
    """ 将数据对象转化为json字符串 """

    return json.dumps(data, ensure_ascii=False)


def json_dump(data: Any, file: str, indent: int = 4, encoding: str = 'utf-8') -> None:
    """ 将数据对象写入json文件 """

    os.makedirs(os.path.dirname(file) or '.', exist_ok=True)
    with open(file, 'w', encoding=encoding) as fp:
        json.dump(data, fp, ensure_ascii=False, indent=indent)


def json_loads(data: str) -> Any:
    """ 读取json字符串至数据对象 """

    return json.loads(data)


def json_load(file: str, encoding: str = 'utf-8') -> Any:
    """ 读取json文件至数据对象 """

    with open(file, 'r', encoding=encoding) as fp:
        return json.load(fp)
