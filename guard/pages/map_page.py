# -*- coding:utf-8 -*-
# @Time: 2020/4/20 17:59
# @Author: wenqin_zhu
# @File: map_page.py
# @Software: PyCharm

from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from guard.pages.components.group_tree import GroupTreePage


class MapPage(BasePage):

    def add_map_group_from_Default(self, group_name, is_peer=True):
        """
        从Default分组创建同级地图分组
        :param group_name: 地图分组名称
        :param is_peer: 判断是否创建同级/下一级分组，默认创建同级分组
        """
        if is_peer:
            # 滑动到创建同级分组
            GroupTreePage(self.driver).click_menu_by_name("Default", "创建同级")
            # 动态定位title 为 创建同级
            GroupTreePage(self.driver).create_dep_group_com(group_name, "创建同级")
        else:
            # 滑动到创建下一级分组
            GroupTreePage(self.driver).click_menu_by_name("Default", "创建下一级")
            # 动态定位title 为 创建下一级
            GroupTreePage(self.driver).create_dep_group_com(group_name, "创建下一级")

    def upload_map(self, file_name):
        """ 地图上传 """
        # 定位上传按钮
        UPLOAD_BTN = (By.XPATH, '//input[@class="el-upload__input"]')
        # 地图上传
        BasePage(self.driver).upload_file(loc=UPLOAD_BTN, filename=file_name)


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.login_page import LoginPage
    from guard.pages.components.menubar import MenubarPage
    driver = webdriver.Chrome()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888")
    MenubarPage(driver).click_nav_item("配置", "地图管理")
