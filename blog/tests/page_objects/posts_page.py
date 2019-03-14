""" Representation of the main page containing all available posts
"""
from selenium.webdriver.common.by import By

from blog.tests.page_objects.base_page import BasePage
from blog.tests.page_objects.elements.side_panel import SidePanelElement
from blog.tests.page_objects.elements.top_panel import TopPanelElement


class PostsPage(BasePage):
    """ Representation of the main page containing all available posts """

    def __init__(self, driver):
        self.driver = driver

        self.top_panel = TopPanelElement(driver)
        self.side_panel = SidePanelElement(driver)

        self.post = By.CLASS_NAME, "post"

    # TODO: separate class for post

    def post_block_title(self, index: int):
        """
        :param index: number of block
        :return: webelement for post title
        """
        return self.driver.find_element_by_xpath(
            f"/html/body/div[2]/div[1]/div[{index}]/div/h2/a"
        )

    def posts(self):
        """ Return list of post elements from page
        """
        return self.driver.find_elements(*self.post)
