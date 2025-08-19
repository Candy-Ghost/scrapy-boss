import re
import random
import time
import scrapy
from ..items import BossSpierItem
class ZhipinSpierSpider(scrapy.Spider):
    name = "zhipin_spier"   #爬虫名字
    allowed_domains = ["zhipin.com"] #允许爬虫的域名
    start_urls = ["https://www.zhipin.com"] #起始url

    """response回来的页面代码清洗数据"""
    def parse(self, response):
        jobs_max_cls = response.xpath('//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/dd/b')
        for n,max_cls in enumerate(jobs_max_cls, 1) :
            jobs_mid_cls = response.xpath(f'//*[@id="main"]/div/div[1]/div/div[1]/dl[{n}]/div/ul/li[1]/h4')
            for m,mid_cls in enumerate(jobs_mid_cls, 1) :
                jobs_min_cls = response.xpath(f'//*[@id="main"]/div/div[1]/div/div[1]/dl[{n}]/div/ul/li[{m}]/div/a[1]')
                for min_cls in jobs_min_cls :
                    item = BossSpierItem()
                    item['position'] = min_cls.xpath('./text()').extract_first()
                    jobs_link1 = min_cls.xpath('./@ka').re_first(r'\d+')
                    jobs_link = 'https://www.zhipin.com/web/geek/jobs?query=&city=101280600&position='+jobs_link1
                    key = random.choice(['A', 'B'])
                    yield scrapy.Request(
                            url = jobs_link ,  #需要往下爬的url
                            callback = self.parse_jobs, #获取这次 url response 的清洗方法
                            meta={'item': item, #从上一个url获取的信息传给下一个url response
                                  'middleware': 'A'}, # 选用中间件
                    )
                    # yield item

    def parse_jobs(self,response):
        try:
            item = response.meta['item']  #从上个页面传下来的数据
            jobs_name_link = response.xpath('//*[@id="wrap"]/div[2]/div[3]/div/div/div[1]/ul/div/div/li')
            for jobs in jobs_name_link :
                jobs_link = BossSpierItem()
                jobs_link['position'] = item['position']
                jobs_link["job"] = jobs.xpath('./div[1]/div/a/text()').extract_first()
                address = jobs.xpath('./div[2]/span/text()').extract_first()
                link = jobs.xpath('./div[1]/div/a/@href').extract_first()
                jobs_detail_link = 'https://www.zhipin.com'+link
                # yield jobs_link  #把 jobs_link 传给管道存储

                yield scrapy.Request(
                    url=jobs_detail_link,
                    callback=self.parse_jobs_detail,
                    meta={'item': jobs_link,
                          'middleware': 'B'},
                )
        except Exception as e:
            self.logger.error(f"解析详情页出错: {str(e)}")

    def parse_jobs_detail(self, response):
        try:
            jobs_item = response.meta['item']
            jobs = BossSpierItem()
            jobs['position'] = jobs_item['position']
            jobs["job"] = jobs_item["job"]
            jobs['location'] = response.xpath('//*[@id="main"]/div[1]/div/div/div[1]/p/a/text()').extract_first()
            jobs["salary"] = response.xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[2]/span/text()').extract_first()
            jobs["experience"] = response.xpath('//*[@id="main"]/div[1]/div/div/div[1]/p/span[1]/text()').extract_first()
            jobs["degree"] = response.xpath('//*[@id="main"]/div[1]/div/div/div[1]/p/span[2]/text()').extract_first()
            benefit_sum = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/span')
            if  benefit_sum:
                add_benefit = [n.xpath("./text()").extract_first() for n in benefit_sum]
                jobs["labels"] = f"{add_benefit}"
            else:
                jobs["labels"] = None
            position_description = response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[1]/div[3]/text()').extract()
            jobs["description"] = str(position_description)
            jobs["industry"] = response.xpath('//*[@id="main"]/div[3]/div/div[1]/div[2]/p[4]/a/text()').extract_first()
            if not jobs["industry"]:
                jobs["industry"] = response.xpath('//*[@id="main"]/div[3]/div/div[1]/div[2]/p[3]/a/text()').extract_first()
            skill_sum = response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[1]/ul/li')
            if skill_sum:
                add_skill = [m.xpath("./text()").extract_first() for m in skill_sum]
                jobs["skills"] = f"{add_skill}"
            else:
                jobs["skills"] = None
            jobs["address"] = (response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[4]/div[3]/div/div[1]/text()').extract_first()
                               or
                               response.xpath(
                                   '//*[@id="main"]/div[3]/div/div[2]/div[4]/div[2]/div/div[1]/text()').extract_first()
                               )
            if jobs["address"]:
                district = re.search(r"(.{2}区)", jobs["address"])
                if district:
                    jobs['district'] = district.group(1)
            else:
                jobs['district'] = None
            jobs["brand"] = (response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[4]/div[2]/div/ul/li[1]/text()').extract_first()
                             or
                            response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[4]/div[1]/div/ul/li[1]/text()').extract_first())
            jobs["scale"] = (response.xpath('//*[@id="main"]/div[3]/div/div[1]/div[2]/p[3]/text()').extract_first()
                             or
                             response.xpath('//*[@id="main"]/div[3]/div/div[1]/div[2]/p[2]/text()').extract_first()
                             )
            yield jobs
        except Exception as e:
            self.logger.error(f"解析详情页出错: {str(e)}")


