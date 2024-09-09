#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 用于发送邮件通知 """

__all__ = ['Mail']

import os
import smtplib
import mimetypes
from email.message import EmailMessage
from email.utils import make_msgid
from typing import Optional, Union
from .logger import logger


class Mail():
    """ 用于发送邮件通知
    
    Note: 
        1. linux如果使用localhost, 可以使用postfix服务
        2. 官方文档: `smptlib`_, `module-email`_, `email-examples`_
    
    Args: 
        host (str): 邮件服务器地址
        suffix (str): 邮箱地址后缀, 如果邮箱地址中没有@符号, 则添加此后缀
        sender (str): 发件人地址, 可简写为邮箱地址前缀
        sender_desc (str): 发件人地址显示的用户名
        encode (str): 编码类型, 暂未使用
        port (int): 邮箱服务器端口, 默认为25, SSL端口一般为465
        ssl (str): 是否开启SSL认证
        level (int): 日志等级, ``0/1/2`` 分别表示 ``隐藏/少量/大量``, 默认为0
        username (str): 认证登陆用户, 默认为空, 一般为发件人地址
        password (str): 认证登陆密码, 默认为空
        
    .. _smptlib:
        https://docs.python.org/zh-cn/3/library/smtplib.html?highlight=smtplib
    
    .. _module-email:
        https://docs.python.org/zh-cn/3/library/email.html?highlight=email#module-email
    
    .. _email-examples:
        https://docs.python.org/zh-cn/3/library/email.examples.html#email-examples
    """

    def __init__(self,
                 host: str,
                 suffix: str,
                 sender: str,
                 sender_desc: str,
                 encode: str = 'utf-8',
                 port: int = 25,
                 ssl: bool = False,
                 level: int = 0,
                 username: str = None,
                 password: str = None):
        self.host = host
        self.port = port
        self.ssl = ssl
        self.level = level
        self.username = username
        self.password = password
        self.suffix = suffix
        self.encode = encode

        self.msg = EmailMessage()
        self.msg.policy = self.msg.policy.clone(max_line_length=256)  # fix issue33529 (GH-12020)
        self.msg['From'] = '{}<{}>'.format(sender_desc, self._gen_addr(sender))

    def _gen_addr(self, addr: str) -> str:
        """ 仅内部调用, 生成email地址 """

        return addr.strip() if '@' in addr else (addr.strip() + self.suffix)

    def _guess_type(self, file_path: str, ctype: Optional[str]) -> tuple:
        """ 仅内部调用, 判断文件的类型 """

        if not ctype:
            ctype, encoding = mimetypes.guess_type(file_path)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        return maintype, subtype

    def _send_msg(self):
        """ 仅内部调用, 发送消息对象 """

        _func = smtplib.SMTP_SSL if self.ssl else smtplib.SMTP
        with _func(self.host, self.port) as mail:
            mail.set_debuglevel(self.level)  # 开启debug
            if self.username and self.password:
                mail.login(self.username, self.password)
            mail.send_message(self.msg)

    def add_content(self, content: str, subtype: str = 'plain') -> None:
        """ 添加邮件正文 - 普通模式, 与关联模式互斥

        Args: 
            content (str): 正文内容
            subtype (str): 正文编码, 支持 ``plain/html`` 格式, 默认为plain(纯文本)
        """

        self.msg.set_content(content, subtype=subtype)

    def add_attachment(self,
                       path_list: Union[str, list],
                       ctype: Optional[str] = None,
                       sep: Optional[str] = None) -> None:
        """ 添加邮件附件
        
        Args: 
            path_list (Union[str, list]): 附件路径列表, str会自动 ``split(sep)`` 为列表
            ctype (Optional[str]): 文件类型, 默认为自动检测, 建议默认, 示例: ``image/png``, 详见 ``mimetypes``
            sep (Optional[str]): 附件路径列表分隔符, 默认为空格
        """

        if isinstance(path_list, str):
            path_list = path_list.split(sep)

        for file_path in path_list:
            file_name = os.path.basename(file_path)
            maintype, subtype = self._guess_type(file_path, ctype)

            with open(file_path, 'rb') as fp:
                data = fp.read()
                self.msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=file_name)

    def add_related_content(self,
                            content: str,
                            relate_dict: dict,
                            is_path: bool = True,
                            ctype: Optional[str] = None) -> None:
        """ 添加邮件正文 - 关联模式, 与普通模式互斥, 支持邮件正文中显示图片
        
        Warning:
            * 不支持手动指定多种data类型, 如果需要, 请保存为文件后自动检测
            * 如果is_path为False, 则需要手动指定ctype, 如: ``'image/png'``
        
        Args: 
            content (str): 正文内容, 正文编码只支持html
            relate_dict (dict): 正文html中format()时需要关联的键值对, ``{'html中变量': '文件路径或data'}``
            is_path (bool): relate_dict的键值是否为文件路径, 默认为True, 建议使用文件路径
            ctype (Optional[str]): 文件类型, 默认为自动检测, 建议默认
        """

        cids_dict = {}
        for item in relate_dict:
            cids_dict[item] = make_msgid()[1:-1]

        self.msg.add_alternative(content.format(**cids_dict), subtype='html')

        logger.debug(self.msg.get_payload())
        payload = self.msg.get_payload(0)

        for item in relate_dict:
            data = relate_dict[item]
            if is_path:
                maintype, subtype = self._guess_type(data, ctype)
                with open(data, 'rb') as fp:
                    data = fp.read()
            payload.add_related(data, maintype=maintype, subtype=subtype, cid=cids_dict[item])

    def send_mail(self,
                  subject: str,
                  receivers: Union[str, list],
                  cc_receivers: Union[str, list] = [],
                  bcc_receivers: Union[str, list] = [],
                  sep: Optional[str] = None) -> None:
        """ 发送邮件
        
        Args: 
            subject (str): 邮件主题
            receivers (Union[str, list]): 收件人地址列表, str会自动 ``split(sep)`` 为列表, 可简写为邮箱地址前缀
            cc_receivers (Union[str, list]): 抄送人地址列表, str会自动 ``split(sep)`` 为列表, 可简写为邮箱地址前缀, 默认为空
            bcc_receivers (Union[str, list]): 密送人地址列表, str会自动 ``split(sep)`` 为列表, 可简写为邮箱地址前缀, 默认为空
            sep (Optional[str]): 收件人地址列表分隔符, 默认为空格
        """

        # 生成收件人列表
        if isinstance(receivers, str):
            receivers = receivers.split(sep)
        receivers = [self._gen_addr(x) for x in receivers]

        # 生成抄送人列表
        if isinstance(cc_receivers, str):
            cc_receivers = cc_receivers.split(sep)
        cc_receivers = [self._gen_addr(x) for x in cc_receivers]

        # 生成密送人列表
        if isinstance(bcc_receivers, str):
            bcc_receivers = bcc_receivers.split(sep)
        bcc_receivers = [self._gen_addr(x) for x in bcc_receivers]

        # 配置邮件头
        self.msg['Subject'] = subject
        self.msg['To'] = ','.join(receivers)  # 仅支持,号
        self.msg['Cc'] = ','.join(cc_receivers)  # 仅支持,号
        self.msg['Bcc'] = ','.join(bcc_receivers)  # 仅支持,号

        logger.debug(receivers)

        # 发送邮件
        self._send_msg()
