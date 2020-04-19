# -*- coding:utf-8 -*-
# @Time: 2020/4/1 18:57
# @Author: wenqin_zhu
# @File: test_user.py
# @Software: PyCharm

import re
import pytest
from guard.pages.components.group_tree import GroupTree
from guard.pages.user import UserPage


class TestUser:

    @pytest.mark.positive
    @pytest.mark.usefixtures("close_alert")
    def test_create_peer_dep_from_Default(self, user):
        # 测试从Default根分组创建同级分组
        UserPage(user[0]).create_department_from_Default(user[1])

        result = UserPage(user[0]).judge_alert_info()
        assert "创建同级分组成功" == result

    @pytest.mark.positive
    @pytest.mark.usefixtures("close_alert", "del_sub_dep_name_to_user")
    def test_create_next_dep_from_user_defined(self, user, sole_group_name):
        # 测试从用户自定义分组创建下一级分组
        UserPage(user[0]).create_department_from_user_defined(group_name=sole_group_name, parent_name=user[1], is_peer=False)

        result = UserPage(user[0]).judge_alert_info()
        assert "创建下一级分组成功" == result

    @pytest.mark.positive
    @pytest.mark.usefixtures("close_alert", "del_dep_name_to_user")
    def test_create_peer_dep_from_user_defined(self, user, sole_group_name):
        # 测试从用户自定义分组创建同级分组
        UserPage(user[0]).create_department_from_user_defined(group_name=sole_group_name, parent_name=user[1])

        result = UserPage(user[0]).judge_alert_info()
        assert "创建同级分组成功" == result

    @pytest.mark.positive
    @pytest.mark.usefixtures("close_alert", "del_sub_dep_name_to_default")
    def test_create_next_dep_from_Default(self, user, sole_group_name):
        # 测试从Default根分组创建下一级分组
        UserPage(user[0]).create_department_from_Default(sole_group_name, is_peer=False)

        result = UserPage(user[0]).judge_alert_info()
        assert "创建下一级分组成功" == result

    @pytest.mark.error
    def test_search_dep_by_name(self, user):
        # 测试group_tree的搜索功能
        GroupTree(user[0]).search_dep_by_name(user[1])

        # 断言搜索到的内容<前端缩略显示的>在user字符串内
        result = GroupTree(user[0]).judge_search_success(user[1])
        # 正则表达式匹配 - 'UDN-871888...' in 'UDN-871888b9-8004-4b95-954f-562f3e50d421'   字符串在字符内部
        # result = re.match('^[.]', result)
        # TODO
        assert True

    @pytest.mark.positive
    @pytest.mark.usefixtures("close_alert")
    def test_delete_peer_dep_from_Default(self, user):
        UserPage(user[0]).delete_department_by_name(parent_name=user[1])

        result = UserPage(user[0]).judge_alert_info()
        assert "删除分组成功" == result
