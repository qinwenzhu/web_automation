# -*- coding:utf-8 -*-
# @Time: 2020/3/24 19:46
# @Author: wenqin_zhu
# @File: tool_page.py
# @Software: PyCharm


from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage


class ToolPage(BasePage):

    def verify_one_to_one_face(self, path1, path2):
        """ 1:1人脸验证 """

        # 上传左侧图片
        IMAGE_UPLOAD_INPUT_L = (By.CSS_SELECTOR, '.app-tools-content-pics .imageselsect-container:first-child > input[type="file"]')
        # 上传右侧图片
        IMAGE_UPLOAD_INPUT_R = (By.CSS_SELECTOR, '.app-tools-content-pics .imageselsect-container:last-child > input[type="file"]')
        # 点击比对按钮
        CHECK_CONTENT_FACE_BUTTON = (By.CLASS_NAME, "app-tools-content-pics-vsbtn")

        # input类型的file文件上传
        BasePage(self.driver).upload_file(IMAGE_UPLOAD_INPUT_L, path1)
        BasePage(self.driver).upload_file(IMAGE_UPLOAD_INPUT_R, path2)
        BasePage(self.driver).click_ele(CHECK_CONTENT_FACE_BUTTON)

    def get_one_to_one_face_result(self):
        # 获取人脸比对成功的结果
        CHECK_RESULT_CONTENT = (By.CSS_SELECTOR, '.app-tools-content-pics-vsbtn-popover > strong')
        return BasePage(self.driver).get_text(CHECK_RESULT_CONTENT)

    def evaluate_face_image_quality(self, path):
        """ 质量分数检测 """

        # 上传人脸图片
        IMAGE_UPLOAD_INPUT = (By.CSS_SELECTOR, 'input[type="file"]')
        # 点击检测按钮
        CHECK_CONTENT_DETECTION_BUTTON = (By.CSS_SELECTOR, '.app-tools-content-detection-detectbtn')

        BasePage(self.driver).upload_file(IMAGE_UPLOAD_INPUT, path)
        BasePage(self.driver).click_ele(CHECK_CONTENT_DETECTION_BUTTON)

    def get_face_image_quality_result(self):
        # 获取人脸质量分数的检测结果
        CHECK_CONTENT_DETECTION_BUTTON_RESULT = (By.XPATH, '//div[@class="app-tools-content-center"]//span')
        # TODO filter 和 lambda结合使用
        # return "".join(filter(lambda c: c not in [' '], self.get_text(CHECK_CONTENT_DETECTION_BUTTON_RESULT)))
        return BasePage(self.driver).get_text(CHECK_CONTENT_DETECTION_BUTTON_RESULT)

    def detect_facial_attribute(self, path):
        """ 人脸属性检测 """

        # 图片上传按钮
        IMAGE_UPLOAD_INPUT = (By.CSS_SELECTOR, 'input[type="file"]')
        # 点击检测
        CHECK_CONTENT_FACE_BUTTON = (By.CSS_SELECTOR, '.app-tools-content-face-detectbtn')

        BasePage(self.driver).upload_file(IMAGE_UPLOAD_INPUT, path)
        BasePage(self.driver).click_ele(CHECK_CONTENT_FACE_BUTTON)

    def get_facial_attribute_by_name(self, name):
        """
        获取返回的人脸属性内容
        :param name: 人脸属性名称，可选性别、年龄、表情、胡子、眼睛、口罩、安全帽、帽子
        """
        CHECK_CONTENT = (By.XPATH, f'//div[@class="app-tools-content-detection-right"]//li//span[contains(text(), "{name}")]/parent::li')
        return BasePage(self.driver).get_text(CHECK_CONTENT, "小工具")

    def close_tool_current_win(self, current_btn):
        """ common 关闭当前操作的小工具 """
        if current_btn == "tools-face-verification":
            CLOSE_BTN = (By.XPATH,
                         f'//div[contains(@class, "{current_btn}")]//i[contains(@class, "app-tools-header-close")]')
        elif current_btn == "tools-score-detection":
            CLOSE_BTN = (By.XPATH,
                         f'//div[contains(@class, "{current_btn}")]//i[contains(@class, "app-tools-header-close")]')
        elif current_btn == "tools-test-detection":
            CLOSE_BTN = (By.XPATH,
                         f'//div[contains(@class, "{current_btn}")]//i[contains(@class, "app-tools-header-close")]')
        BasePage(self.driver).click_ele(CLOSE_BTN)


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.components.menubar import MenubarPage
    from guard.pages.login_page import LoginPage
    driver = webdriver.Chrome()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888", login_way="ssh")
    MenubarPage(driver).click_nav_item("工具", "1:1人脸验证")
