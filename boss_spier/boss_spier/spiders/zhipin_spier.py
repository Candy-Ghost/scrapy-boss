import re

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
                    jobs_link1 = min_cls.xpath('./@ka').extract_first()
                    item['jobs_link'] = 'https://www.zhipin.com/web/geek/jobs?query=&city=101280600&position='+jobs_link1
                    yield scrapy.Request(
                            url = item['jobs_link'] ,
                            callback = self.parse_jobs,
                            meta={'item': item},
                    )
                    # yield item

    def parse_jobs(self,response):
        item = response.meta['item']
        jobs_name_link = response.xpath('//*[@id="wrap"]/div[2]/div[3]/div/div/div[1]/ul/div/div/li/div[1]/div/a')
        for jobs in jobs_name_link :
            jobs_link = BossSpierItem()
            jobs_link['jobs_max_name'] = item['jobs_max_name']
            jobs_link['jobs_mid_name'] = item['jobs_mid_name']
            jobs_link['jobs_min_name'] = item['jobs_min_name']
            jobs_link["jobs_name"] = jobs.xpath('./text()').extract_first()
            link = jobs.xpath('./@href').extract_first()
            jobs_link["jobs_detail_link"] = 'https://www.zhipin.com'+link
            yield jobs_link

