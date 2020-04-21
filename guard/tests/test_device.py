# -*- coding:utf-8 -*-
# @Time: 2020/4/21 19:12
# @Author: wenqin_zhu
# @File: test_device.py
# @Software: PyCharm

import pytest
from guard.pages.device_page import DevicePage


@pytest.mark.positive
@pytest.mark.smoke
def test_create_peer_device_group_from_default(device):
    # 测试从Default分组创建同级地图分组
    DevicePage(device[0]).add_map_group_from_Default(device[1]["device_group_name"])

    assert True

