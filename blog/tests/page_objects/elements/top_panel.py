""" """
from selenium.webdriver.common.by import By


class TopPanelElement:

    def __init__(self, driver):
        self.driver = driver

        self.search_input = By.NAME, "search"
        self.search_button = By.ID, "button-search"

    def search(self, text):
        """ """
        self.driver.find_element(*self.search_input).send_keys(text)
        self.driver.find_element(*self.search_button).click()
