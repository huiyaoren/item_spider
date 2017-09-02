# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pymysql import connect


def db_mongodb(db_name='test_database', uri='mongodb://localhost:27017/'):
    Client = MongoClient(uri)
    db = Client[db_name]
    return db


def db_mysql(db_name='erp', host='192.168.1.248', username='root', password='root'):
    db = connect(host, username, password, db_name)
    return db


if __name__ == '__main__':
    pass
