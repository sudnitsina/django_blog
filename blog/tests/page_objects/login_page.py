""" Representation of admin login page admin/login/ """
from selenium.webdriver.common.by import By


class LoginPage:
    """ Representation of admin login page admin/login/ """

    def __init__(self, driver):
        self.driver = driver

        self.name_field = By.NAME, "username"
        self.password_field = By.NAME, "password"

        self.submit_button = By.CSS_SELECTOR, "input[type='submit']"

    def login(self, username: str, password: str):
        """ Fill and submit login form
        """
        username_input = self.driver.find_element(*self.name_field)
        username_input.send_keys(username)
        password_input = self.driver.find_element(*self.password_field)
        password_input.send_keys(password)

        self.driver.find_element(*self.submit_button).click()
