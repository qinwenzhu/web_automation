# -*- coding:utf-8 -*-
# @Time: 2020/4/21 19:12
# @Author: wenqin_zhu
# @File: test_device.py
# @Software: PyCharm

import pytest
from guard.pages.device_page import DevicePage
from guard.pages.components.group_tree import GroupTreePage

from guard.pages.classes.web_global_info import GlobalDialogInfo


@pytest.mark.smoke
@pytest.mark.positive
class TestDevicePositive:

    def test_create_peer_device_group_from_default(self, device):
        # 测试从Default分组创建同级地图分组
        GroupTreePage(device[0]).create_peer_or_next_group(device[1]["device_group_name"])

        result = GlobalDialogInfo(device[0]).judge_alert_info()
        assert "创建同级分组成功" == result

