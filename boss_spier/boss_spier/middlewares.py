# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from fake_useragent import UserAgent
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from scrapy import signals
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
import time
import random
import logging


class SeleniumMiddleware:
    def process_request(self, request, spider):
        # 创建浏览器实例
        url = request.url
        chrome_driver_path = r"D:\Program Files\chromedriver-win64\chromedriver.exe"
        service = Service(executable_path=chrome_driver_path)
        # 配置 Chrome 选项
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # 启动浏览器
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        stealth(
            driver,
            languages=["zh-CN", "zh"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            run_on_insecure_origins=True,
            # 特别针对中文网站的配置
            locale="zh-CN",
            timezone="Asia/Shanghai"
        )

        # 访问 Boss 直聘
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        driver.quit()
        res = HtmlResponse(url=url, body=html, encoding="utf-8", request=request)
        return res