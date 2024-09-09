#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 标准化日志工具

__all__ = ['Logger']

import os
import logging
from logging import Logger as LoggerType
from logging import handlers
from typing import Any

try:
    import colorlog
    COLORLOG = True
except ModuleNotFoundError:
    COLORLOG = False


def _success(self, msg, *args, **kwargs):
    """ SUCCESS等级处理函数 """

    if self.isEnabledFor(logging.SUCCESS):
        self._log(logging.SUCCESS, msg, args, **kwargs)


class Logger():
    """ 标准化日志工具
    
    Warning:
        同一logger_id仅第一次初始化时生效, 后续重复初始化不再改变
    
    Attributes:
        logger: 实例化后的日志工具
    
    Args:
        logger_id (str): logger的名称, 默认为 ``mini``
        file_path (str): 日志文件名, 默认为 ``./all.log``
        to_file (bool): 是否写入文件, 默认为True
        to_console (bool): 是否输出至控制台, 默认为True
        color_file (bool): 文件输出为彩色, 默认为True
        color_console (bool): 控制台输出为彩色, 默认为True
        show_process (bool): 日志输出显示进程字段, 默认为False
        show_thread (bool): 日志输出显示线程字段, 默认为False
        show_module (bool): 日志输出显示模块字段, 默认为False
        level (str): 日志显示等级, 默认为 DEBUG, 可选项 ``('FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'SUCCESS')``
        log_size (float): 单个日志文件大小(MB), 默认为10MB
        log_count (int): 日志备份数量, 默认为10个
        encoding (str): 写入文件的编码, 默认为'utf-8'

    Example:
        >>> logger = Logger().logger
        >>> logger.info('this is info message.')
    """

    def __init__(self,
                 logger_id: str = 'mini',
                 file_path: str = 'all.log',
                 to_file: bool = True,
                 to_console: bool = True,
                 color_file: bool = True,
                 color_console: bool = True,
                 show_process: bool = False,
                 show_thread: bool = False,
                 show_module: bool = False,
                 level: str = 'DEBUG',
                 log_size: float = 10.0,
                 log_count: int = 10,
                 encoding: str = 'utf-8'):
        self.logger_id = logger_id
        self.file_path = file_path
        self.to_file = to_file
        self.to_console = to_console
        self.color_file = color_file and COLORLOG
        self.color_console = color_console and COLORLOG
        self.show_process = show_process
        self.show_thread = show_thread
        self.show_module = show_module
        self.level = level
        self.log_size = log_size
        self.log_count = log_count
        self.encoding = encoding

        self._add_success_level()
        self.logger: LoggerType = logging.getLogger(self.logger_id)
        self._set_logger()

    def _add_success_level(self) -> None:
        """ logging新增success等级 """
        logging.SUCCESS = 60
        logging.addLevelName(logging.SUCCESS, 'SUCCESS')
        logging.Logger.success = _success

    def _set_logger(self) -> None:
        """ 初始化logger """

        self.logger.setLevel(self.level)

        if len(self.logger.handlers) == 0:
            if self.to_file:
                file_handler = self._configure_file()
                self.logger.addHandler(file_handler)
                file_handler.close()
            if self.to_console:
                console_handler = self._configure_console()
                self.logger.addHandler(console_handler)
                console_handler.close()

    def _configure_console(self) -> Any:
        """ 配置 console handler """

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(self._get_formatter(self.color_console))
        return console_handler

    def _configure_file(self) -> Any:
        """ 配置 file handler """

        max_size = 1024 * 1024 * self.log_size  # log_size MB
        os.makedirs(os.path.dirname(self.file_path) or '.', exist_ok=True)
        file_handler = handlers.RotatingFileHandler(filename=self.file_path,
                                                    maxBytes=max_size,
                                                    backupCount=self.log_count,
                                                    encoding=self.encoding)
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self._get_formatter(self.color_file))
        return file_handler

    def _get_formatter(self, color: bool = False) -> Any:
        """ 配置 日志样式 """

        colors_cfg = {
            'DEBUG': 'green',
            # 'INFO': 'white',
            'WARNING': 'bold_yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'red',
            'SUCCESS': 'bold_green',
        }
        log_fmt = '[%(asctime)s.%(msecs)03d][%(name)s]{}{}[%(levelname)s][%(filename)s:%(lineno)d]{}: %(message)s'.format(
            '[%(processName)s]' if self.show_process else '',
            '[%(threadName)s]' if self.show_thread else '',
            '[%(funcName)s]' if self.show_module else '',
        )
        color_fmt = '%(log_color)s' + log_fmt
        date_fmt = "%Y-%m-%d %H:%M:%S"

        if color:
            fmt = colorlog.ColoredFormatter(fmt=color_fmt, datefmt=date_fmt, log_colors=colors_cfg)
        else:
            fmt = logging.Formatter(fmt=log_fmt, datefmt=date_fmt)
        return fmt


# 仅内部调用, 抢占并声明id为'mini_toolbox'的logger, 以免外部引用时影响库内部日志输出
logger = Logger(logger_id='mini_toolbox', to_file=False, level='WARN').logger
