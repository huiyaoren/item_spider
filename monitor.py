from datetime import datetime
from time import sleep

from pymongo.errors import DuplicateKeyError

from ebay.ebay.utils.common import date
from ebay.ebay.utils.data import db_redis, db_mongodb, db_mysql

'''
爬虫数据监控
'''


class Monitor():
    def __init__(self):
        self.redis = db_redis()
        self.mongodb = db_mongodb()
        self.mongodb_remote = None
        self.date = date()
        self.collection = self.mongodb['m_{0}'.format(self.date)]
        self.collection.ensure_index('item_data', unique=True)
        self.mysql = db_mysql()
        self.mysql_cursor = self.mysql.cursor()

    def data(self):
        r = self.redis
        m = self.mongodb
        data = {}
        data['category_ids'] = r.llen('ebay:category_ids')
        data['category_urls'] = r.llen('ebay:category_urls')
        data['item_ids'] = r.llen('ebay:item_ids')
        data['item_ids_filter'] = r.scard('ebay:item_ids_filter')
        data['item_data'] = m['d_{0}'.format(self.date)].count()
        data['time'] = datetime.now().strftime("%H:%M:%S")
        return data

    def insert_data_to_mongodb(self):
        data = self.data()
        c = self.collection
        try:
            c.insert_one(data)
        except DuplicateKeyError:
            pass
        else:
            print(data)

    def run(self):
        while True:
            self.insert_data_to_mongodb()
            sleep(60)


if __name__ == '__main__':
    monitor = Monitor()
    monitor.run()
