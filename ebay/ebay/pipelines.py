# -*- coding: utf-8 -*-
import logging
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from .utils.data import db_mysql, db_mongodb
from .utils.common import date, clean_item_id

logger = logging.getLogger(__name__)


class EbayPipeline(object):
    def __init__(self):
        self.mongodb = db_mongodb()
        self.date = date()
        self.collection = self.mongodb['c_{0}'.format(self.date)]
        self.collection.ensure_index('itemId', unique=True)
        self.collection_detail = self.mongodb['d_{0}'.format(self.date)]

        # self.mysql = db_mysql()
        # self.cursor = self.mysql.cursor()

    def process_item(self, item, spider):
        if spider.name == 'listing_redis_spider':
            self.process_item_listing(item, spider)
        elif spider.name == 'detail_xml_redis_spider':
            self.process_item_detail(item, spider)

    def process_item_detail(self, item, spider):
        d = self.collection_detail
        item['date'] = self.date
        logger.info(item)
        try:
            d.insert_one(item)
        except:
            logger.info("Mongodb Error")
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
