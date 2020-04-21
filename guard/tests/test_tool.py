# -*- coding:utf-8 -*-
# @Time: 2020/3/26 11:34
# @Author: wenqin_zhu
# @File: test_tool.py
# @Software: PyCharm

import re
import time
import pytest
from guard.pages.classes.custom_share_path import SharePath
from guard.datas.tool.tool_data import ToolData
from guard.pages.components.menubar import MenubarPage
from guard.pages.tool import ToolPage
from guard.pages.classes.web_global_info import GlobalDialogInfo


@pytest.mark.positive
@pytest.mark.smoke
@pytest.mark.usefixtures("tool_close_one_to_one_face_compare")
def test_one_to_one_face_compare(login):
    """ 测试1:1人脸验证功能 """
    MenubarPage(login).click_nav_item("工具", "1:1人脸验证")
    ToolPage(login).verify_one_to_one_face(r"{}/tool/img_one_to_one/img1.jpg".format(SharePath.DATA_FOLDER), r"{}/tool/img_one_to_one/img2.jpg".format(SharePath.DATA_FOLDER))

    result = ToolPage(login).get_one_to_one_face_result()
    assert '评分参考' == result


@pytest.mark.positive
@pytest.mark.smoke
@pytest.mark.parametrize("data", ToolData.score_detection_data_negative)
@pytest.mark.usefixtures("tool_close_one_img_quality")
def test_score_detection(login, data):
    """ 测试人脸质量分数检测功能 """
    MenubarPage(login).click_nav_item("工具", "质量分数检测")
    ToolPage(login).evaluate_face_image_quality(r'{}/tool/img_score_detection/{}'.format(SharePath.DATA_FOLDER, data["img_path"]))

    result = ToolPage(login).get_face_image_quality_result()
    assert re.match(r'\d+ .\d+%', result)


@pytest.mark.negative
@pytest.mark.usefixtures("tool_close_one_img_quality")
def test_negative_score_detection(login):
    """ 测试上传大于16M的图片 - 系统支持上传小于16M的图片 """
    MenubarPage(login).click_nav_item("工具", "质量分数检测")
    time.sleep(3)
    ToolPage(login).detect_facial_attribute(r"{}/tool/img_score_detection/size_greater_16M.jpg".format(SharePath.DATA_FOLDER))

    result = GlobalDialogInfo(login).judge_alert_info()
    assert "上传图片大小不能超过 16MB!" in result


@pytest.mark.positive
@pytest.mark.smoke
@pytest.mark.usefixtures("tool_close_face_score_detection")
def test_face_property(login):
    """ 测试人脸属性输出的属性字段 """
    MenubarPage(login).click_nav_item("工具", "人脸属性检测")
    ToolPage(login).detect_facial_attribute(r'{}/tool/img_face_property/normal.jpg'.format(SharePath.DATA_FOLDER))

    # 断言
    result = {
        "sex": ToolPage(login).get_facial_attribute_by_name("性别"),
        "age": ToolPage(login).get_facial_attribute_by_name("年龄"),
        "phiz": ToolPage(login).get_facial_attribute_by_name("表情"),
        "mustache": ToolPage(login).get_facial_attribute_by_name("胡子"),
        "glasse": ToolPage(login).get_facial_attribute_by_name("眼镜"),
        "mask": ToolPage(login).get_facial_attribute_by_name("口罩"),
        "helmet": ToolPage(login).get_facial_attribute_by_name("安全帽"),
        "hat": ToolPage(login).get_facial_attribute_by_name("帽子")
    }
    assert ("性别" in result["sex"]) and ("年龄" in result["age"]) and ("表情" in result["phiz"]) and (
                "胡子" in result["mustache"]) and ("眼镜" in result["glasse"]) and ("口罩" in result["mask"]) and (
                "安全帽" in result["helmet"]) and ("帽子" in result["hat"])


@pytest.mark.negative
@pytest.mark.smoke
@pytest.mark.usefixtures("tool_close_face_score_detection")
@pytest.mark.parametrize("data", ToolData.face_data_negative)
def test_negative_face_property(login, data):
    """ 测试上传不同属性的人脸照片检测出对应的人脸属性 """
    MenubarPage(login).click_nav_item("工具", "人脸属性检测")
    ToolPage(login).detect_facial_attribute(f'{SharePath.DATA_FOLDER}/tool/img_face_property/{data["img_path"]}')

    # 断言
    result = {
        "sex": ToolPage(login).get_facial_attribute_by_name("性别"),
        "age": ToolPage(login).get_facial_attribute_by_name("年龄"),
        "phiz": ToolPage(login).get_facial_attribute_by_name("表情"),
        "mustache": ToolPage(login).get_facial_attribute_by_name("胡子"),
        "glasse": ToolPage(login).get_facial_attribute_by_name("眼镜"),
        "mask": ToolPage(login).get_facial_attribute_by_name("口罩"),
        "helmet": ToolPage(login).get_facial_attribute_by_name("安全帽"),
        "hat": ToolPage(login).get_facial_attribute_by_name("帽子")
    }
    assert (data["sex"] in result["sex"]) and (data["age"] in result["age"]) and (data["phiz"] in result["phiz"]) and (
            data["mustache"] in result["mustache"]) and (data["glasse"] in result["glasse"]) and (
            data["mask"] in result["mask"]) and (data["helmet"] in result["helmet"]) and (data["hat"] in result["hat"])


if __name__ == '__main__':
    pytest.main()
