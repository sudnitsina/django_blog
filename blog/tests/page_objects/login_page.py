""" Representation of admin login page admin/login/ """


class LoginPage:
    """ Representation of admin login page admin/login/ """

    def __init__(self, driver):
        self.driver = driver

        self.name_field = "username"
        self.password_field = "password"

        self.submit_button = "/html/body/div/div[2]/div/form/div[3]/input"

    def login(self, username: str, password: str):
        """ Fill and submit login form
        """
        username_input = self.driver.find_element_by_name(self.name_field)
        username_input.send_keys(username)
        password_input = self.driver.find_element_by_name(self.password_field)
        password_input.send_keys(password)
        self.driver.find_element_by_xpath(self.submit_button).click()
