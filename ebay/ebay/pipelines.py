# -*- coding: utf-8 -*-
import logging
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from .statics import Cleaner
from .utils.data import db_mysql, db_mongodb, insert_item_into_mysql, create_table_in_mysql
from .utils.common import date, clean_item_id

logger = logging.getLogger(__name__)


class EbayPipeline(object):
    def __init__(self):
        self.mongodb = db_mongodb()
        self.date = date()
        self.collection = self.mongodb['c_{0}'.format(self.date)]
        self.collection_detail = self.mongodb['d_{0}'.format(self.date)]
        # self.collection_detail.ensure_index('itemId', unique=True)
        # todo 索引构建应在 app.init() 中实现
        self.mysql = db_mysql()
        self.cursor = self.mysql.cursor()
        self.cleaner = Cleaner(self.date, self.mongodb)
        create_table_in_mysql(self.date)

    def process_item(self, item, spider):
        if spider.name == 'listing_redis_spider':
            return self.process_item_listing(item, spider)
        elif spider.name == 'detail_xml_redis_spider':
            return self.process_item_detail(item, spider)

    def process_item_detail(self, item, spider):
        logger.info(item)
        item = dict(item)
        item['date'] = self.date

        try:
            # 数据统计
            data = self.cleaner.data_cleaned(item)
            item = dict(data, **item)
            # 写入 mongodb 与 mysql
            self.collection_detail.insert_one(item)
            insert_item_into_mysql(item, self.date, self.mysql, self.cursor)
        except:
            logger.info("Database Error.")
        else:
            return item

    def process_item_listing(self, item, spider):
        c = self.collection
        listing = {}
        listing['price'] = item.get('price')
        listing['title'] = item.get('title')
        listing['seller'] = item.get('seller')
        listing['itemLocation'] = item.get('itemLocation')
        listing['categories'] = item.get('categories')
        listing['image'] = item.get('image')
        listing['itemId'] = item.get('itemId')
        listing['itemWebUrl'] = item.get('itemWebUrl')
        listing['date'] = self.date
        logger.info(listing)
        # return listing
        try:
            c.insert_one(listing)
        except DuplicateKeyError:
            logger.info("Duplicate Item")
        else:
            return
