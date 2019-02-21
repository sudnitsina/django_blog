""" GUI tests for blog
run: python manage.py test
or
python -m pytest blog/tests/tests_selenium.py
install pytest-xdist to use multiple processes
python -m pytest -n 2 blog/tests/tests_selenium.py
"""

import json
import logging
import pytest

from django.contrib.auth.models import User

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from blog.tests.page_objects.login_page import LoginPage
from blog.tests.page_objects.posts_page import PostsPage
from blog.tests.page_objects.post_page import PostPage, EditPostPage
from blog.tests.utils import get_screenshot

with open('blog/tests/test_data.json') as f:
    DATA = json.load(f)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# TODO: move test data to files


@pytest.fixture(autouse=True)
def user(db):
    User.objects.create_superuser(username="admin",
                                  email="test@test.test",
                                  password="admin")


class MySeleniumTests(StaticLiveServerTestCase):
    """ GUI tests for blog
    """
    fixtures = ["blog/tests/test_data.json"]

    def setUp(self):
        options = Options()
        options.add_argument("--headless")

        self.selenium = WebDriver(firefox_options=options)
        self.selenium.implicitly_wait(10)

        logger.info("'%s' testcase started", self._testMethodName)

    def tearDown(self):
        for method, error in self._outcome.errors:
            if error:
                logger.info('%s failed. Screenshot saved: %s',
                            self._testMethodName, get_screenshot(self.selenium))

        self.selenium.quit()

    @pytest.mark.page('login.html')
    def test_login(self):
        """ Check login and redirection
        """
        self.selenium.get(f'{self.live_server_url}/admin/login/?next=/')
        LoginPage(self.selenium).login("tester", "Qwerty123")
        logging.info("Verify post page")
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

    def test_new(self):
        """ Click link 'new' from side panel and verify redirection
        """
        self.selenium.get(self.live_server_url)
        page = PostsPage(self.selenium)
        page.side_panel.click_new()
        assert page.side_panel.check_new_link_is_not_available()

    def test_search(self):
        """ Apply search and verify that only one post is available and it has a right title
        """
        self.selenium.get(self.live_server_url)
        page = PostsPage(self.selenium)
        page.top_panel.search("test")
        assert len(page.posts()) == 1

        title = page.post_block_title(1)
        assert title.text == DATA[2]["fields"]["title"]

    def test_edit_tags(self):
        """ Add tags to post
        """
        self.selenium.get(self.live_server_url)
        page = PostsPage(self.selenium)
        title = page.post_block_title(1)
        title.click()

        PostPage(self.selenium).edit()

        LoginPage(self.selenium).login("tester", "Qwerty123")

        edit_post_page = EditPostPage(self.selenium)
        edit_post_page.add_tags("a", "b", "C")
        edit_post_page.save()
        page = PostPage(self.selenium)
        assert len(page.get_tags()) == 3

        # TODO: make separate test for tag filtering
        page.click_tag("a")
        assert self.selenium.current_url[-7:] == "/tag/a/"
