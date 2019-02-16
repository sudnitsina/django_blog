""" Representation of the main page containing all available posts """


class PostsPage:
    """ Representation of the main page containing all available posts """

    def __init__(self, driver):
        self.driver = driver

    # TODO: separate class for post

    def post_block_title(self, index: int):
        """
        :param index: number of block
        :return: webelement for post title
        """
        return self.driver.find_element_by_xpath(f"/html/body/div[2]/div[1]/div[{index}]/div/h2/a")
