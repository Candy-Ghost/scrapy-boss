# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from itemadapter import ItemAdapter
from datetime import datetime

from scrapy.exceptions import DropItem

"""存到json"""
# class BossSpierPipeline:
#     def __init__(self,):
#         self.file = open('css.json','w',encoding='utf-8')
#
#     def process_item(self, item, spider):
#         item = dict(item)
#         json_data = json.dumps(item,ensure_ascii=False)# 将字典数据序列化(将对象转化为json)
#         self.file.write(json_data+ ',\n')
#         return item
#
#     def __del__ (self):
#         self.file.close()

#
# """存到MySQL"""
class BossSpierPipeline:
      #初始化数据库（配置）
    def __init__(self, host, user, password, database, table):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table

        # 延迟初始化连接
        self.conn = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        """
        从 settings 中获取 MySQL 配置
        """
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),  # 使用自定义键名
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            table=crawler.settings.get('MYSQL_TABLE')
        )

    def open_spider(self, spider):
        """
        在爬虫启动时建立数据库连接
        """
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                port=3306,
                password=self.password,
                database=self.database,
                charset='utf8mb4',  # 支持存储 emoji 和特殊字符
                autocommit=False ,# 手动提交事务
                use_pure=True,
            )
            self.cursor = self.conn.cursor(dictionary=True)
            spider.logger.info(f"✅ 成功连接到 MySQL 数据库: {self.database}.{self.table}")
        except mysql.connector.Error as err:
            spider.logger.error(f"❌ MySQL 连接错误: {err}")
            raise DropItem(f"MySQL 连接失败: {err}")

    def close_spider(self, spider):
        """
        在爬虫关闭时关闭数据库连接
        """
        if self.conn:
            if self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                spider.logger.info("🔌 MySQL 连接已关闭")

    def process_item(self, item, spider):
        """
        处理每个 item，将其插入 MySQL 表
        """
        # 获取适配器对象
        adapter = ItemAdapter(item)

        # 准备数据 - 设置默认值防止空值
        data = {
            'id': adapter.get(None),
            'industryName': adapter.get('industry', None), #没有 jobs_max_name 的时候就默认none （根据数据库的键）
            'positionName': adapter.get('position',None),
            'jobName': adapter.get('job', None),
            'brandName': adapter.get('brand', None),
            'locationName': adapter.get('location', None),
            'areaDistrict': adapter.get('district', None),
            'experienceName': adapter.get('experience', None),
            'degreeName': adapter.get('degree', None),
            'salaryDesc': adapter.get('salary', None),
            'showSkills': adapter.get('skills', None),
            'address': adapter.get('address', None),
            'labels': adapter.get('labels', None),
            'scaleName': adapter.get('scale', None),
            'postDescription': adapter.get('description', None),

             # 允许 NULL
        }

        # 构建 SQL 插入语句（参数化查询防止 SQL 注入）
        columns = ', '.join(data.keys())  #将数据的键名用逗号隔开
        placeholders = ', '.join(['%s'] * len(data)) #有多少条数据就有多少个'%s'
        sql = f"INSERT INTO `{self.table}` ({columns}) VALUES ({placeholders})" #sql语句

        try:
            # 执行 SQL 插入
            self.cursor.execute(sql, tuple(data.values()))
            self.conn.commit()  #提交事务
            spider.logger.debug("📥 成功插入数据")
            return item
        except mysql.connector.Error as err:
            # 错误处理
            self.conn.rollback() #事务回滚
            spider.logger.error(f"❌ 插入失败")
            raise DropItem(f"MySQL 插入失败: {err}")