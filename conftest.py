# -*- coding:utf-8 -*-
# @Time: 2020/3/25 11:26
# @Author: wenqin_zhu
# @File: conftest.py
# @Software: PyCharm

import time
import uuid
import random

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from guard.pages.classes.basepage import BasePage
from guard.pages.map_page import MapPage
from guard.pages.tool_page import ToolPage
from guard.pages.user_page import UserPage
from guard.pages.task_page import TaskPage
from guard.pages.login_page import LoginPage
from guard.pages.device_page import DevicePage
from guard.pages.timezone_page import TimezonePage
from guard.pages.components.menubar import MenubarPage
from guard.pages.components.group_tree import GroupTreePage

from guard.pages.classes.custom_share_path import SharePath
from guard.pages.classes.web_global_dialog import GlobalDialog
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


""" ---------------------------- 启动/关闭 WebDriver服务 ---------------------------- """
@pytest.fixture(scope="module")
def start_driver_and_quit():
    # 前置 - 启动会话窗口 后置 - 关闭
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


""" ---------------------------- 系统登录 ---------------------------- """
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


""" ---------------------------- 配置-任务管理 ---------------------------- """
@pytest.fixture(scope="module")
def task(login):
    before_name = {"map_group_name": f"MGN-{uuid4_data()}", "device_group_name": f"DGN-{uuid4_data()}",
                   "device_name": f"dname-{get_current_time()}", "device_id": f"id-{get_current_time()}",
                   "task_name": f"tname-{get_current_time()}", "time_minute": integer_num()}
    MenubarPage(login).click_nav_item("配置", "地图管理")
    GroupTreePage(login).create_peer_or_next_group(group_name=before_name["map_group_name"], parent_name="Default")
    MapPage(login).upload_map(file_name=r"{}/map_data/company_4th_floor.jpg".format(SharePath.DATA_FOLDER), group_name=before_name["map_group_name"])
    # 进入设备模块，创建设备分组，不同设备类型的设备
    time.sleep(2)
    MenubarPage(login).click_nav_item("配置", "设备管理")
    time.sleep(2)
    GroupTreePage(login).create_peer_or_next_group(group_name=before_name["device_group_name"], parent_name="Default")
    # 添加设备类型为：网络摄像机、相机类型为：RTSP 的设备
    time.sleep(2)
    DevicePage(login).add_camera(device_type="网络摄像机", device_name=before_name["device_name"], device_id=before_name["device_id"],
                                device_group_name=before_name["device_group_name"], map_group_name=before_name["map_group_name"],
                                rtsp_address="rtsp://10.151.3.119:7554/IMG_0322.264", camera_type="RTSP")
    time.sleep(2)
    MenubarPage(login).click_nav_item("配置", "任务管理")
    yield login, before_name
    # 进入实况，搜索设备，查看推送
    # MenubarPage(login).click_nav_item("实况")

    # 删除任务
    # 删除设备分组
    # MenubarPage(login).click_nav_item("配置", "设备管理")
    # GroupTreePage(login).delete_peer_or_next_group_by_name(parent_name=before_name["device_group_name"], module_val="device")
    # # 删除地图分组
    # MenubarPage(login).click_nav_item("配置", "地图管理")
    # GroupTreePage(login).delete_peer_or_next_group_by_name(parent_name=before_name["map_group_name"], module_val="map")


@pytest.fixture(scope="module")
def task_no_setup(login):
    MenubarPage(login).click_nav_item("配置", "任务管理")
    yield login
    TaskPage(login).click_close_dialog_btn()


""" ---------------------------- 配置-设备管理 ---------------------------- """
@pytest.fixture(scope="module")
def device(login):
    before_name = {"map_group_name": f"MGN-{uuid4_data()}", "device_group_name": f"DGN-{uuid4_data()}",
                   "device_name": f"name-{uuid4_data()}", "device_id": f"id-{uuid4_data()}"}
    # 进入地图模块，创建地图分组，上传地图
    MenubarPage(login).click_nav_item("配置", "地图管理")
    GroupTreePage(login).create_peer_or_next_group(group_name=before_name["map_group_name"], parent_name="Default")
    MapPage(login).upload_map(file_name=r"{}/map_data/company_4th_floor.jpg".format(SharePath.DATA_FOLDER), group_name=before_name["map_group_name"])
    MenubarPage(login).click_nav_item("配置", "设备管理")
    yield login, before_name
    # 删除设备
    # 删除设备分组
    GroupTreePage(login).delete_peer_or_next_group_by_name(parent_name=before_name["device_group_name"], module_val="device")
    # 删除地图分组
    MenubarPage(login).click_nav_item("配置", "地图管理")
    GroupTreePage(login).delete_peer_or_next_group_by_name(parent_name=before_name["map_group_name"], module_val="map")


