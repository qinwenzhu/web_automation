# -*- coding:utf-8 -*-
# @Time: 2020/3/30 18:52
# @Author: wenqin_zhu
# @File: user.py
# @Software: PyCharm

import time
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from guard.pages.components.group_tree import GroupTree


class UserPage(BasePage):

    def create_department_from_Default(self, group_name, is_peer=True):
        """
        通过Default部门创建 同级/下一级分组
        :param group_name: 组名称
        :param is_peer: 判断是否创建同级分组  默认为创建同级
        """
        if is_peer:
            # 滑动到创建同级分组
            GroupTree(self.driver).click_menu_by_name("Default", "创建同级")
            # 动态定位title 为 创建同级
            GroupTree(self.driver).create_dep_group_com(group_name, "创建同级")
        else:
            # 滑动到创建下一级分组
            GroupTree(self.driver).click_menu_by_name("Default", "创建下一级")
            # 动态定位title 为 创建下一级
            GroupTree(self.driver).create_dep_group_com(group_name, "创建下一级")

    def create_department_from_user_defined(self, group_name, parent_name="Default", is_peer=True):
        if is_peer:
            # 滑动到创建同级分组
            GroupTree(self.driver).click_menu_by_name(parent_name, "创建同级")
            # 动态定位title 为 创建同级
            GroupTree(self.driver).create_dep_group_com(group_name, "创建同级")
        else:
            # 滑动到创建下一级分组
            GroupTree(self.driver).click_menu_by_name(parent_name, "创建下一级")
            # 动态定位title 为 创建下一级
            GroupTree(self.driver).create_dep_group_com(group_name, "创建下一级")

    def delete_department_by_name(self, sub_name=None, parent_name="Default", is_peer=True, delete=True):
        """
        通过组名称删除分组
        :param sub_name: 子级分组
        :param parent_name: 父级分组
        :param is_peer: 判断删除父级/子级分组，默认删除父级
        :param delete: 判断点击删除还是取消按钮，默认删除
        """
        if is_peer:
            GroupTree(self.driver).click_group_by_name(parent_name)
            # 滑动到删除
            GroupTree(self.driver).click_menu_by_name(parent_name, "删除")
        else:
            # 点击父级分组，出现子级分组列表
            GroupTree(self.driver).click_group_by_name(parent_name)
            time.sleep(0.5)
            # 滑动到删除
            GroupTree(self.driver).click_menu_by_name(sub_name, "删除")

        if delete:
            # 点击删除按钮
            GroupTree(self.driver).delete_dep_group_com()
        else:
            # 点击取消按钮
            GroupTree(self.driver).delete_dep_group_com(delete=False)

    def judge_alert_info(self):
        # 定位alert弹框的文本
        INFO_TEXT = (By.XPATH, '//div[@role="alert"]//p')
        # 强制等待元素可见
        BasePage(self.driver).wait_for_ele_to_be_visible(INFO_TEXT)
        return BasePage(self.driver).get_text(INFO_TEXT)

    def add_user(self):
        # 添加用户
        pass


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.components.menubar import MenubarPage
    from guard.pages.login import LoginPage
    driver = webdriver.Chrome()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888", login_way="ssh")
    MenubarPage(driver).click_nav_item("配置", "用户管理")
    UserPage(driver).create_department_from_Default("用户分组")
