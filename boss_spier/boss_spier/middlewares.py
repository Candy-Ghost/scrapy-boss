# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from scrapy import signals
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
import time
import random
from selenium.webdriver.common.keys import Keys


class SeleniumMiddleware:
    def process_request(self, request, spider):
        # 创建浏览器实例
        url = request.url
        if url =="https://www.zhipin.com":
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
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") # 隐藏navigator.webdriver属性

            # 使用stealth库进一步隐藏自动化特征
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
            page_source = driver.page_source  # 获取页面源码
            driver.quit()
            res = HtmlResponse(url=url, body=page_source, encoding="utf-8", request=request)
            return res
        return None


class SeleniumMiddlewareTwe:
    def __init__(self):
        self.driver = None  # 单例浏览器实例

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        # 将爬虫关闭信号 (spider_closed) 连接到中间件的 spider_closed 方法，关闭浏览器
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def init_driver(self):
        """初始化浏览器（仅执行一次）"""
        if self.driver is None:
            chrome_driver_path = r"D:\Program Files\chromedriver-win64\chromedriver.exe"
            service = Service(executable_path=chrome_driver_path)

            options = webdriver.ChromeOptions()
            # socks5_proxy = "socks5://128.199.202.122:1080"  # 示例地址，请替换为您的代理
            # options.add_argument(f'--proxy-server={socks5_proxy}')
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            stealth(
                self.driver,
                languages=["zh-CN", "zh"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                run_on_insecure_origins=True,
                locale="zh-CN",
                timezone="Asia/Shanghai"
            )
        return self.driver

    def process_request(self, request, spider):
        url = request.url
        if url != "https://www.zhipin.com":
                driver = self.init_driver()
                driver.get(url)
                time.sleep(5)

                last_height = driver.execute_script("return document.body.scrollHeight")
                consecutive_unchange = 0  #连续未变化计数
                max_scroll_attempts = 50  # 最大滚动尝试次数
                scroll_attempts = 0
                # 滚动控制循环
                while scroll_attempts < max_scroll_attempts:
                    scroll_attempts += 1

                    # 随机决定滚动方式
                    if random.random() < 0.9:
                        # 使用JavaScript滚动（兼容性更好）
                        scroll_amount = random.randint(300, 800)  # 随机滚动距离
                        driver.execute_script(f"window.scrollBy(0, {scroll_amount})")

                        # 添加人类化的滚动停顿
                        for _ in range(random.randint(2, 5)):
                            time.sleep(random.uniform(0.05, 0.2))
                            small_scroll = scroll_amount // random.randint(3, 6)
                            driver.execute_script(f"window.scrollBy(0, {small_scroll})")
                    else:
                        # 使用键盘翻页
                        body = driver.find_element(By.TAG_NAME, 'body')
                        body.send_keys(Keys.PAGE_DOWN)
                        time.sleep(random.uniform(0.2, 0.6))

                    # 随机阅读停顿
                    if random.random() < 0.3:
                        pause_time = random.uniform(0.5, 2.5)
                        time.sleep(pause_time)

                    # 随机小概率回滚
                    if random.random() < 0.1:
                        scroll_back = -random.randint(100, 300)
                        driver.execute_script(f"window.scrollBy(0, {scroll_back})")
                        time.sleep(random.uniform(0.3, 1.0))

                    # 获取新页面高度
                    new_height = driver.execute_script("return document.body.scrollHeight")

                    # 检查是否到达底部
                    if new_height == last_height:
                        consecutive_unchange += 1
                        if consecutive_unchange >= 3:
                            break
                    else:
                        consecutive_unchange = 0
                        last_height = new_height

                    # 随机滚动间隔
                    time.sleep(random.uniform(0.2, 1.2))

                # 获取最终页面源码
                page_source = driver.page_source
                res = HtmlResponse(url=url, body=page_source, encoding="utf-8", request=request)
                return res
        return None

    def reset_browser(self):
        """异常后重置浏览器"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        self.driver = None

    def spider_closed(self, spider):
        """爬虫关闭时清理资源"""
        if self.driver:
            self.driver.quit()
            self.driver = None