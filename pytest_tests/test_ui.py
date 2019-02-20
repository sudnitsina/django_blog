"""
live_server: fixture runs a live Django server in a background thread
run: python -m pytest pytest_tests/test_ui.py
"""
import pytest
from django.contrib.auth.models import User
from nerodia.browser import Browser

CREDENTIALS = {'username': 'admin', 'password': 'admin'}


@pytest.fixture(scope='session')
def browser(live_server):
    browser = Browser(browser="chrome")
    yield browser
    browser.close()


@pytest.fixture(scope='session')
def headless_browser():
    browser = Browser(browser="chrome", options={"headless": True})
    yield browser
    browser.close()


@pytest.fixture(autouse=True)
def user(db):
    User.objects.create_superuser(username="admin",
                                  email="test@test.test",
                                  password="admin")


class TestAuth:
    @pytest.mark.skip
    def test_make_screenshot(self, headless_browser, live_server):
        headless_browser.goto(live_server.url)
        headless_browser.screenshot.save('screen2.png')

    # @pytest.mark.skip
    def test_home(self, browser, live_server):
        browser.goto(live_server.url + "/?search=")
        btn = browser.link(id='logo')
        # btn.wait_until(timeout=2, interval=0.5, method=lambda e: e.enabled)
        btn.click()
        expected_url = live_server.url + "/"
        assert browser.url == expected_url

    # @pytest.mark.skip
    def test_redirect_to_login(self, browser, live_server):
        browser.goto(live_server.url)
        # btn = browser.link(href="/new/")
        btn = browser.link(text="new post")
        btn.click()
        expected_url = live_server.url + "/admin/login/?next=/new/"
        assert browser.url == expected_url
