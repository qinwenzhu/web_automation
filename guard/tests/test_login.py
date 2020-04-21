# -*- coding:utf-8 -*-
# @Time: 2020/3/17 10:05
# @Author: wenqin_zhu
# @File: test_login.py
# @Software: PyCharm


import pytest
from guard.pages.login import LoginPage
from guard.datas.login_data import LoginData
from guard.pages.classes.web_global_info import GlobalDialogInfo


@pytest.mark.positive
@pytest.mark.smoke
def test_login_success(setup_login):
    # 登录成功校验
    LoginPage(setup_login).login(*LoginData.success_login_data, login_way="ssh")

    # 断言 - 只要判断首页的某个指定元素存在，说明登录成功并进行页面跳转
    assert LoginPage(setup_login).is_login_success()


@pytest.mark.negative
@pytest.mark.parametrize("data", LoginData.negative_login_data)
def test_login_fail(setup_login, data):
    # 用户名和密码的非空校验
    LoginPage(setup_login).login(data["username"], data["password"], code=data["code"], login_way="ssh")

    result = LoginPage(setup_login).get_error_info()
    assert data["error_info"] in result


@pytest.mark.negative
def test_code_error(setup_login):
    # 测试验证码错误 - 前端提示信息
    LoginPage(setup_login).login(*LoginData.success_login_data, code="123456", login_way="ssh")

    result = GlobalDialogInfo(setup_login).judge_alert_info()
    assert "验证码错误" in result


@pytest.mark.negative
@pytest.mark.parametrize("data", LoginData.negative_password_data)
def test_code_error(setup_login, data):
    # 测试验证码错误 - 前端提示信息
    LoginPage(setup_login).login(data["username"], data["password"], login_way="ssh")

    result = GlobalDialogInfo(setup_login).judge_alert_info()
    assert data["error_info"] in result


if __name__ == '__main__':
    pytest.main()
