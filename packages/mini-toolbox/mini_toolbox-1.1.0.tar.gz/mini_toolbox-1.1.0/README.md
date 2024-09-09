# 说明文档
  
  [![GitHub stars][github-stars-badge]][github-stars-link]
  [![GitHub forks][github-forks-badge]][github-forks-link]
  [![GitHub issues][github-issues-badge]][github-issues-link]
  [![GitHub license][github-license-badge]][github-license-link]
  [![Documentation Status][rtd-badge]][rtd-link]
  [![Python version][python-badge]][pypi-link]
  [![PyPI][pypi-badge]][pypi-link]
  [![PyPI - Downloads][install-badge]][install-link]

## 简述

Python迷你工具箱，包含简化的常用工具，旨在帮助脚本快速开发。

它具有调用方式统一、参数简单、实现相对简明、文档相对清晰的特点。

功能描述详见[接口文档][rtd-link]，常用功能如：执行系统命令、创建/删除文件夹、压缩解压、日志工具、哈希计算、字符加密、邮件发送、钉钉通知、ssh连接、xml解析等。

## 安装说明

```shell
# python版本要求
    依赖python3.6+版本, 默认centos7环境yum安装的python3可以使用
    
# pip仓库配置示例(网速慢建议更换为镜像仓库)
    # unix: ~/.pip/pip.conf
    # win: %APPDATA%\pip\pip.ini
    
    [global]
    index-url = http://pypi.douban.com/simple
    trusted-host = pypi.douban.com

# 安装方式
    # 完全安装, 建议, 可以使用全部功能
        pip3 install mini-toolbox[full]
    
    # 最小化安装, 仅使用原生python3, 可用模块详见源码, 常用模块如下: 
    # utils/path/extra/logger/hash/archive/mail/pip_list/conifg/ftp
        pip3 install mini-toolbox

# 发布地址
    Download: https://pypi.org/project/mini-toolbox
    Document: https://mini-toolbox.readthedocs.io
```

## 调用示例

```python
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" mini_toolbox调用示例, unix环境中执行 """

from mini_toolbox.path import mkdirs, pushd
from mini_toolbox.utils import exec_cmd
from mini_toolbox.logger import Logger

# 实例化日志工具
logger = Logger(logger_id='test_lib', to_file=False).logger

# 重建dir2文件夹
mkdirs('dir1/dir2', is_file=False, remake=True)

# 进入dir1/dir2文件夹, 执行结束后返回原路径
with pushd('dir1/dir2'):
    # 创建dir3目录, 存在则忽略
    mkdirs('dir3/file1', is_file=True)

    # 执行`ls -lh`指令, 输出用日志工具打印
    rst = exec_cmd('ls -lh')
    logger.debug(rst)

# 执行`find .`指令, 输出直接打印
exec_cmd('find .', live=True)
```

## 格式规范

