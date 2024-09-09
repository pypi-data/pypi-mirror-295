#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 用于操作免认证的api获取返回json数据 """

__all__ = ['api_get', 'api_post']

import requests
from typing import Optional


def api_get(api_url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
    """ 获取GET请求响应中json数据

    Args: 
        api_url (str): api接口地址
        params (dict): 参数字典
        headers (dict): 请求头字典
        
    Returns: 
        dict: 接口返回的json数据
    """

    rsp = requests.get(api_url, params, headers=headers)
    return rsp.json()


def api_post(api_url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
    """ 获取POST请求响应中json数据

    Args: 
        api_url (str): api接口地址
        params (dict): 参数字典
        headers (dict): 请求头字典
        
    Returns: 
        dict: 接口返回的json数据
    """

    _headers = {'Content-type': 'application/json', 'Charset': 'UTF-8', 'Accept': 'text/plain'}
    if isinstance(headers, dict):
        _headers.update(headers)

    rsp = requests.post(api_url, json=params, headers=_headers)
    return rsp.json()
