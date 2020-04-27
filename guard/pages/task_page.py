# -*- coding:utf-8 -*-
# @Time: 2020/4/20 17:59
# @Author: wenqin_zhu
# @File: task_page.py
# @Software: PyCharm

import time
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from guard.pages.classes.web_com_content_click import WebContentClick as click_btn


class TaskPage(BasePage):

    def click_left_menu(self, menu_name):
        """ 点击左侧任务菜单 """
        TASK_MENU = (By.XPATH, f'//div[@class="task-menu-container"]//li[contains(text(), "{menu_name}")]')
        BasePage(self.driver).click_ele(TASK_MENU)

    def add_task_to_parked_vehicle(self, task_name, device_name, time_minute, timezone_name=None, attr_name=None, menu_name="车辆-违停检测任务"):
        """
        添加车辆违停任务
        :param task_name: 任务名称
        :param device_name: 设备名称
        :param time_minute: 违停时长
        :param timezone_name: 时间条件名称
        :param attr_name: 特殊属性
        :param menu_name: 任务类型
        :return:
        """

        # 点击左侧菜单
        self.click_left_menu(menu_name)

        # 点击添加任务
        click_btn(self.driver).click_btn(btn_name="添加任务")

        # 基础配置
        # self.select_task_type()
        self.input_task_name(task_name)
        self.select_device(device_name)
        # self.select_timezone(timezone_name)
        # self.select_special_attr(attr_name)
        self.input_park_time(time_minute)
        self.draw_park_region()

    # 定位-任务类型
    def select_task_type(self):
        # 此处，采用的是先点击左侧对应的菜单，所以次数不需要下拉选择
        pass

    # 定位-任务名称
    def input_task_name(self, task_name):
        NAME = (By.XPATH, '//label[contains(text(), "任务名称")]/following-sibling::div//input')
        BasePage(self.driver).update_input_text(NAME, task_name)

    # 定位-设备，为指定设备绑定任务
    def select_device(self, device_name):
        DEVICE = (By.XPATH, '//label[contains(text(), "设备")]/following-sibling::div//div[contains(@class, "el-popover__reference")]//input')
        BasePage(self.driver).click_ele(DEVICE)

        # 通过设备名搜索设备并选择
        self.comm_search_result_by_name(device_name)

    # 定位-时间条件
    def select_timezone(self, timezone_name):
        """
        选择时间条件名
        :param timezone_name: 通过设置好的timezone名，选择对应的时间条件
        """
        TIMEZONE = (By.XPATH, '//label[contains(text(), "时间条件")]/following-sibling::div//input')
        BasePage(self.driver).click_ele(TIMEZONE)

        # 通过timezone的名称，定位时间条件
        SELECT_TIMEZONE = (By.XPATH, f'//span[text()="{timezone_name}"]')
        # 移动到时间条件上并进行选择时间条件
        BasePage(self.driver).mouse_move_ele_and_click(TIMEZONE, SELECT_TIMEZONE)

    # 定位-特殊属性
    def select_special_attr(self, attr_name):
        """  特殊属性支持多选：入口，出口，第三方对接 """
        SPECIAL_ATTR = (By.XPATH, '//label[contains(text(), "特殊属性")]/following-sibling::div//input')
        BasePage(self.driver).click_ele(SPECIAL_ATTR)

        # 通过指定特殊属性的名称，进行选择
        SELECT_TIMEZONE = (By.XPATH, f'//span[text()="{attr_name}"]')
        # 移动到特殊属性下拉列表上并进行选择
        BasePage(self.driver).mouse_move_ele_and_click(SPECIAL_ATTR, SELECT_TIMEZONE)

    # 定位-违停时限
    def input_park_time(self, time_minute=1):
        PARK_TIME = (By.XPATH, '//label[contains(text(), "违停时限")]/following-sibling::div//input')

        # 先清空输入框内的数值
        BasePage(self.driver).clear_input_default_val(PARK_TIME)

        # 再输入目标分钟数
        BasePage(self.driver).update_input_text(PARK_TIME, time_minute)

    # 定位-最小/最大车辆识别尺寸
    def com_car_size(self, text_name, width, height):
        SIZE_WIDTH = (By.XPATH, f'//label[contains(text(), "{text_name}")]/following-sibling::div//label[text()="宽"]/following-sibling::div//input')
        BasePage(self.driver).update_input_text(SIZE_WIDTH, width)
        SIZE_HEIGHT = (By.XPATH, f'//label[contains(text(), "{text_name}")]/following-sibling::div//label[text()="高"]/following-sibling::div//input')
        BasePage(self.driver).update_input_text(SIZE_HEIGHT, height)

    # 定位-最小车辆识别尺寸
    # def input_min_size(self, width=30, height=30):
    #     # 定位-宽
    #     MIN_SIZE_WIDTH = (By.XPATH, '//label[contains(text(), "最小车辆识别尺寸")]/following-sibling::div//input')
    #     BasePage(self.driver).update_input_text(MIN_SIZE_WIDTH, width)
    #
    #     # 定位-高
    #     MIN_SIZE_HEIGHT = (By.XPATH, '//label[contains(text(), "最小车辆识别尺寸")]/following-sibling::div//input')
    #     BasePage(self.driver).update_input_text(MIN_SIZE_HEIGHT, height)

    # 定位-最大车辆识别尺寸
    # def input_max_size(self, width=500, height=500):
    #     # 定位-宽
    #     MIN_SIZE_WIDTH = (By.XPATH, '//label[contains(text(), "最大车辆识别尺寸")]/following-sibling::div//input')
    #     BasePage(self.driver).update_input_text(MIN_SIZE_WIDTH, width)
    #
    #     # 定位-高
    #     MIN_SIZE_HEIGHT = (By.XPATH, '//label[contains(text(), "最大车辆识别尺寸")]/following-sibling::div//input')
    #     BasePage(self.driver).update_input_text(MIN_SIZE_HEIGHT, height)

    # 定位-绘制违停区域

    def draw_park_region(self):
        # 定位点击绘制区域的按钮
        REGION_BTN = (By.XPATH, '//i/parent::div[contains(text(), "点击绘制区域 ")]')
        BasePage(self.driver).click_ele(REGION_BTN)

        # 滚动到视频违停区域
        REGION = (By.XPATH, '//div[@class="addTaskPC-video"]')
        BasePage(self.driver).scroll_visibility_region(loc=REGION)

        time.sleep(3)

        # 绘制违停区域
        # PARK_REGION = (By.XPATH, '//canvas[@class="draw-line"]')
        PARK_REGION = (By.CSS_SELECTOR, '.draw-line')
        ele = BasePage(self.driver).get_ele_locator(PARK_REGION)
        # self.draw_line()

        # from selenium.webdriver.common.action_chains import ActionChains
        alarm_line = [(-100, -100), (100, -100), (100, 100), (-100, 100), (-100, -100)]
        # ActionChains(self.driver).move_to_element(ele).move_by_offset(xoffset=10, yoffset=-10).pause(3).click(ele).perform()
        # ActionChains(self.driver).move_to_element(ele).move_by_offset(xoffset=100, yoffset=-10).pause(3).click(ele).perform()
        # ActionChains(self.driver).move_to_element(ele).move_by_offset(xoffset=100, yoffset=-100).pause(3).click(ele).perform()
        # ActionChains(self.driver).move_to_element(ele).move_by_offset(xoffset=10, yoffset=--100).pause(3).click(ele).perform()
        # actions = ActionChains(self.driver)
        for point in alarm_line:
            self.mouse_ele_and_set_offset(ele, point[0], point[1])
            # actions.move_to_element(ele).pause(2).perform()
            # actions.move_by_offset(xoffset=point[0], yoffset=point[1]).pause(3).perform()
            # actions.click(ele).perform()

        # 点击确定
        CONFIRM_BTN = (By.XPATH, '//div[@aria-label="添加任务"]//div[@class="el-dialog__footer"]//span[contains(text(), "确定")]')
        BasePage(self.driver).click_ele(CONFIRM_BTN)


    def mouse_ele_and_set_offset(self, ele, x_offset, y_offset):
        """ 进行区域绘制 """
        from selenium.webdriver.common.action_chains import ActionChains
        actions = ActionChains(self.driver)
        actions.move_to_element(ele)
        actions.perform()
        # time.sleep(1)
        actions.pause(1)
        actions.move_by_offset(x_offset, y_offset)
        actions.perform()
        # time.sleep(1)
        actions.pause(1)
        actions.click()
        actions.perform()


    """ ---------------------------- 页面共用封装方法 ---------------------------- """
    def comm_search_result_by_name(self, name):
        """  任务下拉列表搜索 """
        # 1、通过设备名device_name,查找设备
        SELECT_GROUP = (By.XPATH,
                        '//div[@role="tooltip" and contains(@style, "position")]//div[contains(@class, "el-input")]//input')
        BasePage(self.driver).update_input_text(SELECT_GROUP, name)

        # 2、通过设备名device_name, 定位到查询结果
        RESULT = (By.XPATH, f'//span[@class="el-radio__label"]//span[@title="{name}"]')
        # 点击到查询的设备分组名
        BasePage(self.driver).click_ele(RESULT)


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.login_page import LoginPage
    from guard.pages.components.menubar import MenubarPage

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888", login_way="debug")
    MenubarPage(driver).click_nav_item("配置", "任务管理")
    TaskPage(driver).add_task_to_parked_vehicle(task_name="test", device_name="ddd", time_minute=1)
