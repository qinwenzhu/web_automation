# -*- coding:utf-8 -*-
# @Time: 2020/3/16 11:21
# @Author: wenqin_zhu
# @File: menubar.py
# @Software: PyCharm

from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage


class MenubarPage(BasePage):

    def click_nav_item(self, menu_text, sub_menu_text=None):
        """
        封装导航栏组件：传入的参数是一级还是二级导航
        :param menu_text: 菜单文本<导航文本的唯一性>
        :param sub_menu_text: 子菜单文本
        :return:
        """

        if menu_text == "工具":
            MENU_TEXT = (By.XPATH, f'//div[text()="{menu_text}"]')
            SUB_MENU_TEXT = (By.XPATH, f'//li[text()="{sub_menu_text}"]')
        else:
            MENU_TEXT = (By.XPATH, f'//em[text()="{menu_text}"]')
            SUB_MENU_TEXT = (By.XPATH, f'//em[text()="{sub_menu_text}"]')

        if sub_menu_text is not None:
            # 通过移动到一级目录然后点击二级目录
            BasePage(self.driver).mouse_move_ele(MENU_TEXT, "顶部导航组件-nav")
            BasePage(self.driver).mouse_move_ele_and_click(MENU_TEXT, SUB_MENU_TEXT, img_describe="顶部导航组件-nav")
        else:
            # 选择指定的一级目录
            BasePage(self.driver).click_ele(MENU_TEXT, "顶部导航组件-nav")


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.login import LoginPage
    import time
    driver = webdriver.Chrome()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888", login_way="ssh")
    # 测试点击存在二级导航的
    MenubarPage(driver).click_nav_item("工具", "人脸属性检测")
    time.sleep(4)
    # 测试点击只存在一级导航
    MenubarPage(driver).click_nav_item("看板")
    time.sleep(2)
    driver.quit()
