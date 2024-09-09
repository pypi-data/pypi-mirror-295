#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 用于gitlab相关操作 """

__all__ = ['GitTools']

import gitlab
import gitlab.v4.objects as GitObj
from typing import Any, Optional
from .logger import logger


class GitTools():
    """ 用于gitlab相关操作, 仅支持token认证
    
    Note: 
        1. 官方文档: `python-gitlab`_
    
    Args:
        token (str): private_token, 请使用用户私有token
        server (str): git服务器地址
        ssl_verify (bool): 是否启用SSL认证, 默认为True, 认证失败是建议置为False
    
    .. _python-gitlab:
        https://python-gitlab.readthedocs.io/en/v2.10.1/api/gitlab.v4.html#module-gitlab.v4.objects
    """

    LEVELS = {'reporter': 20, 'developer': 30, 'maintainer': 40}

    def __init__(self, token: str, server: str, ssl_verify: bool = True):
        self.gl = gitlab.Gitlab(url=server, private_token=token, timeout=10, ssl_verify=ssl_verify)
        self.git_url = None  # 用于减少重复查询
        self.user_ids = {}  # 用于缓存查询到的用户ID

    def _show_msg(self, msg: str, show: bool = False, raise_err: bool = False) -> None:
        """ 仅内部调用, 用于简化信息显示 """

        _func = logger.warn if show else logger.debug
        if raise_err:
            raise Exception(msg)
        else:
            _func(msg)

    def _get_item(self, item: object, ref: str, show: bool = False):
        """ 仅内部调用, 获取指定ref对象, item支持<commit/branch/tag> """

        if item:
            try:
                return item.get(id=ref)
            except Exception as err:
                self._show_msg('指定ref不存在: {} {}'.format(ref, err), show=show, raise_err=False)
        return None

    def _get_project(self, git_url: str, raise_err: bool = False) -> None:
        """ 仅内部调用, 获取git_url相关的git对象 """

        if self.git_url != git_url:
            # 相同git_url不再重复查询
            self.project: GitObj.projects.ProjectManager = None
            for project in self.gl.projects.list(all=True, search=git_url.strip('/').split('/')[-1].replace('.git',
                                                                                                            '')):
                if git_url in (project.web_url, project.http_url_to_repo, project.ssh_url_to_repo):
                    self.project = self.gl.projects.get(project.id)
                    break
            self.commit: GitObj.commits.ProjectCommitManager = self.project and self.project.commits
            self.branch: GitObj.branches.ProjectBranchManager = self.project and self.project.branches
            self.tag: GitObj.tags.ProjectTagManager = self.project and self.project.tags
            self.member: GitObj.members.ProjectMemberManager = self.project and self.project.members
            self.git_url = git_url

        if not self.project:
            self._show_msg('GitUrl不存在: {}'.format(git_url), show=True, raise_err=raise_err)

    def check_project(self, git_url: str) -> Any:
        """ 校验git_url是否存在, 返回project对象/None """

        self._get_project(git_url)
        return self.project

    def check_ref(self, git_url: str, ref: str) -> Any:
        """ 校验ref是否存在, 查询全部<branch/tag/commit>, 返回commit对象/None """

        self._get_project(git_url)
        return self._get_item(self.commit, ref)

    def check_branch(self, git_url: str, branch: str) -> Any:
        """ 校验branch是否存在, 返回branch对象/None """

        self._get_project(git_url)
        return self._get_item(self.branch, branch)

    def check_tag(self, git_url: str, tag_name: str) -> Any:
        """ 校验tag是否存在, 返回tag对象/None """

        self._get_project(git_url)
        return self._get_item(self.tag, tag_name)

    def get_refs(self, git_url: str, branch: bool = True, tag: bool = True) -> list:
        """ 获取git_url的全部分支和标签名称 """

        dst = []
        self._get_project(git_url)
        if branch:
            dst += [x.name for x in self.branch.list(all=True)]
        if tag:
            dst += [x.name for x in self.tag.list(all=True)]
        return dst

    def create_branch(self, git_url: str, branch: str, ref: str, force: bool = False) -> Any:
        """ 创建分支
        
        Args: 
            git_url (str): git仓库的url地址
            branch (str): 新分支名称
            ref (str): 基于的分支名/标签名/commit
            force (bool): 是否强制重建
        """

        self._get_project(git_url, raise_err=True)
        try:
            if self._get_item(self.branch, branch):
                # 不存在或需要强制重建
                if not force:
                    return logger.info('分支已存在: {}'.format(branch))
                logger.debug('删除分支: {}'.format(branch))
                self.branch.delete(branch)
            logger.debug('新建分支: {}'.format(branch))
            return self.branch.create({'branch': branch, 'ref': ref})
        except Exception as err:
            raise Exception('分支创建失败: {}'.format(err))

    def delete_branch(self, git_url: str, branch: str) -> None:
        """ 删除分支
        
        Args: 
            git_url (str): git仓库的url地址
            branch (str): 分支名称
        """

        self._get_project(git_url, raise_err=True)
        try:
            if self._get_item(self.branch, branch):
                logger.debug('删除分支: {}'.format(branch))
                self.branch.delete(branch)
            else:
                logger.info('分支不存在: {}'.format(branch))
        except Exception as err:
            raise Exception('分支删除失败: {}'.format(err))

    def create_tag(self, git_url: str, tag_name: str, ref: str, force: bool = False, msg: Optional[str] = None) -> Any:
        """ 创建标签
        
        Args: 
            git_url (str): git仓库的url地址
            tag_name (str): 新标签名称
            ref (str): 基于的分支名/标签名/commit
            force (bool): 是否强制重建, 默认为不重建
            msg (Optional[str]): 标签提交信息, 默认为空
        """

        self._get_project(git_url, raise_err=True)
        try:
            if self._get_item(self.tag, tag_name):
                # 不存在或需要强制重建
                if not force:
                    return logger.info('标签已存在: {}'.format(tag_name))
                logger.debug('删除标签: {}'.format(tag_name))
                self.tag.delete(tag_name)
            logger.debug('新建标签: {}'.format(tag_name))
            return self.tag.create({'tag_name': tag_name, 'ref': ref, 'message': msg})
        except Exception as err:
            raise Exception('标签创建失败: {}'.format(err))

    def delete_tag(self, git_url: str, tag_name: str) -> None:
        """ 删除标签

        Args: 
            git_url (str): git仓库的url地址
            tag_name (str): 标签名称
        """

        self._get_project(git_url, raise_err=True)
        try:
            if self._get_item(self.tag, tag_name):
                logger.debug('删除标签: {}'.format(tag_name))
                self.tag.delete(tag_name)
            else:
                logger.info('标签不存在: {}'.format(tag_name))
        except Exception as err:
            raise Exception('标签删除失败: {}'.format(err))

    def _get_users(self, users: str) -> list:
        """ 判断user_ids是否存在, 返回存在的user_id列表 """

        dst_user_ids = []
        for user in filter(None, [x.strip() for x in users.split(',')]):
            if user not in self.user_ids:
                user_id = None
                for _user in self.gl.users.list(all=True, search=user):
                    if user == _user.username:
                        user_id = _user.id
                        self._show_msg('GitUser查询成功: {}'.format([user, user_id]), show=False, raise_err=False)
                        break
                self.user_ids[user] = user_id
            if not self.user_ids[user]:
                self._show_msg('GitUser查询失败: {}'.format([user]), show=True, raise_err=False)
            else:
                dst_user_ids.append(self.user_ids[user])
        return dst_user_ids

    def update_auth(self, git_url: str, user_ids: str, access_level: str, expires_at: str) -> None:
        """ 添加用户权限, user_ids多个用英文逗号分隔 """

        self._get_project(git_url)
        _user_ids = self._get_users(user_ids)
        _level = self.LEVELS[access_level.lower()]
        _members = [x.username for x in self.member.list(all=True)]

        for user_id in _user_ids:
            if user_id not in _members:
                self.member.create({'user_id': user_id, 'access_level': _level, 'expires_at': expires_at})
                _members.append(user_id)
            else:
                self.member.update(id=user_id, new_data={'access_level': _level, 'expires_at': expires_at})
            self._show_msg('GitUser权限添加成功: {}'.format([user_id, _level, expires_at, git_url]), show=False)
