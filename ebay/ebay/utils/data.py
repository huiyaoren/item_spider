# -*- coding: utf-8 -*-
import logging
from pymysql import connect
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from redis import Redis

from ..utils.common import bytes_to_str
from ..configs.database_config import config
from ..configs.ebay_config import config as ebay_config

logger = logging.getLogger(__name__)


def db_mongodb_base(db_name, host, port):
    Client = MongoClient(host, port)
    db = Client[db_name]
    return db


def db_mongodb():
    return db_mongodb_base(
        config['mongodb']['database'],
        config['mongodb']['host'],
        config['mongodb']['port'])


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
        config['mysql']['database'],
        config['mysql']['host'],
        config['mysql']['username'],
        config['mysql']['password'],
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
    r.delete('ebay:category_urls')
    for listing in category_ids_from_mysql():
        try:
            url = 'https://api.ebay.com/buy/browse/v1/item_summary/search?limit=200&category_ids={0}&fieldgroups=FULL'
            url = url.format(listing.get('category_id'))
            r.lpush('ebay:category_urls', url)
        except:
            print("Redis Error")
    print('count: {0}'.format(r.llen('ebay:category_urls')))
    print('Insert Category Ids to Redis Done.')


def token_from_redis(redis):
    r = redis or db_redis()
    token = r.zrange('ebay:tokens', 0, 0)[0]
    use_token(token, r)
    return bytes_to_str(token)


def reset_token(redis=None):
    r = redis or db_redis()
    r.delete('ebay:tokens')
    for config in ebay_config['product']:
        r.zadd('ebay:tokens', config['token_old'], 0)
    print('Reset Token Done.')


def use_token(token, redis=None):
    r = redis or db_redis()
    r.zincrby('ebay:tokens', token, 1)


def item_id_is_duplicated(item_id, redis=None):
    ''' 商品分类是否重复 '''
    r = redis or db_redis()
    return 0 == r.sadd('ebay:item_ids_filter', item_id)


def insert_item_url_to_redis(item_id, item_url, redis=None):
    r = redis or db_redis()
    if not item_id_is_duplicated(item_id, r):
        r.lpush('ebay:item_urls', item_url)


def insert_item_id_to_redis(item_id, redis=None):
    r = redis or db_redis()
    if not item_id_is_duplicated(item_id, r):
        r.lpush('ebay:item_ids', item_id)


def delete_item_ids_filter(redis=None):
    r = redis or db_redis()
    r.delete('ebay:item_ids_filter')


def delete_item_ids(redis=None):
    r = redis or db_redis()
    r.delete('ebay:item_ids')


def is_item_ids_enough(count, redis=None):
    ''' 判断获取的 item_id 是否达到预设值 '''
    r = redis or db_redis()
    return r.llen('ebay:item_ids') >= count


def copy_item_ids(redis=None):
    r = redis or db_redis()
    for id in r.smembers('ebay:item_ids_filter'):
        r.lpush('ebay:item_ids', id)


if __name__ == '__main__':
    pass
