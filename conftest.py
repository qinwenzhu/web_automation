# -*- coding:utf-8 -*-
# @Time: 2020/3/25 11:26
# @Author: wenqin_zhu
# @File: conftest.py
# @Software: PyCharm

import time
import uuid

import pytest
from selenium import webdriver

from guard.pages.login import LoginPage
from guard.pages.components.menubar import MenubarPage
from guard.pages.tool import ToolPage
from guard.pages.timezone import TimezonePage
from guard.pages.user import UserPage

from guard.pages.classes.custom_share_path import SharePath
from guard.pages.classes.web_global_info import GlobalDialogInfo

from utils.handle_config import HandleConfig
from utils.handle_database import HandleDB
# 获取当前的运行的测试环境
from guard.pages.classes.get_run_env import env


""" ---------------------------- 连接数据库 ---------------------------- """
@pytest.fixture(scope="session")
def connect_mysql_and_close():
    # 前置 - 连接数据库 后置 - 关闭连接

    # 读取数据库配置文件中的配置信息
    DB_CONFIG = HandleConfig(r'{}\db_config.yml'.format(SharePath.CONFIG_FOLDER)).config
    db_config = DB_CONFIG.get("database")
    # 通过读取配置文件获取到当前运行环境的ip
    db_config['hostname'] = env()["host"]       # db_config['host'] = "10.151.3.96"
    # 连接数据库
    database = HandleDB(host=db_config['hostname'],
                        username=db_config['user'],
                        password=db_config['password'],
                        port=db_config['port'],
                        database=db_config["database"])
    print("数据库连接成功！")
    yield database
    # 关闭游标、关闭数据库
    database.close()


""" ---------------------------- 启动/关闭 webdriver服务 ---------------------------- """
@pytest.fixture(scope="module")
def start_driver_and_quit():
    # 前置 - 启动会话窗口 后置 - 关闭
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


""" ---------------------------- 网页的模块登陆 ---------------------------- """
@pytest.fixture(scope="module")
def login(start_driver_and_quit):
    # 成功登录网站
    # 优化：动态传入测试环境  start_driver_and_quit.get("http://10.151.3.96/login")
    start_driver_and_quit.get(f'http://{env()["host"]}/login')
    # 优化：动态传入登陆用户  LoginPage(start_driver_and_quit).login("zhuwenqin", "888888")
    # LoginPage(start_driver_and_quit).login(f'{env()["username"]}',
    #                                        f'{env()["password"]}',
    #                                        login_way=env()["login_way"])
    LoginPage(start_driver_and_quit).login(f'{env()["username"]}',
                                           f'{env()["password"]}')
    yield start_driver_and_quit


""" ---------------------------- 时间条件 timezone ---------------------------- """
@pytest.fixture(scope="module")
def timezone(login):
    # 进入时间条件模块
    MenubarPage(login).click_nav_item("配置", "时间条件")
    class_timezone_name = f"TIME-{get_current_time()}"
    class_holiday_name = f"H-{get_current_time()}"
    class_workday_name = f"W-{get_current_time()}"
    yield login, class_timezone_name, class_holiday_name, class_workday_name
    TimezonePage(login).delete_or_rename_timezone_name(class_timezone_name)
    TimezonePage(login).delete_or_rename_holidays_or_workday(class_holiday_name)
    TimezonePage(login).delete_or_rename_holidays_or_workday(class_workday_name)


@pytest.fixture
def overlong_name():
    # 创建超出时间条件命名长度的名称
    sole_name = f"ABD-{uuid4_data()}"
    yield sole_name


""" ---------------------------- 用户管理 user ---------------------------- """
@pytest.fixture(scope="module")
def user(login):
    # 进入用户管理模块
    MenubarPage(login).click_nav_item("配置", "用户管理")
    sole_name = f"UDN-{uuid4_data()}"
    yield login, sole_name


@pytest.fixture
def close_alert(user):
    # 删除alert消息弹框
    yield
    GlobalDialogInfo(user[0]).close_alert()


@pytest.fixture
def sole_group_name():
    # 分组名称 - 数据唯一性
    sole_name = f"UDN-{uuid4_data()}"
    yield sole_name


@pytest.fixture
def del_sub_dep_name_to_default(user, sole_group_name):
    yield
    # 删除Default分组的下一级分组
    UserPage(user[0]).delete_department_by_name(sub_name=sole_group_name, is_peer=False)
    time.sleep(2)


@pytest.fixture
def del_dep_name_to_user(user, sole_group_name):
    yield
    # 删除用户自定义分组
    UserPage(user[0]).delete_department_by_name(parent_name=sole_group_name)
    time.sleep(2)


@pytest.fixture
def del_sub_dep_name_to_user(user, sole_group_name):
    yield
    # 删除用户自定义分组的下一级分组
    UserPage(user[0]).delete_department_by_name(sub_name=sole_group_name, parent_name=user[1], is_peer=False)
    time.sleep(2)


""" ---------------------------- 工具 tool ---------------------------- """
@pytest.fixture(scope="function")
def tool_close_one_to_one_face_compare(login):
    # 后置：关闭当前窗口 - 1:1人脸验证
    yield
    ToolPage(login).close_tool_current_win("tools-face-verification")


@pytest.fixture
def tool_close_one_img_quality(login):
    # 后置：关闭当前窗口 - 质量分数检测
    yield
    ToolPage(login).close_tool_current_win("tools-score-detection")


@pytest.fixture
def tool_close_face_score_detection(login):
    # 后置：关闭当前窗口 - 人脸属性检测
    yield
    ToolPage(login).close_tool_current_win("tools-test-detection")


""" ---------------------------- 登录 login ---------------------------- """
@pytest.fixture
def setup_login():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(f'http://{env()["host"]}/login')          # start_driver_and_quit.get("http://10.151.3.96/login")
    yield driver
    driver.quit()


""" ---------------------------- 封装公用方法/常用方法 ---------------------------- """


def get_current_time():
    # 获取当前系统时间时间
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


def uuid4_data():
    # 生成随机数据
    return str(uuid.uuid4())
