import re
import random
import time

import scrapy
from ..items import BossSpierItem
class ZhipinSpierSpider(scrapy.Spider):
    name = "zhipin_spier"
    allowed_domains = ["zhipin.com"]
    start_urls = ["https://www.zhipin.com"]

    def parse(self, response):
        jobs_max_cls = response.xpath('//*[@id="main"]/div/div[1]/div/div[1]/dl/dd/b')
        for n,max_cls in enumerate(jobs_max_cls, 1) :
            jobs_mid_cls = response.xpath(f'//*[@id="main"]/div/div[1]/div/div[1]/dl[{n}]/div/ul/li/h4')
            for m,mid_cls in enumerate(jobs_mid_cls, 1) :
                jobs_min_cls = response.xpath(f'//*[@id="main"]/div/div[1]/div/div[1]/dl[{n}]/div/ul/li[{m}]/div/a')
                for min_cls in jobs_min_cls :
                    item = BossSpierItem()
                    item['jobs_max_name'] = max_cls.xpath('./text()').extract_first()
                    item['jobs_mid_name'] = mid_cls.xpath('./text()').extract_first()
                    item['jobs_min_name'] = min_cls.xpath('./text()').extract_first()
                    jobs_link1 = min_cls.xpath('./@ka').re_first(r'\d+')
                    item['jobs_link'] = 'https://www.zhipin.com/web/geek/jobs?query=&city=101280600&position='+jobs_link1
                    key = random.choice(['A', 'B'])
                    yield scrapy.Request(
                            url = item['jobs_link'] ,
                            callback = self.parse_jobs,
                            meta={'item': item,
                                  'middleware': key},
                    )
                    # yield item

    def parse_jobs(self,response):
        item = response.meta['item']
        jobs_name_link = response.xpath('//*[@id="wrap"]/div[2]/div[3]/div/div/div[1]/ul/div/div/li/div[1]/div/a')
        if not jobs_name_link:
            return
        for jobs in jobs_name_link :
            jobs_link = BossSpierItem()
            jobs_link['jobs_max_name'] = item['jobs_max_name']
            jobs_link['jobs_mid_name'] = item['jobs_mid_name']
            jobs_link['jobs_min_name'] = item['jobs_min_name']
            jobs_link["jobs_name"] = jobs.xpath('./text()').extract_first()
            link = jobs.xpath('./@href').extract_first()
            jobs_link["jobs_detail_link"] = 'https://www.zhipin.com'+link
            yield jobs_link
            # yield scrapy.Request(
            #     url=jobs_link["jobs_detail_link"],
            #     callback=self.parse_jobs_detail,
            #     meta={'item': jobs_link,
            #           'middleware': 'B'},
            # )

    # def parse_jobs_detail(self, response):
    #     try:
    #         jobs_item = response.meta['item']
    #         jobs = BossSpierItem()
    #         jobs["jobs_max_name"] = jobs_item['jobs_max_name']
    #         jobs["jobs_mid_name"] = jobs_item['jobs_mid_name']
    #         jobs["jobs_min_name"] = jobs_item['jobs_min_name']
    #         jobs["jobs_name"] = jobs_item["jobs_name"]
    #         jobs["pay"] = response.xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[2]/span/text()').extract_first()
    #         if not jobs["pay"]:
    #             yield jobs
    #         else:
    #             jobs["address"] = response.xpath('//*[@id="main"]/div[1]/div/div/div[1]/p/a/text()').extract_first()
    #             jobs["experience"] = response.xpath('//*[@id="main"]/div[1]/div/div/div[1]/p/span[1]/text()').extract_first()
    #             jobs["education"] = response.xpath('//*[@id="main"]/div[1]/div/div/div[1]/p/span[2]/text()').extract_first()
    #             benefit_sum = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/span')
    #
    #             add_benefit = [n.xpath("./text()").extract_first() for n in benefit_sum]
    #             jobs["benefit"] = f"{add_benefit}"
    #             position = response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[1]/div[3]/text()').extract()
    #             jobs["position"] = str(position)
    #             yield jobs
    #     except Exception as e:
    #         self.logger.error(f"解析详情页出错: {str(e)}")


