# -*- coding:utf-8 -*-
# @Time: 2020/4/21 16:30
# @Author: wenqin_zhu
# @File: test_map.py
# @Software: PyCharm

import pytest
from guard.pages.map_page import MapPage


@pytest.mark.positive
@pytest.mark.smoke
def test_create_peer_map_group_from_default(map_module):
    # 测试从Default分组创建同级地图分组
    MapPage(map_module[0]).add_map_group_from_Default(map_module[1]["map_group_name"])

    assert True
