# -*- coding: utf-8 -*-
import logging
from pymysql import connect
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from redis import Redis
from ..configs.database_config import Config

logger = logging.getLogger(__name__)


def db_mongodb_base(db_name, host, port):
    Client = MongoClient(host, port)
    db = Client[db_name]
    return db


def db_mongodb():
    return db_mongodb_base(
        Config['mongodb']['database'],
        Config['mongodb']['host'],
        Config['mongodb']['port'])


def category_ids():
    db = db_mongodb()
    c = db.category_ids
    # todo-1 改为 pop 操作 | 取一条删一条
    for data in c.find():
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


def db_redis():
    redis = Redis()
    return redis


def category_ids_from_mysql():
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
        logger.info("Mysql error")
    else:
        mysql.close()


def insert_category_ids(to='mongodb', db=None):
    if to == 'mongodb':
        insert_category_ids_to_mongodb(db)
    elif to == 'redis':
        insert_category_ids_to_redis(db)


def insert_category_ids_to_mongodb(mongodb=None):
    ''' category_ids 从 mysql 转移至 mongodb '''
    m = mongodb
    if m is None:
        m = db_mongodb()
    c = m['category_ids']
    c.ensure_index('category_id', unique=True)
    for listing in category_ids_from_mysql():
        try:
            c.insert_one(listing)
        except DuplicateKeyError:
            print("Duplicate ")
    print('count: ', c.count())


def insert_category_ids_to_redis(redis=None):
    ''' category_ids 从 mysql 转移至 redis '''
    r = redis
    if r is None:
        r = db_redis()
    for listing in category_ids_from_mysql():
        try:
            url = 'https://api.ebay.com/buy/browse/v1/item_summary/search?limit=200&category_ids={0}&fieldgroups=FULL'
            url = url.format(listing.get('category_id'))
            redis.lpush('ebay:category_urls', url)
        except:
            print("Redis Error")
    print('Done')


def token_from_redis(redis):
    # 从 redis 获取 token todo
    pass


def keep_token_available():
    # todo 定期获取 token
    pass


def category_id_from_redis(redis):
    # 从 redis 获取 category_id todo
    pass


def item_id_from_redis(redis):
    # 从 redis 获取 category_id todo
    pass


def item_id_is_duplicated(item_id, redis):
    ''' 商品分类是否重复 todo
    :param category_id: 
    :return: 
    '''
    return False


if __name__ == '__main__':
    pass
