# -*- coding:utf-8 -*-
# @Time: 2020/4/21 16:30
# @Author: wenqin_zhu
# @File: test_map.py
# @Software: PyCharm
import time

import pytest
from guard.pages.components.group_tree import GroupTreePage
from guard.pages.map_page import MapPage

from guard.pages.classes.custom_share_path import SharePath


@pytest.mark.positive
@pytest.mark.smoke
def test_create_peer_map_group_from_default(map_module):
    # 测试从Default分组创建同级地图分组
    MapPage(map_module[0]).add_map_group_from_Default(map_module[1]["map_group_name"])

    assert True


@pytest.mark.positive
@pytest.mark.smoke
def test_upload_map(map_module):
    # 测试在指定地图分组中上传地图

    # 点击地图分组
    GroupTreePage(map_module[0]).click_group_by_name(map_module[1]["map_group_name"])
    # 上传地图
    MapPage(map_module[0]).upload_map(r"{}/map_data/company_4th_floor.jpg".format(SharePath.DATA_FOLDER))
    time.sleep(1)   # 查看上传的地图展示

    assert True
