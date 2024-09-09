#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 用于XML相关操作

__all__ = ['XmlTools']

from lxml import etree
from lxml.etree import _Comment as CM
from lxml.etree import _Element as EM
from lxml.etree import _ElementTree as ET
from typing import List, Optional, Union


class XmlTools():
    """ 用于XML相关操作

    Args:
        file (str): xml文件路径
        pretty (bool): 是否格式化保存, 默认为原始格式
    
    Note:
        官方文档: `Element`_, `ElementTree`_, `xpath`_, `findall`_
    
    Example:
        lxml.etree 语法示例::
        
            # 节点间位置关系约定: 父节点, 子节点, 上节点(同级), 下节点(同级)
            
            node.findall(xpath)      # 搜索 # 查找全部匹配子节点, 返回列表
            node.find(xpath)         # 搜索 # 查找首个匹配子节点, 返回节点
            
            node.iter()              # 遍历 # 递归遍历子节点
            node.itertext()          # 遍历 # 递归遍历子节点文本
            node.iterchildren()      # 遍历 # 遍历子节点
            
            node.getparent()         # 获取 # 获取父节点
            node.getprevious()       # 获取 # 获取上节点
            node.getnext()           # 获取 # 获取下节点
            root.makeelement(name)   # 获取 # 创建节点
            
            node.append(_node)       # 增删 # 新增子节点
            node.addprevious(_node)  # 增删 # 新增上节点
            node.addnext(_node)      # 增删 # 新增下节点
            node.remove(_node)       # 增删 # 删除节点
            
            node.tag                 # 编辑 # 节点标签
            node.text                # 编辑 # 节点文本
            node.attrib              # 编辑 # 节点属性
            node.get(key)            # 编辑 # 节点属性获取
            node.set(key, value)     # 编辑 # 节点属性增改
            
        node.findall(xpath) 简化语法示例::
        
            .                        # 当前节点
            ..                       # 父节点
            *                        # 下级全部子节点
            //                       # 递归全部子节点
            
            [@key]                   # 节点存在指定属性
            [@key='value']           # 节点存在指定键值对
            [tag]                    # 子节点存在指定标签
            [tag='text']             # 子节点存在指定标签文本对

    .. _Element:
        https://lxml.de/2.2/api/lxml.etree._Element-class.html
    
    .. _ElementTree:
        https://lxml.de/2.2/api/lxml.etree._ElementTree-class.html
        
    .. _xpath:
        https://docs.python.org/3/library/xml.etree.elementtree.html#supported-xpath-syntax
        
    .. _findall:
        https://lxml.de/FAQ.html#what-are-the-findall-and-xpath-methods-on-element-tree
    """

    def __init__(self, file: str, pretty: bool = False) -> None:
        self.file = file
        self.pretty = pretty

        if self.pretty:
            parser = etree.XMLParser(remove_blank_text=True)
            self.tree: ET = etree.parse(file, parser=parser)
        else:
            self.tree: ET = etree.parse(file)

        self.root: EM = self.tree.getroot()
        self.nsmap = self.root.nsmap

    def save(self, as_file: Optional[str] = None, encoding: str = 'utf-8', indent: str = '    ') -> None:
        """ 保存或另存为文件
    
        Args:
            as_file (str): 另存为文件, 默认为更新原始文件
            encoding (str): 文件编码, 默认为utf-8
            indent (str): 格式化保存时缩进, 默认为4个空白字符
        """

        if self.pretty:
            etree.indent(self.tree, indent)
        self.tree.write(as_file or self.file, encoding=encoding, pretty_print=self.pretty, xml_declaration=True)

    def _seq_nodes(self, nodes: Union[EM, List[EM]], reverse: bool) -> List[EM]:
        """ 仅内部调用, 序列化nodes节点 """

        if not isinstance(nodes, list):
            nodes = [nodes]
        if reverse:
            nodes.reverse()
        return nodes

    def findall(self, xpath: str) -> List[EM]:
        """ 查找全部匹配子节点, 返回节点列表 """

        return self.root.findall(xpath, namespaces=self.nsmap)

    def find(self, xpath: str) -> Optional[EM]:
        """ 查找首个匹配子节点, 返回节点 """

        _t = self.findall(xpath)
        return _t[0] if _t else None

    def getprev(self, node: EM) -> Optional[EM]:
        """ 获取上节点 """

        if node is not None:
            return node.getprevious()

    def getnext(self, node: EM) -> Optional[EM]:
        """ 获取下节点 """

        if node is not None:
            return node.getnext()

    def getparent(self, node: EM) -> Optional[EM]:
        """ 获取父节点 """

        if node is not None:
            return node.getparent()

    def addchild(self, base: EM, nodes: Union[EM, List[EM]], reverse: bool = False) -> EM:
        """ 新增子节点, 支持同时添加多个, 返回base节点 """

        for node in self._seq_nodes(nodes, reverse):
            base.append(node)
        return base

    def addprev(self, base: EM, nodes: Union[EM, List[EM]], reverse: bool = False) -> EM:
        """ 新增上节点, 支持同时添加多个, 返回base节点 """

        for node in self._seq_nodes(nodes, reverse):
            base.addprevious(node)
        return base

    def addnext(self, base: EM, nodes: Union[EM, List[EM]], reverse: bool = False) -> EM:
        """ 新增下节点, 支持同时添加多个, 返回base节点 """

        for node in self._seq_nodes(nodes, reverse):
            base.addnext(node)
        return base

    def remove(self, node: EM) -> None:
        """ 删除节点 """

        parent = self.getparent(node)
        if parent is not None:
            parent.remove(node)

    def gettag(self, node: EM) -> Optional[str]:
        """ 节点标签获取 """

        if node is not None:
            return node.tag

    def gettext(self, node: EM) -> Optional[str]:
        """ 节点文本获取 """

        if node is not None:
            return node.text

    def getattr(self, node: EM, key: str) -> Optional[str]:
        """ 节点属性获取 """

        if node is not None:
            return node.get(str(key))

    def settext(self, node: EM, text: Optional[str] = None) -> None:
        """ 节点文本修改 """

        if node is not None and text is not None:
            node.text = str(text)

    def setattr(self, node: EM, attrib: Optional[dict] = None) -> None:
        """ 节点属性增改 """

        if node is not None and attrib is not None:
            for k, v in attrib.items():
                node.set(str(k), str(v))

    def makenode(self,
                 tag: str,
                 text: Optional[str] = None,
                 attrib: Optional[dict] = None,
                 namespace: Optional[str] = None) -> EM:
        """ 创建节点 
        
        Args:
            tag (str): 节点标签
            text (str): 节点文本
            attrib (dict): 节点属性
            namespace (Optional[str]): 节点命名空间, 默认为None, 自动处理
        """

        if namespace in self.nsmap:
            node: EM = self.root.makeelement('{{{}}}{}'.format(self.nsmap[namespace], tag), nsmap=self.nsmap)
        else:
            node: EM = self.root.makeelement(tag, nsmap=self.nsmap)
        self.settext(node, text)
        self.setattr(node, attrib)
        return node

    def makenote(self, text: str, space: str = ' ') -> CM:
        """ 创建注释, 默认文本前后添加一个空格 """

        return etree.Comment('{}{}{}'.format(space, text, space))
