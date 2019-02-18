from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:

    @staticmethod
    def object_not_exists(driver, locator):
        return WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(locator)
        )