- **编码遵循[Google Python编码风格][google-style]**
- **文档编写遵循附录中的[Google风格文档编写示例](#sphinx-google-style)**


```shell
# 迭代说明
    1. 版本采用三段式 x.y.z
    2. x 表示主版本 - 当产生重大变更或重大里程碑时, x+1, y=z=0
    3. y 表示增量版本 - 当z版本大于9时, y+1, z=0
    4. z 表示补丁版本 - 当涉及变更时, z+1, z<=9

# 命名大小写
    1. 类: 单词首字母大写
    2. 全局变量: 字母大写, 下划线分隔
    3. 内部函数/方法/对象/变量/模块: 单下划线开头, 小写字母, 下划线分隔
    4. 其它函数/方法/对象/变量/模块: 小写字母, 下划线分隔
    
# 其它约定
    1. 格式化 - 使用yapf插件格式化代码 # pip3 install yapf
    2. 兼容性 - 相同x版本, 做到向后兼容, 尽量做到向前兼容
    3. 更新日志 - 提供y版本的详细变更日志和时间, 做到描述简练、分类正确
    4. 实现范围 - 不涉及业务代码, 删除冗余代码/注释, 做到相对独立性和通用性
    5. 标点符号 - 代码段中的逗号、冒号、分号全部使用英文符号
    5. 类型注释 - 尽量提供代码类型注释
        - int/float/str/bool/None
        - from typing import Dict, List, Tuple, Optional, Union, Any
```

## 打包说明

``` shell
# 将本地目录作为库安装调试
python3 -m pip install --upgrade pip setuptools wheel
pip3 install -e .[full,docs,build]

# 手动格式化代码
./build.sh format

# 编译和预览文档
./build.sh doc

# 编译全部
./build.sh

# 更新版本及编译 - x/y/z
./build.sh z
```

## 附录

<a id="sphinx-google-style"></a>

### Google风格文档编写示例

```shell
"""Example Google style docstrings(One line summary).

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Sections support any reStructuredText formatting, including literal 
    blocks::

        $ python example_google.py

    >>> print([i for i in example_generator(4)])
    [0, 1, 2, 3]

Attributes:
    likes_spam: A boolean indicating if we like SPAM or not.
    eggs: An integer count of the eggs we have laid.

Args:
    param1 (int): The first parameter.
    param2 (str): The second parameter.
    keys (str): A sequence of strings representing the key of each table \
    row to fetch.  String keys will be UTF-8 encoded.

Returns:
    bool: The return value. True for success, False otherwise.

Raises:
    IOError: An error occurred accessing the smalltable.

Todo:
    * For module TODOs, need ``sphinx.ext.todo`` extension
    * This is colorful block

Note:
    This is colorful block

Warning:
    This is colorful block

See Also:
    This is colorful block. `PEP 484`_ type annotations are supported.

.. _Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html

.. _PEP 484:
    https://www.python.org/dev/peps/pep-0484/
"""
```

### Pypi官方打包说明

```shell
1. 注册账户, 配置token  # https://pypi.org/
    # cat ~/.pypirc
    [pypi]
        username = __token__
        password = pypi-xxxxxxxxxxxxxxxxxxxxxxxxxx
    
2. 安装依赖
    python3 -m pip install --upgrade pip setuptools wheel
    pip3 install build virtualenv twine

3. 执行打包
    python3 -m build

4. 执行上传
    python3 -m twine upload --repository pypi dist/*
```


### 参考链接

- [[官方] Python项目打包](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [[官方] Read the Docs简明文档](https://docs.readthedocs.io/en/stable/)
- [[官方] Sphinx文档](https://www.sphinx-doc.org/en/master/index.html)
- [[官方] Sphinx Read the Docs主题](https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html)
- [[官方] Sphinx Google编码风格支持](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/)
- [[官方] Google开源项目风格指南-中文版][google-style]
- [[官方] Python PEP-8](https://peps.python.org/pep-0008)
- [[官方] Python Cookbook](https://python3-cookbook.readthedocs.io/zh_CN/latest/copyright.html)

[google-style]: https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/

[github-stars-badge]: https://img.shields.io/github/stars/gnzhoutian/mini_toolbox.svg
[github-stars-link]: https://github.com/gnzhoutian/mini_toolbox/stargazers

[github-forks-badge]: https://img.shields.io/github/forks/gnzhoutian/mini_toolbox.svg
[github-forks-link]: https://github.com/gnzhoutian/mini_toolbox/network

[github-issues-badge]: https://img.shields.io/github/issues/gnzhoutian/mini_toolbox.svg
[github-issues-link]: https://github.com/gnzhoutian/mini_toolbox/issues

[github-license-badge]: https://img.shields.io/badge/license-MIT-blue.svg
[github-license-link]: https://raw.githubusercontent.com/gnzhoutian/mini_toolbox/main/LICENSE

[python-badge]: https://img.shields.io/badge/python-3.6%2B-orange
[python-link]: https://pypi.org/project/mini-toolbox

[rtd-badge]: https://readthedocs.org/projects/mini-toolbox/badge/?version=latest
[rtd-link]: https://mini-toolbox.readthedocs.io?badge=latest

[pypi-badge]: https://img.shields.io/pypi/v/mini-toolbox.svg
[pypi-link]: https://pypi.org/project/mini-toolbox

[install-badge]: https://img.shields.io/pypi/dw/mini-toolbox?label=pypi%20installs
[install-link]: https://pypistats.org/packages/mini-toolbox
