import os.path

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from common.fatal_exception import FatalException


class ChromeBrowserDriverHelper(object):
    def __int__(self, driver_path):
        pass

    @staticmethod
    def get(driver_path: str) -> WebDriver:
        if not driver_path or os.path.exists(driver_path):
            raise FatalException("chrome driver file not exists, you can visit site ["
                                 "https://chromedriver.chromium.org/downloads] to download")
        chrome_service = Service(driver_path)
        return webdriver.Chrome(service=chrome_service)

    @staticmethod
    def get_with_options(driver_path: str, options: Options) -> WebDriver:
        if not driver_path or not os.path.exists(driver_path):
            raise FatalException("chrome driver file not exists, you can visit site ["
                                 "https://chromedriver.chromium.org/downloads] to download")
        chrome_service = Service(driver_path)
        return webdriver.Chrome(service=chrome_service, options=options)

    @staticmethod
    def get_with_default_options(driver_path: str) -> WebDriver:
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # options.add_argument('window-size=1920x1080')
        options.add_argument('--start-maximized')
        options.page_load_strategy = 'normal'
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/80.0.3987.149 Safari/537.36')
        return ChromeBrowserDriverHelper.get_with_options(driver_path, options)

    @staticmethod
    def get_options() -> Options:
        return webdriver.ChromeOptions()
