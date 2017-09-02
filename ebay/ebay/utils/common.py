# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pymysql import connect

import logging
from ..configs.database_config import Config
from pymongo.errors import DuplicateKeyError


def db_mongodb_base(db_name, uri):
    Client = MongoClient(uri)
    db = Client[db_name]
    return db


def db_mongodb():
    return db_mongodb_base(
        Config['mongodb']['database'],
        'mongodb://{0}:{1}/'.format(Config['mongodb']['host'], Config['mongodb']['port'])
    )


def category_ids():
    db = db_mongodb()
    c = db.category_ids
    for data in c.find()[:100]:
        yield data['category_id']


def db_mysql_base(db_name, host, username, password):
    db = connect(host, username, password, db_name)
    return db


def db_mysql():
    return db_mysql_base(
        Config['mysql']['database'],
        Config['mysql']['host'],
        Config['mysql']['username'],
        Config['mysql']['password'],
    )


def get_category_ids():
    mysql = db_mysql()
    cursor = mysql.cursor()
    sql = 'select platform_category_id from erp_saas_goods_category where site = 201'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print(row[0])
            data = {'category_id': row[0]}
            yield data
    except:
        print("Error: unable to fetch data")
    else:
        mysql.close()
    return


def insert_category_ids():
    mongodb = db_mongodb()
    c = mongodb['category_ids']
    c.ensure_index('category_id', unique=True)
    for listing in get_category_ids():
        try:
            c.insert_one(listing)
        except DuplicateKeyError:
            print("Duplicate ")
            logging.info("Duplicate Item")
    print('count: ', c.count())


if __name__ == '__main__':
    pass