""" ---------------------------- 配置-地图管理 ---------------------------- """
@pytest.fixture(scope="module")
def map_module(login):
    # 进入地图管理模块
    MenubarPage(login).click_nav_item("配置", "地图管理")
    before_name = {"map_group_name": f"FGN-{uuid4_data()}"}
    yield login, before_name
    GroupTreePage(login).delete_peer_or_next_group_by_name(parent_name=before_name["map_group_name"], module_val="map")


@pytest.fixture
def del_sub_map_group_to_default(map_module, sole_group_name):
    yield
    # 删除Default分组的下一级分组，只有当Default下没有该元素的时候，才说明下一级地图分组创建成功，才进行后置删除操作
    if not MapPage(map_module[0]).judge_upload_map_success():
        GroupTreePage(map_module[0]).delete_peer_or_next_group_by_name(group_name=sole_group_name, parent_name="Default", module_val="map", is_peer=False)


@pytest.fixture
def close_next_map_group_tree_dialog(login):
    # 关闭左侧树图弹框 - 当创建已经存在地图分组的下一级组
    yield
    GlobalDialog(login).close_dialog_btn("创建下一级")


""" ---------------------------- 配置-时间条件 ---------------------------- """
@pytest.fixture(scope="module")
def timezone(login):
    # 进入时间条件模块
    MenubarPage(login).click_nav_item("配置", "时间条件")
    before_name = {"timezone": f"TIME-{get_current_time()}",
                   "holiday_name": f"H-{get_current_time()}",
                   "workday_name": f"W-{get_current_time()}"}
    yield login, before_name
    # 如果创建成功，进行后置数据的处理
    if TimezonePage(login).assert_result_by_name(before_name["timezone"]):
        TimezonePage(login).delete_or_rename_timezone_name(before_name["timezone"])
    if TimezonePage(login).assert_result_by_name(before_name["holiday_name"]):
        TimezonePage(login).delete_or_rename_holidays_or_workday(before_name["holiday_name"])
    if TimezonePage(login).assert_result_by_name(before_name["workday_name"]):
        TimezonePage(login).delete_or_rename_holidays_or_workday(before_name["workday_name"])


@pytest.fixture
def overlong_name():
    # 创建超出时间条件命名长度的名称
    sole_name = f"ABD-{uuid4_data()}"
    yield sole_name


""" ---------------------------- 配置-用户管理 ---------------------------- """
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
def del_sub_dep_name_to_default(user, sole_group_name):
    yield
    # 删除Default分组的下一级分组
    GroupTreePage(user[0]).delete_peer_or_next_group_by_name(group_name=sole_group_name, module_val="user", is_peer=False)
    time.sleep(2)


@pytest.fixture
def del_dep_name_to_user(user, sole_group_name):
    yield
    # 删除用户自定义分组的同级分组
    GroupTreePage(user[0]).delete_peer_or_next_group_by_name(parent_name=sole_group_name, module_val="user")
    time.sleep(2)


@pytest.fixture
def del_sub_dep_name_to_user(user, sole_group_name):
    yield
    # 删除用户自定义分组的下一级分组
    time.sleep(10)
    GroupTreePage(user[0]).delete_peer_or_next_group_by_name(group_name=sole_group_name, parent_name=user[1], module_val="user", is_peer=False)
    time.sleep(2)


""" ---------------------------- 工具 ---------------------------- """
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


""" ---------------------------- 登录模块 ---------------------------- """
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


def integer_num():
    # 生成指定范围内的整数
    return random.randint(1, 60)


@pytest.fixture
def sole_group_name():
    sole_name = f"UNIQUE-{uuid4_data()}"
    yield sole_name
