import time

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class ChromeSession:
    def __init__(self):
        self.client = None

    async def __aenter__(self) -> WebDriver:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')

        self.client = webdriver.Remote("http://selenium:4444/wd/hub", options=options)
        return self.client

    async def __aexit__(self, exc_type, exc, tb):
        # required to correctly send requests to another server
        time.sleep(0.5)
        self.client.close()
        self.client.quit()
