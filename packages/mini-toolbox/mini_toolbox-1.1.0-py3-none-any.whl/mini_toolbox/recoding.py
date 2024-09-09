#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 
Note:
    提供命令行工具 ``file_recoding``, 用于转换文件编码, 使用 ``-h`` 查看命令行帮助
"""

__all__ = ['file_recoding']

import sys
import argparse


def file_recoding(file_path: str, src_encoding: str, dst_encoding: str, errors: str = 'ignore') -> str:
    """ 将文件转化从原编码转化为指定编码
    
    Args: 
        file_path (str): 文件路径
        src_encoding (str): 文件当前编码
        dst_encoding (str): 目标转换编码
        errors (str): 遇到错误时处理模式, 默认为 ``ignore``, 可选: ``strict/ignore/replace``
    
    Returns:
        str: 解码后的文档内容
    """

    with open(file_path, 'r', encoding=src_encoding, errors=errors) as fp:
        data = fp.read()

    with open(file_path, 'w+', encoding=dst_encoding, errors=errors) as fp:
        fp.write(data)

    return data


def main():
    """ 用于命令行直接调用, 转换文件编码, 使用 ``-h`` 查看命令行帮助 """

    parser = argparse.ArgumentParser(description='转换文件编码')
    parser.add_argument('FilePath', help='文件路径')
    parser.add_argument('-s', help='文档当前编码, 默认为gbk', default='gbk', metavar='SrcEncoding')
    parser.add_argument('-d', help='目标转换编码, 默认为utf-8', default='utf-8', metavar='DstEncoding')
    parser.add_argument('-e', help='遇到错误时处理方式, 默认为ignore, 可选strict/ignore/replace', default='ignore', metavar='Errors')
    args = parser.parse_args()

    file_recoding(args.FilePath, args.s, args.d, args.e)
    sys.exit(0)


if __name__ == '__main__':
    main()