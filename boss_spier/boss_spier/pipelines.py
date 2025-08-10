# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BossSpierPipeline:
    def __init__(self):
        self.file = open('jobs_link.json','w',encoding='utf-8')

    def process_item(self, item, spider):
        item = dict(item)
        json_data = json.dumps(item,ensure_ascii=False)# 将字典数据序列化(将对象转化为json)
        self.file.write(json_data+ ',\n')
        return item

    def __del__ (self):
        self.file.close()
