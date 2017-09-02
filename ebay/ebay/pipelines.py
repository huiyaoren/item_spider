# -*- coding: utf-8 -*-
import logging
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from .utils.common import db_mysql, db_mongodb


logger = logging.getLogger(__name__)

class EbayPipeline(object):
    def __init__(self):

        self.db = db_mongodb()
        self.collection = self.db['test_collection']
        self.collection.ensure_index('itemId', unique=True)

    def process_item(self, item, spider):

        listing = item['data']
        logger.info(listing)
        c = self.collection

        try:
            c.insert_one(listing)
        except DuplicateKeyError:
            logger.info("Duplicate Item")
        else:
            return
