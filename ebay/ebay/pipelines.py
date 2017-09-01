# -*- coding: utf-8 -*-

from pymongo import MongoClient


class EbayPipeline(object):
    def __init__(self):
        # MongoDB 数据库连接 todo-1
        Client = MongoClient()
        self.db = Client['test_database']
        self.collection = self.db['test_collection']

    def process_item(self, item, spider):
        return item
