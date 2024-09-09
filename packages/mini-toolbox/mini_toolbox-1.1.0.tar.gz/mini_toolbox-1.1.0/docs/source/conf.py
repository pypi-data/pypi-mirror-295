# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# The full version, including alpha/beta/rc tags.
release = '1.1.0'

project = 'Python迷你工具箱'
author = 'gnzhoutian'
copyright = '2024, {}, 文档版本 {}, Python 3.6+'.format(author, release)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = [
    'modules.rst',
]

language = 'zh_CN'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = './_static/logo.png'
html_favicon = './_static/favicon.png'
html_title = 'Python迷你工具箱'
