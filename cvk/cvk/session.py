# session.py

import time

from selenium import webdriver
from contextlib import asynccontextmanager
from pyvirtualdisplay import Display


@asynccontextmanager
async def session():
    driver = await clean_chrome()
    yield driver
    await kill_selenium(driver)


async def clean_chrome():
    display = Display(visible=0)
    display.start()
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1024,768')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver


async def kill_selenium(driver):
    # required to correctly send requests to another server
    time.sleep(0.5)
    driver.close()
    driver.quit()
