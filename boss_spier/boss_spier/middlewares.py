# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import requests
import undetected_chromedriver as uc
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from scrapy import signals
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
import time
import random
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

# class SeleniumMiddleware:
#     def process_request(self, request, spider):
#         # 创建浏览器实例
#         url = request.url
#         if url =="https://www.zhipin.com":
#             chrome_driver_path = r"D:\Program Files\chromedriver-win64\chromedriver.exe"
#             service = Service(executable_path=chrome_driver_path)
#             # 配置 Chrome 选项
#             PROXY = f"http://122.96.255.219:20167"
#
#             options = webdriver.ChromeOptions()
#             options.add_argument(f'--proxy-server={PROXY}')
#             options.add_argument(
#                 "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
#             options.add_argument('--disable-blink-features=AutomationControlled')
#             options.add_experimental_option("excludeSwitches", ["enable-automation"])
#             options.add_experimental_option('useAutomationExtension', False)
#             # 启动浏览器
#             driver = webdriver.Chrome(service=service, options=options)
#             driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") # 隐藏navigator.webdriver属性
#
#             # 使用stealth库进一步隐藏自动化特征
#             stealth(
#                 driver,
#                 languages=["zh-CN", "zh"],
#                 vendor="Google Inc.",
#                 platform="Win32",
#                 webgl_vendor="Intel Inc.",
#                 renderer="Intel Iris OpenGL Engine",
#                 fix_hairline=True,
#                 run_on_insecure_origins=True,
#                 # 特别针对中文网站的配置
#                 locale="zh-CN",
#                 timezone="Asia/Shanghai"
#             )
#
#             # 访问 Boss 直聘
#             driver.get(url)
#             time.sleep(5)
#             page_source = driver.page_source  # 获取页面源码
#             driver.quit()
#             res = HtmlResponse(url=url, body=page_source, encoding="utf-8", request=request)
#             return res
#         return None


class SeleniumMiddlewareTwe:
    def __init__(self):
        self.driver = None  # 单例浏览器实例
        self.max_retries = 3
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
            api_url = "https://dps.kdlapi.com/api/getdps?secret_id=o4l7sc3jex4b9ylskndf&num=1&signature=c0wsmknpo3pqvgkock5z3m4xlepptnh8"
            response = requests.get(api_url)
            PROXY = f"http://{response.text}"
            # PROXY = f"http://218.95.37.135:21580"
            options = webdriver.ChromeOptions()
            # socks5_proxy = "socks5://128.199.202.122:1080"  # 示例地址，请替换为您的代理
            options.add_argument(f'--proxy-server={PROXY}')
            options.add_argument(random.choice(
            ['Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.2991.101 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.2700.69 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.2128.93 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.2651.92 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.2148.109 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.2986.31 Safari/537.36',
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3581.86 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.2991.101 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.2784.100 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3806.52 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3888.51 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3378.47 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.2336.120 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3562.172 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3928.120 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.2909.135 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.2263.122 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3010.44 Safari/537.36'
             ]))
            options.add_argument('--disable-web-security')
            options.add_argument('--disable-site-isolation-trials')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-webgl-device-blacklist')
            # 强制修改渲染器信息
            options.add_argument('--use-gl=angle')
            options.add_argument('--use-angle=gl-egl')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            # options.add_argument('--ssl-version-min=tls1.2')
            # options.add_argument('--cipher-suite-blacklist=0x0004,0x0005,0xC011,0xC007')
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            width = random.randint(800, 1200)
            height = random.randint(600, 900)
            self.driver.set_window_size(width, height)
            # 设置随机窗口位置（避免超出屏幕）
            screen_width = self.driver.execute_script("return window.screen.availWidth")
            screen_height = self.driver.execute_script("return window.screen.availHeight")
            x = random.randint(0, screen_width - width)
            y = random.randint(0, screen_height - height)
            self.driver.set_window_position(x, y)

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
        new_ua = random.choice(
            ['Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.2991.101 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.2700.69 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.2128.93 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.2651.92 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.2148.109 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.2986.31 Safari/537.36',
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3581.86 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.2991.101 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.2784.100 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3806.52 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3888.51 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3378.47 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.2336.120 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3562.172 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3928.120 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.2909.135 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.2263.122 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3010.44 Safari/537.36'
             ])
        try:
            url = request.url
            if url =="https://www.zhipin.com":
                driver = self.init_driver()
                self.driver.get(url)
                time.sleep(5)
                page_source = driver.page_source
                res = HtmlResponse(url=url, body=page_source, encoding="utf-8", request=request)
                return res

            if request.meta.get('middleware') == 'A':
                    self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": new_ua})
                    driver = self.init_driver()
                    driver.get(url)
                    WebDriverWait(driver, 600).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "job-search-form"))
                    )

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


            if request.meta.get('middleware') == 'B':

                self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": new_ua})
                driver = self.init_driver()
                driver.get(url)
                element = WebDriverWait(driver, 600).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "job-search-form"))
                )
                time.sleep(random.uniform(1, 2))
                scroll_amounts = random.randint(50, 100)  # 随机滚动距离
                driver.execute_script(f"window.scrollBy(0, {scroll_amounts})")

                page_source = driver.page_source
                res = HtmlResponse(url=url, body=page_source, encoding="utf-8", request=request)
                return res
            return None
        except Exception as e:
            spider.logger.error(f"处理请求异常: {str(e)}")

            return self.reset_browser(request,spider)

    def reset_browser(self, request=None, spider=None):
        """异常后重置浏览器并重试请求"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                if spider:
                    spider.logger.error(f"关闭浏览器时出错: {str(e)}")
            finally:
                self.driver = None

        # 添加短暂延迟，确保浏览器完全关闭
        import time
        time.sleep(random.uniform(50, 100))

        # 如果没有请求对象或spider对象，返回None
        if not request or not spider:
            return None

        # 检查重试次数
        retry_times = request.meta.get('retry_times', 0)
        if retry_times >= self.max_retries:
            spider.logger.error(f"达到最大重试次数 {self.max_retries}，放弃请求 {request.url}")
            raise Exception(f"达到最大重试次数 {self.max_retries}，放弃请求 {request.url}")

        try:
            # 重新初始化浏览器
            self.init_driver()

            # 复制原始请求的meta信息
            retry_request = request.copy()
            retry_request.dont_filter = True  # 确保重试请求不会被过滤

            # 更新重试次数
            retry_request.meta['retry_times'] = retry_times + 1
            spider.logger.info(f"重试请求 {request.url} (第 {retry_times + 1} 次)")

            # 处理重试请求并返回结果
            return self.process_request(retry_request, spider)
        except Exception as e:
            spider.logger.error(f"重试请求失败: {str(e)}")
            raise

    def spider_closed(self, spider):
        """爬虫关闭时清理资源"""
        if self.driver:
            self.driver.quit()
            self.driver = None