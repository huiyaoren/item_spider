# -*- coding: utf-8 -*-
import logging
import traceback
from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymysql import IntegrityError

from .tests.time_recoder import log_time_with_name
from .statics import Cleaner
from .utils.data import db_mysql, db_mongodb, insert_item_into_mysql, create_table_in_mysql
from .utils.common import date, clean_item_id

logger = logging.getLogger(__name__)


class EbayPipeline(object):
    @log_time_with_name('EbayPipeline.__init__')
    def __init__(self):
        self.mongodb = db_mongodb()
        self.date = date()
        self.collection = self.mongodb['c_{0}'.format(self.date)]
        self.collection_detail = self.mongodb['d_{0}'.format(self.date)]
        self.mysql = db_mysql()
        self.cursor = self.mysql.cursor()
        self.cleaner = Cleaner(self.date, self.mongodb)
        try:
            self.collection_detail.ensure_index('itemId', unique=True)
        except:
            logger.info('Create index fail.')
        create_table_in_mysql(self.date)

    @log_time_with_name('EbayPipeline.process_item')
    def process_item(self, item, spider):
        if spider.name == 'listing_redis_spider':
            return self.process_item_listing(item, spider)
        elif spider.name == 'detail_xml_redis_spider':
            return self.process_item_detail(item, spider)

    @log_time_with_name('EbayPipeline.process_item_detail')
    def process_item_detail(self, item, spider):
        # fixme 在本机上运行与在服务器上耗时差距巨大 原因可能在于 Mongodb 本机 0.003s 服务器 0.5-0.6s
        logger.info(item)
        item = dict(item)
        item['date'] = self.date

        try:
            # 数据统计
            t0 = datetime.now()
            data = self.cleaner.data_cleaned(item)
            item = dict(data, **item)
            # 写入 mongodb 与 mysql
            t1 = datetime.now()
            print('t1-t0', t1-t0)
            self.collection_detail.insert_one(item)
            t2 = datetime.now()
            print('t2-t1', t2-t1)
            insert_item_into_mysql(item, self.date, self.mysql, self.cursor)
            t3 = datetime.now()
            print('t3-t2', t3-t2)
        except DuplicateKeyError:
            logger.info("Mongodb Duplicate Item. item: \n{0}".format(item))
        except IntegrityError:
            logger.info("Mysql Duplicate Item. item: \n{0}".format(item))
        except Exception as e:
            info = traceback.format_exc()
            logger.warning("Unknown Database Error. Exception: \n{0}\n{1}".format(e, info))
        else:
            return item

    @log_time_with_name('EbayPipeline.process_item_listing')
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
        try:
            c.insert_one(listing)
        except DuplicateKeyError:
            logger.warning("Duplicate Item. item: {0}".format(item))
        else:
            return
