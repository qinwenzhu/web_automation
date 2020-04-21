# -*- coding:utf-8 -*-
# @Time: 2020/4/20 17:59
# @Author: wenqin_zhu
# @File: device_page.py
# @Software: PyCharm

from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from guard.pages.components.group_tree import GroupTreePage


class DevicePage(BasePage):

    # 定位-设备类型
    def input_device_type(self, type_val):
        NAME = (By.XPATH, '//label[contains(text(), "设备类型")]/following-sibling::div//input')
        BasePage(self.driver).update_input_text(NAME, type_val)

    # 定位-名称
    def input_device_name(self, name):
        NAME = (By.XPATH, '//label[@for="name"]/following-sibling::div//input')
        BasePage(self.driver).update_input_text(NAME, name)

    # 定位-ID
    def input_device_id(self, id):
        ID = (By.XPATH, '//label[@for="ID"]/following-sibling::div//input')
        BasePage(self.driver).update_input_text(ID, id)

    # 定位-分组
    def input_device_group(self, group_val):
        ID = (By.XPATH, '//label[contains(text(), "分组")]/following-sibling::div//input')
        BasePage(self.driver).update_input_text(ID, group_val)

    # 定位-地点
    def input_device_site(self, site):
        ID = (By.XPATH, '//label[contains(text(), "分组")]/following-sibling::div//input')
        BasePage(self.driver).update_input_text(ID, site)

    # 定位-分配用户：设备分配给用户权限
    def input_device_assign_to_user_roles(self, site):
        ID = (By.XPATH, '//label[contains(text(), "分配用户")]/following-sibling::div//input')
        BasePage(self.driver).update_input_text(ID, site)

    # 定位-类型<RTSP/ONVIF>
    def select_camera_type(self, type="RTSP"):
        ID = (By.XPATH, f'//div[@class="el-form-item__content"]//span[contains(text(), "{type}")]')
        BasePage(self.driver).update_input_text(ID, type)

    # 定位-RTSP地址

    # 定位-编码类型<直连/转码>
    def select_encoding_type(self, default_type="直连"):
        ID = (By.XPATH, f'//div[@class="el-form-item__content"]//span[contains(text(), "{default_type}")]')
        BasePage(self.driver).update_input_text(ID, type)

    # 定位-传输协议<TCP/UDP>
    def select_transport_protocols(self, default_type="TCP"):
        ID = (By.XPATH, f'//div[@class="el-form-item__content"]//span[contains(text(), "{default_type}")]')
        BasePage(self.driver).update_input_text(ID, type)

    # 定位-将该设备关联门禁开关
    # 定位-确定按钮
    # 定位-取消按钮

    def select_device_type(self):
        # 选择设备类型
        pass

    def add_device_and_type_is_camera(self):
        """ 添加设备类型为 摄像头 的设备 """
        pass

    def add_map_group_from_Default(self, device_name, is_peer=True):
        """
        从Default分组创建同级设备分组
        :param device_name: 设备分组名称
        :param is_peer: 判断是否创建同级/下一级分组，默认创建同级分组
        """
        if is_peer:
            # 滑动到创建同级分组
            GroupTreePage(self.driver).click_menu_by_name("Default", "创建同级")
            # 动态定位title 为 创建同级
            GroupTreePage(self.driver).create_dep_group_com(device_name, "创建同级")
        else:
            # 滑动到创建下一级分组
            GroupTreePage(self.driver).click_menu_by_name("Default", "创建下一级")
            # 动态定位title 为 创建下一级
            GroupTreePage(self.driver).create_dep_group_com(device_name, "创建下一级")


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.login_page import LoginPage
    from guard.pages.components.menubar import MenubarPage

    driver = webdriver.Chrome()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888")
    MenubarPage(driver).click_nav_item("配置", "设备管理")
