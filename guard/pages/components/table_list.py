# -*- coding:utf-8 -*-
# @Time: 2020/4/28 14:12
# @Author: wenqin_zhu
# @File: table_list.py
# @Software: PyCharm

from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from guard.pages.classes.web_global_dialog import GlobalDialog


class TableListPage(BasePage):

    def judge_table_list_name(self, name):
        """ 判断table列表内的名称 """
        TABLE_NAME = (By.XPATH, f'//table[@class="el-table__body"]//div[@class="cell" and  text() = "{name}"]')
        if BasePage(self.driver).get_ele_locator(TABLE_NAME):
            return True
        else:
            return False

    def operations_table_list(self, name, flag):
        """ 定位列表项的相关操作，有：查看、编辑、删除 """
        # 定位查看icon
        VIEW_ICON = (By.XPATH, f'//table[@class="el-table__body"]//div[@class="cell" and  text() = "{name}"]/parent::td/following-sibling::td[contains(@class, "tables-operate")]//i[contains(@class, "icon-view")]')
        # 定位编辑icon
        EDIT_ICON = (By.XPATH, f'//table[@class="el-table__body"]//div[@class="cell" and  text() = "{name}"]/parent::td/following-sibling::td[contains(@class, "tables-operate")]//i[contains(@class, "icon-edit")]')
        # 定位删除icon
        DELETE_ICON = (By.XPATH, f'//table[@class="el-table__body"]//div[@class="cell" and  text() = "{name}"]/parent::td/following-sibling::td[contains(@class, "tables-operate")]//i[contains(@class, "icon-delete")]')

        # 点击查看、 编辑、删除icon
        if flag == "view":
            BasePage(self.driver).click_ele(VIEW_ICON)

            # TODO 弹框操作
            pass

        elif flag == "edit":
            BasePage(self.driver).click_ele(EDIT_ICON)

            # TODO 弹框操作
            pass

        elif flag == "delete":
            BasePage(self.driver).click_ele(DELETE_ICON)
            # 进行弹框删除操作
            self.table_list_delete()

    def table_list_delete(self, is_delete=True):
        """  table_list 删除操作 """
        if is_delete:
            # 点击删除按钮
            CONFIRM_BTN = (By.XPATH, '//button//span[text()="删除"]')
            ele = BasePage(self.driver).get_ele_locator_by_index(CONFIRM_BTN, 2)
            ele.click()
        else:
            # 点击取消按钮
            CONFIRM_BTN = (By.XPATH, '//button//span[text()="取消"]')
            ele = BasePage(self.driver).get_ele_locator_by_index(CONFIRM_BTN, 2)
            ele.click()

