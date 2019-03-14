""" Representation of page for specific post
"""
from selenium.webdriver.common.by import By

from blog.tests.page_objects.base_page import BasePage
from blog.tests.page_objects.elements.side_panel import SidePanelElement
from blog.tests.page_objects.elements.top_panel import TopPanelElement


class PostPage(BasePage):
    """ Representation of the page containing one specific post """

    def __init__(self, driver):
        self.driver = driver

        self.top_panel = TopPanelElement(driver)
        self.side_panel = SidePanelElement(driver)

        self.tags = By.XPATH, "/html/body/div[2]/div[1]/div/div[2]/a"

        self.edit_button = By.XPATH, "/html/body/div[2]/div[1]/div/span[2]/a"
        self.delete_button = By.XPATH, "/html/body/div[2]/div[1]/div/span[1]/a"

    def edit(self):
        """ Leads to edit or login page
        """
        self.driver.find_element(*self.edit_button).click()

    def get_tags(self):
        """ Get tags list for opened post
        :return: list of webelements
        """
        return self.driver.find_elements(*self.tags)

    def click_tag(self, tag_name):
        """ Click post tag
        :param tag_name:
        """
        self.driver.find_element(
            self.tags[0], self.tags[1] + f"[text()='{tag_name}']"
        ).click()


class EditPostPage(BasePage):
    """ Representation of the page containing post form"""

    def __init__(self, driver):
        self.driver = driver

        self.top_panel = TopPanelElement(driver)
        self.side_panel = SidePanelElement(driver)

        self.tags_field = By.ID, "id_tags"
        self.save_button = (
            By.XPATH,
            "/html/body/div[2]/div[1]/div/form/table/tbody/tr[4]/td/button",
        )

    def add_tags(self, *tags, separator=","):
        """ Enter tags to tags field using specified separator
        """
        for tag in tags:
            self.driver.find_element(*self.tags_field).send_keys(tag, separator)

    def save(self):
        """ Click 'save' button
        """
        self.driver.find_element(*self.save_button).click()
