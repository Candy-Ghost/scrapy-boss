# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BossSpierItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jobs_max_name = scrapy.Field()
    jobs_mid_name = scrapy.Field()
    jobs_min_name = scrapy.Field()
    jobs_link = scrapy.Field()
    jobs_name = scrapy.Field()
    jobs_detail_link = scrapy.Field()

