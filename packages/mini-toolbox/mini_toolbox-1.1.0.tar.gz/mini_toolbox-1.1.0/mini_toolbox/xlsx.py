#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 用于xlsx相关操作

Note:
    1. 由于操作excel时具有较强的特殊性, 此处不提供封装
    2. openpyxl库操作明确, 建议直接根据业务做特殊化处理
    3. 建议使用openpyxl操作最新的xlsx文件
    4. 老的xls文件建议使用xlrd==1.2.0读取
    5. 官方文档: `openpyxl`_, `不同库差异1`_, `不同库差异2`_
    
.. _openpyxl:
    https://openpyxl.readthedocs.io/en/stable/tutorial.html
    
.. _不同库差异1:
    https://www.cnblogs.com/zcg-cpdd/p/14644668.html
    
.. _不同库差异2:
    https://zhuanlan.zhihu.com/p/353669230
"""

__all__ = ['openpyxl', 'xlrd']

import openpyxl
import xlrd
