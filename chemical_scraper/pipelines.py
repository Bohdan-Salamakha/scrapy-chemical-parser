# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

import psycopg2
from scrapy.exceptions import DropItem


# useful for handling different item types with a single interface


class ValidationPipeline:
    allowed_units = ['mg', 'g', 'kg', 'ml', 'l']

    def process_item(self, item, spider):
        item.qt_list = item.qt_list[:5]
        item.unit_list = item.unit_list[:5]
        item.currency_list = item.currency_list[:5]
        item.price_pack_list = item.price_pack_list[:5]

        qt_list_length = len(item.qt_list)
        item.qt_list = [qt for qt in item.qt_list if isinstance(qt, int)]

        unit_list_length = len(item.unit_list)
        item.unit_list = [unit for unit in item.unit_list if unit in self.allowed_units]

        if qt_list_length != len(item.qt_list) or unit_list_length != len(item.unit_list):
            raise DropItem(
                f"Inconsistent lengths for qt_list, unit_list, currency_list, price_pack_list in item: {item}"
            )
        return item


class PostgresPipeline:
    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        self.table_name = "parsers_chemicalproduct"
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    @classmethod
    def from_crawler(cls, crawler):
        db_host = crawler.settings.get('POSTGRES_HOST')
        db_port = crawler.settings.get('POSTGRES_PORT')
        db_name = crawler.settings.get('POSTGRES_NAME')
        db_user = crawler.settings.get('POSTGRES_USER')
        db_password = crawler.settings.get('POSTGRES_PASSWORD')
        return cls(db_host, db_port, db_name, db_user, db_password)

    def process_item(self, item, spider):
        connection = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
        cur = connection.cursor()
        sql = f"""INSERT INTO {self.table_name} (company_name, product_url, numcas, 
        name, qt_list, unit_list, currency_list, price_pack_list, availability, collected_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            item.company_name,
            item.product_url,
            item.numcas,
            item.name,
            item.qt_list,
            item.unit_list,
            item.currency_list,
            item.price_pack_list,
            item.availability,
            datetime.datetime.now()
        )
        cur.execute(sql, values)
        connection.commit()
        cur.close()
        connection.close()
        return item
