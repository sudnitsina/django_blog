import os
import requests

FILE_PATH = 'screenshot.png'


def get_screenshot(driver):
    """ Take and save screenshot
    """
    driver.get_screenshot_as_file(FILE_PATH)

    return img_uploader(FILE_PATH)


def img_uploader(img_path):
    """ Upload file to url specifies in environment variable
    """
    url = os.environ.get("upload_url")
    if not url:

        return "upload_api variable is not specified"

    file = {"file": open(img_path, "rb")}
    my_session = requests.Session()
    res = my_session.post(url, files=file)

    return res.text
