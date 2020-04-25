# -*- coding:utf-8 -*-
# @Time: 2020/4/21 16:30
# @Author: wenqin_zhu
# @File: test_map.py
# @Software: PyCharm

import time
import pytest
from guard.pages.map_page import MapPage
from guard.pages.components.group_tree import GroupTreePage
from guard.pages.classes.web_global_info import GlobalDialogInfo

from guard.pages.classes.custom_share_path import SharePath


@pytest.mark.positive
@pytest.mark.smoke
def test_create_peer_map_group_from_default(map_module):
    # 测试从Default分组创建同级地图分组
    GroupTreePage(map_module[0]).create_peer_or_next_group(group_name=map_module[1]["map_group_name"])

    result = GlobalDialogInfo(map_module[0]).judge_alert_info()
    assert "创建同级分组成功" == result


@pytest.mark.positive
@pytest.mark.smoke
def test_upload_map(map_module):
    # 测试在指定地图分组中上传地图

    # 上传地图
    MapPage(map_module[0]).upload_map(r"{}/map_data/company_4th_floor.jpg".format(SharePath.DATA_FOLDER), group_name=map_module[1]["map_group_name"])

    assert MapPage(map_module[0]).judge_upload_map_success()
