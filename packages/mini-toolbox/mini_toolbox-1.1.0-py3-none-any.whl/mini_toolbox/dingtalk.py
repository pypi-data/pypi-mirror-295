#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 用于钉钉群消息通知 """

__all__ = ['DingTalk']

import hmac
import time
import requests
from base64 import b64encode
from hashlib import sha256
from typing import Optional, Union
from .logger import logger


class DingTalk():
    """ 用于钉钉群消息通知, 仅支持text模式, 详见 `钉钉官方文档`_
    
    Args: 
        token (str): Webhook中的access_token
        secret (Optional[str]): 加签模式的密钥, 可选, 默认为关键字模式, 实现详见 `官方签名文档`_
        user_dict (Optional[dict]): 导入 ``{'用户名':'手机号'}`` 键值对, 用于在at_users中直接选择用户名
        ding_url (str): 钉钉官方api接口的url前缀(不含token)或者公司私用接口
        
    .. _钉钉官方文档:
        https://open.dingtalk.com/document/group/custom-robot-access
        
    .. _官方签名文档:
        https://open.dingtalk.com/document/group/customize-robot-security-settings
    """

    def __init__(self,
                 token: str,
                 secret: Optional[str] = None,
                 user_dict: Optional[dict] = None,
                 ding_url: str = 'https://oapi.dingtalk.com/robot/send?access_token='):
        self.token = token or ''
        self.secret = secret or ''
        self.user_dict = user_dict or {}
        self.ding_url = ding_url

        self.headers = {'Content-Type': 'application/json', 'Charset': 'UTF-8'}

    def _gen_sign(self) -> str:
        """ 仅内部调用, 生成钉钉签名, 返回加签的url字符串 """

        if not self.secret:
            return ''

        timestamp = str(round(time.time() * 1000))
        sign = '{}\n{}'.format(timestamp, self.secret)
        b_sign = sign.encode('utf-8')
        b_secret = self.secret.encode('utf-8')
        sign = b64encode(hmac.new(b_secret, b_sign, digestmod=sha256).digest()).decode('utf-8')

        return '&timestamp={}&sign={}'.format(timestamp, sign)

    def _trans_users(self, users: Union[list, str] = []):
        """ 仅内部调用, 转换用户至手机号列表 """

        if isinstance(users, str):
            users = filter(None, [x.strip() for x in users.split(',')])
        return [self.user_dict.get(x, x) for x in users]

    def send(self,
             content: Optional[str] = None,
             at_users: Union[list, str] = [],
             at_all: bool = False,
             sep: Optional[str] = None) -> dict:
        """ 发送钉钉消息
        
        Args: 
            content (Optional[str]): 消息正文, 默认为 ``'None'``, 支持 ``\\n\\t`` 等扩展字符
            at_users (Union[list, str]): 用于@指定人员, 填写手机号或user_dict中的用户名, \
            str会自动 ``split(sep)`` 为列表
            at_all (bool): 是否@所有人, 默认为False
            sep (Optional[str]): @指定人员列表分隔符, 默认为空格
            
        Returns: 
            dict: 返回api的响应体信息, 如: {'errcode': 0, 'errmsg': 'ok'}
        """

        url = self.ding_url + self.token + self._gen_sign()
        payload = {
            "msgtype": "text",
            "text": {
                "content": str(content)
            },
            "at": {
                "atMobiles": self._trans_users(at_users),
                "isAtAll": at_all,
            },
        }

        logger.debug('url: {}, headers: {}, payload: {}'.format(url, self.headers, payload))
        rsp = requests.post(url, headers=self.headers, json=payload)
        return rsp.json()
