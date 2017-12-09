# -*- coding: utf-8 -*-
import logging
import traceback
from datetime import datetime

from pymongo import ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError
from pymysql import IntegrityError

from .tests.time_recoder import log_time_with_name
from .statics import Cleaner
from .utils.data import db_mysql, db_mongodb, insert_item_into_mysql, create_table_in_mysql, insert_new_item_into_mysql, \
    insert_hot_item_into_mysql
from .utils.common import date, clean_item_id
from .sqls.sqls import SQL

logger = logging.getLogger(__name__)


class BasicPipeline(object):
    date = date()
    spider = 'detail_xml_redis_spider'
    mongodb = db_mongodb()
    collection_detail = mongodb['d_{0}'.format(date)]
    mysql = db_mysql()
    cursor = mysql.cursor()
    cleaner = Cleaner(date, mongodb)

    def process_item(self, item, spider):
        if spider.name == self.spider:
            return self.process_item_spider(item, spider)

    def process_item_spider(self, item, spider):
        pass


class CleanPipeline(BasicPipeline):
    # @log_time_with_name('CleanPipeline')
    def process_item_spider(self, item, spider):
        logger.info(item)
        item = dict(item)
        item['date'] = self.date
        try:
            data = self.cleaner.data_cleaned(item)
            # item = dict(data, **item)
            item = dict(item, **data)
        except Exception as e:
            info = traceback.format_exc()
            logger.warning("Clean Item Error. Exception: \n{0}\n{1}".format(e, info))
        else:
            return item


class MongodbPipeline(BasicPipeline):
    def __init__(self):
        try:
            self.collection_detail.create_index([('itemId', ASCENDING)], unique=True)
            self.collection_detail.create_index([('quantitySoldYesterday', DESCENDING)], unique=False)
            self.collection_detail.create_index([('topCategoryID', ASCENDING)], unique=False)
        except Exception as e:
            logger.warning('Create index fail. exception: \n{0}'.format(e))

    # @log_time_with_name('MongodbPipeline')
    def process_item_spider(self, item, spider):
        try:
            self.collection_detail.insert_one(item)
        except DuplicateKeyError:
            logger.info("Mongodb Duplicate Item. item: \n{0}".format(item))
        except Exception as e:
            info = traceback.format_exc()
            logger.warning("Unknown Mongodb Error. Exception: \n{0}\n{1}".format(e, info))
        finally:
            return item


class MysqlPipeline(BasicPipeline):
    def __init__(self):
        create_table_in_mysql(self.date, SQL['goods'])

    # @log_time_with_name('MysqlPipeline')
    def process_item_spider(self, item, spider):
        if item['quantitySold'] > 0:
            try:
                insert_item_into_mysql(item, self.date, self.mysql, self.cursor)
            except IntegrityError:
                logger.info("Mysql Duplicate Item. item: \n{0}".format(item))
            except Exception as e:
                info = traceback.format_exc()
                logger.warning("Unknown Mysql Error. Exception: \n{0}\n{1}".format(e, info))
            finally:
                return item
        return item


class NewItemPipeline(BasicPipeline):
    def __init__(self):
        create_table_in_mysql(self.date, SQL['new_goods'])

    # @log_time_with_name('NewItemPipeline')
    def process_item_spider(self, item, spider):
        if item['isNew'] == 1:
            try:
                insert_new_item_into_mysql(item, self.date, self.mysql, self.cursor)
            except IntegrityError:
                logger.info("Mysql Duplicate Item. item: \n{0}".format(item))
            except Exception as e:
                info = traceback.format_exc()
                logger.warning("Unknown Mysql Error. Exception: \n{0}\n{1}".format(e, info))
            finally:
                return item
        return item


class HotItemPipeline(BasicPipeline):
    def __init__(self):
        create_table_in_mysql(self.date, SQL['hot_goods'])

    # @log_time_with_name('HotItemPipeline')
    def process_item_spider(self, item, spider):
        if item['isHot'] == 1:
            try:
                insert_hot_item_into_mysql(item, self.date, self.mysql, self.cursor)
            except IntegrityError:
                logger.info("Mysql Duplicate Item. item: \n{0}".format(item))
            except Exception as e:
                info = traceback.format_exc()
                logger.warning("Unknown Mysql Error. Exception: \n{0}\n{1}".format(e, info))
            finally:
                return item
        return item


class ShopStatisticsPipeline(BasicPipeline):
    # @log_time_with_name('ShopStatisticsPipeline')
    def process_item_spider(self, item, spider):
        try:
            self.cleaner.add_up_shop(item)
        except Exception as e:
            info = traceback.format_exc()
            logger.warning("Unknown ShopStatistics Error. Exception: \n{0}\n{1}".format(e, info))
        finally:
            return item
