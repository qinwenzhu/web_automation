# -*- coding: utf-8 -*-
# @time: 2020/4/19 13:11 
# @Author: wenqinzhu
# @Email: zhuwenqin_vendor@sensetime.com
# @file: web_global_dialog.py
# @software: PyCharm

from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage


class GlobalDialog(BasePage):
    """ 封装类：系统dialog弹框操作 """

    """ 通用：系统页面删除dialog """

    def dialog_delete(self, is_delete=True):

        if is_delete:
            # 点击删除按钮
            CONFIRM_BTN = (By.XPATH, '//button//span[contains(text(), "删除")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)
        else:
            # 点击取消按钮
            CONFIRM_BTN = (By.XPATH, '//button//span[contains(text(), "取消")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)
