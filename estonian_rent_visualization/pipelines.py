# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2

from credentials import DB_CREDENTIALS


class EstonianRentVisualizationPipeline:
    def open_spider(self, spider):
        self.connection = psycopg2.connect(**DB_CREDENTIALS)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        address = item.get('address', 'No address')
        self.cursor.execute(
            'insert into real_estates (address) values (%s);', (address,))
        self.connection.commit()
