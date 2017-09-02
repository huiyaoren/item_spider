# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pymysql import connect

from ..configs.database_config import Config


def db_mongodb_base(db_name, uri):
    Client = MongoClient(uri)
    db = Client[db_name]
    return db


def db_mongodb():
    return db_mongodb_base(
        Config['mongodb']['database'],
        'mongodb://{0}:{1}/'.format(Config['mongodb']['host'], Config['mongodb']['port'])
    )


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


if __name__ == '__main__':
    db_mysql()
