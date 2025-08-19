# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

"""设置爬虫时获取信息的键名"""
class BossSpierItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    position = scrapy.Field()
    industry = scrapy.Field()
    job = scrapy.Field()
    brand = scrapy.Field()
    location = scrapy.Field()
    district = scrapy.Field()
    experience = scrapy.Field()
    degree = scrapy.Field()
    salary = scrapy.Field()
    skills = scrapy.Field()
    description = scrapy.Field()
    address = scrapy.Field()
    labels = scrapy.Field()
    scale = scrapy.Field()

