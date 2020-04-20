# -*- coding:utf-8 -*-
# @Time: 2020/4/13 14:19
# @Author: wenqin_zhu
# @File: test_timezone.py
# @Software: PyCharm

import re
import time
import pytest
from guard.pages.timezone import TimezonePage
from guard.pages.classes.web_global_info import GlobalDialogInfo


@pytest.mark.positive
def test_add_timezone(connect_mysql_and_close, timezone):
    # 测试添加时间条件
    TimezonePage(timezone[0]).add_timezone(timezone[1]["timezone"])

    # 断言
    sql = "SELECT * FROM senseguard.info_time_zone WHERE time_zone_name=%s;"
    time.sleep(2)
    result = connect_mysql_and_close.select_database(sql, args=(timezone[1]["timezone"], ))
    print(f"数据库查询结果为：{result}")
    assert timezone[1]["timezone"] == result["time_zone_name"]


@pytest.mark.positive
def test_add_timezone_section(timezone):
    # 通过选择 指定的时间条件名称 创建时间段
    TimezonePage(timezone[0]).add_timezone_section_by_timezone_name(timezone[1]["timezone"])

    # 断言
    result = TimezonePage(timezone[0]).assert_timezone_section()
    assert re.match(r'\d+:\d+-\d+:\d', result)


@pytest.mark.positive
def test_create_holidays(connect_mysql_and_close, timezone):
    # 测试添加假期
    TimezonePage(timezone[0]).create_holidays("添加假期", timezone[1]["holiday_name"], num=1)

    # 断言
    sql = "SELECT * FROM senseguard.info_holiday WHERE holiday_name=%s;"
    time.sleep(2)
    result = connect_mysql_and_close.select_database(sql, args=(timezone[1]["holiday_name"], ))
    print(f"数据库查询结果为：{result}")
    assert timezone[1]["holiday_name"] == result["holiday_name"]


@pytest.mark.positive
def test_create_workday(connect_mysql_and_close, timezone):
    # 测试添加特殊工作日
    TimezonePage(timezone[0]).create_workday("添加特殊工作日", timezone[1]["workday_name"], num=1)

    # 断言
    sql = "SELECT * FROM senseguard.info_holiday WHERE holiday_name=%s;"
    time.sleep(2)
    result = connect_mysql_and_close.select_database(sql, args=(timezone[1]["workday_name"], ))
    print(f"数据库查询结果为：{result}")
    assert timezone[1]["workday_name"] == result["holiday_name"]


@pytest.mark.negative
def test_add_timezone_and_beyond(timezone, overlong_name):
    # 测试添加事件条件的超出指定字符长度
    TimezonePage(timezone[0]).add_timezone(overlong_name)

    # 断言
    result = GlobalDialogInfo(timezone[0]).judge_alert_info()
    assert "请输入最多40个字符的时间条件名称" == result


@pytest.mark.negative
def test_add_holidays_negative_conflict(timezone, overlong_name):
    # 测试添加假期与页面现有的假期时间冲突
    TimezonePage(timezone[0]).create_holidays("添加假期", overlong_name)

    # 断言
    result = GlobalDialogInfo(timezone[0]).judge_alert_info()
    assert "创建的假期与已有的假期有冲突，请检查后重新设置" == result


@pytest.mark.negative
def test_add_workday_negative_conflict(timezone, overlong_name):
    # 测试添加特殊工作日与页面现有的工作日时间冲突
    TimezonePage(timezone[0]).create_workday("添加特殊工作日", overlong_name)

    # 断言
    result = GlobalDialogInfo(timezone[0]).judge_alert_info()
    assert "创建的特殊工作日与已有的特殊工作日有冲突，请检查后重新设置" == result
