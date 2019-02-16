""" GUI tests for blog """

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from blog.tests.page_objects.login_page import LoginPage
from blog.tests.page_objects.posts_page import PostsPage


class MySeleniumTests(StaticLiveServerTestCase):
    """ GUI tests for blog
    """
    fixtures = ["blog/tests/test_data.json"]

    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)

    def tearDown(self):
        self.selenium.quit()

    def test_login(self):
        """ Check login and redirection """
        self.selenium.get(f'{self.live_server_url}/admin/login/?next=/')
        LoginPage(self.selenium).login("tester", "Qwerty123")

        page = PostsPage(self.selenium)
        title1 = page.post_block_title(1)
        assert title1.text == "Testing tools"

    def test_posts(self):
        """ Check that initially created posts are presented at the main page
        """
        self.selenium.get(self.live_server_url)
        page = PostsPage(self.selenium)
        title1 = page.post_block_title(1)
        assert title1.text == "Testing tools"
        title2 = page.post_block_title(2)
        assert title2.text == "Django documentation"
