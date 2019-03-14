""" Page objects based on nerodia framework """
from nerodia import browser


class BasePage:
    def __init__(self, br):
        if isinstance(br, browser.Browser):
            self.browser = br
        elif isinstance(br, str):
            self.browser = browser.Browser(br)
        else:
            raise TypeError("Incorrect object type passed to constructor")

    def close(self):
        self.browser.close()

    def goto(self, url=None):
        self.browser.goto(url) if url else self.browser.goto(self.url)


class SideMenu:
    def __init__(self, browser):
        self.browser = browser
        self.new_post = self.browser.link(text="new post")
        self.list_post = self.browser.link(text="all notes")
        self.rss_post = self.browser.link(href="/rss/")


class MainPage(BasePage):
    """Page object"""

    def __init__(self, browser):
        self.browser = browser
        self.side_menu = SideMenu(browser)

        # super().__init__(browser)
        self.url = "/"

    def select_tag(self, name):
        return self.browser.div(class_name="sidemenu").link(text=name)

    def create_post(self):
        pass


class NewPostPage(BasePage):
    pass
