""" GUI tests for blog """

import json

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from blog.tests.page_objects.login_page import LoginPage
from blog.tests.page_objects.posts_page import PostsPage
from blog.tests.utils import get_screenshot

with open('blog/tests/test_data.json') as f:
    DATA = json.load(f)


class MySeleniumTests(StaticLiveServerTestCase):
    """ GUI tests for blog
    """
    fixtures = ["blog/tests/test_data.json"]

    def setUp(self):
        options = Options()
        options.add_argument("--headless")

        self.selenium = WebDriver(firefox_options=options)
        self.selenium.implicitly_wait(10)

    def tearDown(self):
        for method, error in self._outcome.errors:
            if error:
                print(f'{self._testMethodName} failed.'
                      f'Screenshot saved: {get_screenshot(self.selenium)}')

        self.selenium.quit()

    def test_login(self):
        """ Check login and redirection """
        self.selenium.get(f'{self.live_server_url}/admin/login/?next=/')
        LoginPage(self.selenium).login("tester", "Qwerty123")

        page = PostsPage(self.selenium)
        title = page.post_block_title(1)
        assert title.text == DATA[2]["fields"]["title"]

    def test_posts(self):
        """ Check that initially created posts are presented at the main page
        """
        self.selenium.get(self.live_server_url)
        page = PostsPage(self.selenium)
        title1 = page.post_block_title(1)
        assert title1.text == DATA[2]["fields"]["title"]
        title2 = page.post_block_title(2)
        assert title2.text == DATA[1]["fields"]["title"]
