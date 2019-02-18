""" """
from selenium.webdriver.common.by import By
from blog.tests.page_objects.base_page import BasePage


class SidePanelElement(BasePage):

    def __init__(self, driver):
        self.driver = driver

        self.new = By.LINK_TEXT, "new post"

    def click_new(self):
        """Click link "new post"
        """
        self.driver.find_element(*self.new).click()

    def check_new_link_is_not_available(self):

        return self.object_not_exists(self.driver, self.new)
