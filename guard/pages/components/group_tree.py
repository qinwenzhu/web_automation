# -*- coding:utf-8 -*-
# @Time: 2020/3/30 19:15
# @Author: wenqin_zhu
# @File: group_tree.py
# @Software: PyCharm


from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage


class GroupTreePage(BasePage):

    def click_group_by_name(self, department_name):
        """ 点击左侧树图分组 """

        # 部门分组名称
        DEPARTMENT_NAME = (By.XPATH, f'//div[@title="{department_name}"]')
        BasePage(self.driver).click_ele(DEPARTMENT_NAME)

    def click_menu_by_name(self, department_name, menu_name):
        """ 滑动到左侧树图右侧icon - 出现列表项 """

        # 部门分组右侧icon
        GROUP_ICON = (By.XPATH, f'//div[@title="{department_name}"]/parent::div/following-sibling::div[contains(text(), "︙")]')
        BasePage(self.driver).mouse_move_ele(GROUP_ICON)

        # 通过传入不同的 menu_name 滑动到不同的操作
        GROUP_MENU_NAME = (By.XPATH, f'//div[@id="menu"]//li[@class="menu" and contains(text(), "{menu_name}")]')
        BasePage(self.driver).mouse_move_ele_and_click(GROUP_ICON, GROUP_MENU_NAME, img_describe="左侧组件-tree")

    def create_dep_group_com(self, group_name, loc_by_til_name, confirm=True):
        """
        创建 同级/下一级 分组
        :param group_name: 部门组名称
        :param loc_by_til_name: 通过dialog弹框的标题定位唯一元素
        :param confirm: 判断是点击确定还是点击取消按钮 True默认创建点击确定按钮
        """

        # 组名称input框
        GROUP_INPUT = (By.XPATH, f'//span[contains(text(),"{loc_by_til_name}")]/parent::div/following-sibling::div[@class="el-dialog__body"]//input')
        BasePage(self.driver).update_input_text(GROUP_INPUT, group_name)
        if confirm:
            # 点击确认按钮
            CONFIRM_BTN = (By.XPATH, f'//span[contains(text(),"{loc_by_til_name}")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"确定")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)
        else:
            # 点击取消按钮
            CONFIRM_BTN = (By.XPATH, f'//span[contains(text(),"{loc_by_til_name}")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"取消")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)

    def delete_dep_group_com(self, delete=True):
        # 删除分组

        if delete:
            # 点击删除按钮
            CONFIRM_BTN = (By.XPATH, '//span[contains(text(),"删除")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"删除")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)
        else:
            # 点击取消按钮
            CONFIRM_BTN = (By.XPATH,
                           '//span[contains(text(),"删除")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"取消")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)

    def search_dep_by_name(self, group_name):

        # 定位搜索文本框
        SEARCH_INPUT = (By.XPATH, '//aside[@class="el-aside"]//div[contains(@class,"el-input--suffix")]/input')
        BasePage(self.driver).update_input_text(SEARCH_INPUT, group_name)

        # 点击搜索
        SEARCH_BTN = (By.XPATH, '//aside[@class="el-aside"]//div[contains(@class,"el-input--suffix")]/span')
        BasePage(self.driver).click_ele(SEARCH_BTN)

    def judge_search_success(self, group_name):
        # 判断 tree分组下搜索到对应的分组
        RESULT_TEXT = (By.XPATH, f'//div[@role="tree"]//div[contains(@title,"{group_name}")]')
        return BasePage(self.driver).get_text(RESULT_TEXT)
