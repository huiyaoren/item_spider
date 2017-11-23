import json
import logging
from datetime import datetime

import multiprocessing
from pymysql import connect, IntegrityError
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from redis import Redis
from pprint import pprint

from ..tokens import Token
from ..utils.common import bytes_to_str
from ..configs.database_config import config
from ..configs.ebay_config import config as ebay_config

logger = logging.getLogger(__name__)


# db


def db_mongodb_base(db_name, host, port):
    Client = MongoClient(host, port)
    db = Client[db_name]
    return db


def db_mongodb(host_name='mongodb_remote'):
    return db_mongodb_base(
        config[host_name]['database'],
        config[host_name]['host'],
        config[host_name]['port'])


def db_mysql_base(db_name, host, username, password):
    db = connect(host=host, user=username, passwd=password, db=db_name, charset='utf8')
    return db


def db_mysql(host_name='mysql'):
    return db_mysql_base(
        config[host_name]['database'],
        config[host_name]['host'],
        config[host_name]['username'],
        config[host_name]['password'],
    )


def create_table_in_mysql(date, sql=None, mysql=None):
    mysql = mysql or db_mysql()
    cursor = mysql.cursor()
    sql = sql or '''
      CREATE TABLE IF NOT EXISTS `goods_{0}` (
          `id` VARCHAR(100) NOT NULL COMMENT '商品id',
          `platform` VARCHAR(20) NOT NULL DEFAULT 'ebay' COMMENT '平台',
          `site` VARCHAR(255) DEFAULT NULL COMMENT '商品所属站点',
          `title` VARCHAR(255) NOT NULL COMMENT '商品信息',
          `default_image` VARCHAR(255) DEFAULT NULL COMMENT '主图',
          `other_images` TEXT COMMENT '商品其他图片，json格式',
          `price` DECIMAL(10,2) NOT NULL DEFAULT '0.00' COMMENT '商品售价',
          `currency` VARCHAR(255) DEFAULT NULL COMMENT '货币符号',
          `total_sold` INT(11) NOT NULL DEFAULT '0' COMMENT '总销量',
          `hit_count` INT(11) DEFAULT NULL COMMENT '访问量',
          `goods_category` VARCHAR(255) NOT NULL COMMENT '商品分类',
          `goods_url` VARCHAR(255) DEFAULT NULL COMMENT '商品页面访问地址',
          `shop_name` VARCHAR(255) DEFAULT NULL COMMENT '店铺名称',
          `shop_feedback_score` INT(11) DEFAULT NULL COMMENT '店铺评分',
          `shop_feedback_percentage` DOUBLE(10,2) DEFAULT NULL COMMENT '店铺好评率',
          `shop_open_time` TIMESTAMP NULL DEFAULT NULL COMMENT '店铺开张时间',
          `publish_time` TIMESTAMP NULL DEFAULT NULL COMMENT '上架时间',
          `weeks_sold` INT(11) NOT NULL DEFAULT '0' COMMENT '周销量',
          `weeks_sold_money` DOUBLE(20,2) DEFAULT '0.00' NOT NULL COMMENT '近7天销售金额',
          `day_sold` INT(11) NOT NULL DEFAULT '0' COMMENT '当日销量',
          `last_weeks_sold` INT(11) DEFAULT NULL COMMENT '上上周销量',
          `trade_increase_rate` DOUBLE(10,4) DEFAULT NULL COMMENT '交易增幅比率，比如：0.1256 表示12.56%',
          `is_hot` ENUM('0','1') DEFAULT '0' COMMENT '是否爆款，0-否，1-是',
          `is_new` ENUM('0','1') DEFAULT '0' COMMENT '是否新品，0-否，1-是',
          `record` TEXT COMMENT '商品 14 天相关统计数据记录',
          `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
          PRIMARY KEY (`id`),
          KEY `idx_title` (`title`(250)) COMMENT '商品标题',
          KEY `idx_goods_category` (`goods_category`(250)),
          KEY `idx_shop_name` (`shop_name`(250)),
          KEY `idx_price` (`price`) USING BTREE COMMENT '售价',
          KEY `idx_weeks_sold` (`weeks_sold`) COMMENT '商品周销量',
          KEY `idx_trade_increase_rate` (`trade_increase_rate`) COMMENT '交易增幅',
          KEY `idx_shop_open_time` (`shop_open_time`),
          KEY `idx_total_sold` (`total_sold`) USING BTREE COMMENT '总销量'
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COMMENT='商品表';'''

    sql = sql.format(date)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except:
        print("Error: unable to fetch data")
        logger.info("Mysql error")
        return False
    else:
        mysql.close()
        print('Create Table In Mysql Done.')
        return True


def db_redis():
    redis = Redis(host=config['redis']['host'])
    return redis


# category


def category_ids():
    ''' 弃用 '''
    db = db_mongodb()
    c = db.category_ids
    for data in c.find():
        yield data['category_id']


def category_ids_from_mysql():
    mysql = db_mysql()
    cursor = mysql.cursor()
    sql = 'SELECT platform_category_id FROM erp_saas_goods_category WHERE site = 201'
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


def category_ids_from_redis(num=1000, redis=None):
    r = redis or db_redis()
    ids = r.smembers('ebay:leaf_category_ids')
    for k, id in enumerate(ids):
        if k >= num:
            break
        yield int(id)


def insert_category_id(specified_category_ids, leaf_category_count=0, redis=None):
    r = redis or db_redis()
    count = leaf_category_count
    leaf_category_ids = set(category_ids_from_redis(count, redis)) if count > 0 else set()
    leaf_category_ids.update(specified_category_ids)
    for i in leaf_category_ids:
        r.lpush('ebay:category_ids', '{0}:1'.format(i))
    print('Insert Category Id Done. Count: {0}'.format(r.llen('ebay:category_ids')))


def insert_category_ids(to='redis', redis=None):
    ''' category_ids 从 mysql 转移至 redis '''
    r = redis or db_redis()
    for listing in category_ids_from_mysql():
        try:
            # insert_category_id(listing.get('category_id'))
            r.lpush('ebay:category_ids', '{0}:1'.format(listing.get('category_id')))
        except:
            print("Redis Error")
    print('Insert Category Id Done. Count: {0}'.format(r.llen('ebay:category_ids')))
    print('Insert Category Ids to Redis Done.')


# token

token = Token(mongodb=db_mongodb('mongodb'), redis=db_redis())


def token_from_redis(redis):
    return token.one()


def reset_token(redis=None, _from='mongodb'):
    ''' 将配置中的 token 导入 redis '''
    token.reset_all(redis)


def copy_token():
    t = Token(mongodb=db_mongodb('mongodb_local'), redis=db_redis())
    t.copy_all(db_mongodb('mongodb_remote'))


# item_id


def insert_item_url_to_redis(item_id, item_url, redis=None):
    r = redis or db_redis()
    if not is_item_id_duplicated(item_id, r):
        r.lpush('ebay:item_urls', item_url)


def insert_item_id_to_redis(item_id, redis=None):
    r = redis or db_redis()
    if not is_item_id_duplicated(item_id, r):
        r.lpush('ebay:item_ids', item_id)


def delete_redis_key(keys, redis=None):
    r = redis or db_redis()
    for key in keys:
        r.delete(key)


def copy_item_ids_to_clean(redis=None):
    r = redis or db_redis()
    r.delete('ebay:item_ids_unclean')
    for id in r.smembers('ebay:item_ids_filter'):
        r.lpush('ebay:item_ids_unclean', id)


def write_item_ids_to_file(redis=None):
    r = redis or db_redis()
    with open('item_ids.txt', 'w') as f:
        for id in r.smembers('ebay:item_ids_filter'):
            f.write(bytes_to_str(id) + '\n')
    print('Write Item Ids To File Done.')


def read_item_ids_from_file(file='item_ids.txt', redis=None):
    ''' 从文件中读取 item id 写入 ebay:item_ids_filter '''
    r = redis or db_redis()
    with open(file, 'r') as f:
        for id in f.readlines():
            r.sadd('ebay:item_ids_filter', id)
    print('Read Item Ids From File Done.')


def is_item_id_duplicated(item_id, redis=None):
    ''' 商品分类是否重复 '''
    r = redis or db_redis()
    return 0 == r.sadd('ebay:item_ids_filter', item_id)


def is_item_ids_enough(count, redis=None):
    ''' 判断获取的 item_id 是否达到预设值 '''
    r = redis or db_redis()
    return r.llen('ebay:item_ids') >= count


# item


def items_from_mongodb(collection, mongodb=None):
    ''' 遍历 mongodb 中的商品数据 '''
    m = mongodb or db_mongodb()
    c = m[collection]
    for data in c.find():
        yield data


def insert_items_into_mysql(day, process=16, from_day='20170907'):
    ''' 将商品数据从 mongodb 转移至 mysql '''
    # fixme-已弃用
    start = datetime.now()
    date = day or datetime.now().strftime("%Y%m%d")
    c = 'd_{0}'.format(date)
    c = 'c_{0}'.format(from_day)
    m = db_mongodb()
    if not create_table_in_mysql(date):
        return False
    pool = multiprocessing.Pool(process)
    for item in items_from_mongodb(c, m):
        # print(item)
        item_new = {}
        item_new['itemId'] = item.get('itemId')
        item_new['site'] = item.get('itemLocation').get('country', 'US')
        item_new['title'] = item.get('title')
        item_new['price'] = item.get('price').get('value')
        item_new['currency'] = item.get('price').get('currency')
        item_new['quantitySold'] = 0
        item_new['hitCount'] = 0
        item_new['categoryID'] = max([int(i.get('categoryId')) for i in item.get('categories', [{'categories': '0'}])])
        item_new['viewItemURL'] = item.get('itemWebUrl')
        item_new['seller'] = item.get('seller').get('username')
        item_new['feedbackScore'] = item.get('seller').get('feedbackScore')
        item_new['positiveFeedbackPercent'] = item.get('seller').get('feedbackPercentage')
        item_new['quantitySoldLastWeek'] = 0
        item_new['quantitySoldTwoWeeksAgo'] = 0
        item_new['isHot'] = 0
        item_new['isNew'] = 0
        item_new['image'] = item.get('image').get('imageUrl', '') if item.get('image') is not None else ' '
        # insert_item_into_mysql(item_new, date)
        pool.apply_async(insert_item_into_mysql, args=(item_new, date,))
    pool.close()
    pool.join()
    print('Insert Items Into Mysql Done. {0}'.format(datetime.now() - start))


def insert_item_into_mysql(item, datetime, mysql=None, cursor=None):
    ''' 插入单条商品数据至 mysql '''
    mysql = mysql or db_mysql()
    cursor = cursor or mysql.cursor()
    data = item_cleaned(item)
    sql = "INSERT INTO erp_spider.goods_{datetime_} (record, id, site, title, price, currency, total_sold, hit_count, goods_category, goods_url, shop_name, shop_feedback_score, shop_feedback_percentage, shop_open_time, publish_time, weeks_sold, last_weeks_sold, is_hot, is_new, default_image, other_images, trade_increase_rate, day_sold, weeks_sold_money)" \
          "VALUES (%(record)s, %(id)s, %(site)s, %(title)s, %(price)s, %(currency)s, %(total_sold)s, %(hit_count)s, %(goods_category)s, %(goods_url)s, %(shop_name)s, %(shop_feedback_score)s, %(shop_feedback_percentage)s, %(shop_open_time)s, %(publish_time)s, %(weeks_sold)s, %(last_weeks_sold)s, %(is_hot)s, %(is_new)s, %(default_image)s, %(other_images)s, %(trade_increase_rate)s, %(day_sold)s, %(weeks_sold_money)s)"
    sql = sql.format(datetime_=datetime)
    cursor.execute(sql, {
        'id': data.get('id', 0),
        'site': data.get('site', 0),
        'title': data.get('title', 0),
        'default_image': data.get('default_image', 0),
        'price': data.get('price', 0),
        'currency': data.get('currency', 0),
        'total_sold': data.get('total_sold', 0),
        'hit_count': data.get('hit_count', 0),
        'goods_category': data.get('goods_category', 0),
        'goods_url': data.get('goods_url', 0),
        'shop_name': data.get('shop_name', 0),
        'shop_feedback_score': data.get('shop_feedback_score', 0),
        'shop_feedback_percentage': data.get('shop_feedback_percentage', 0),
        'shop_open_time': data.get('shop_open_time'),
        'publish_time': data.get('publish_time'),
        'day_sold': data.get('day_sold', 0),
        'weeks_sold': data.get('weeks_sold', 0),
        'last_weeks_sold': data.get('last_weeks_sold', 0),
        'is_hot': data.get('is_hot'),
        'is_new': data.get('is_new'),
        'other_images': data.get('other_images'),
        'trade_increase_rate': data.get('trade_increase_rate'),
        'record': data.get('record'),
        'weeks_sold_money': float(data.get('price', 0)) * int(data.get('weeks_sold', 0)),
    })
    mysql.commit()


def insert_new_item_into_mysql(item, datetime, mysql=None, cursor=None):
    ''' 插入单条商品数据至 mysql '''
    mysql = mysql or db_mysql()
    cursor = cursor or mysql.cursor()
    data = item_cleaned(item)
    sql = "INSERT INTO erp_spider.new_goods_{datetime_} (record, id, site, title, price, currency, total_sold, hit_count, goods_category, goods_url, shop_name, shop_feedback_score, shop_feedback_percentage, shop_open_time, publish_time, weeks_sold, last_weeks_sold, default_image, other_images, trade_increase_rate, day_sold, weeks_sold_money)" \
          "VALUES (%(record)s, %(id)s, %(site)s, %(title)s, %(price)s, %(currency)s, %(total_sold)s, %(hit_count)s, %(goods_category)s, %(goods_url)s, %(shop_name)s, %(shop_feedback_score)s, %(shop_feedback_percentage)s, %(shop_open_time)s, %(publish_time)s, %(weeks_sold)s, %(last_weeks_sold)s, %(default_image)s, %(other_images)s, %(trade_increase_rate)s, %(day_sold)s, %(weeks_sold_money)s)"
    sql = sql.format(datetime_=datetime)
    cursor.execute(sql, {
        'id': data.get('id', 0),
        'site': data.get('site', 0),
        'title': data.get('title', 0),
        'default_image': data.get('default_image', 0),
        'price': data.get('price', 0),
        'currency': data.get('currency', 0),
        'total_sold': data.get('total_sold', 0),
        'hit_count': data.get('hit_count', 0),
        'goods_category': data.get('goods_category', 0),
        'goods_url': data.get('goods_url', 0),
        'shop_name': data.get('shop_name', 0),
        'shop_feedback_score': data.get('shop_feedback_score', 0),
        'shop_feedback_percentage': data.get('shop_feedback_percentage', 0),
        'shop_open_time': data.get('shop_open_time'),
        'publish_time': data.get('publish_time'),
        'day_sold': data.get('day_sold', 0),
        'weeks_sold': data.get('weeks_sold', 0),
        'last_weeks_sold': data.get('last_weeks_sold', 0),
        'other_images': data.get('other_images'),
        'trade_increase_rate': data.get('trade_increase_rate'),
        'record': data.get('record'),
        'weeks_sold_money': float(data.get('price', 0)) * int(data.get('weeks_sold', 0)),
    })
    mysql.commit()


def insert_hot_item_into_mysql(item, datetime, mysql=None, cursor=None):
    ''' 插入单条商品数据至 mysql '''
    mysql = mysql or db_mysql()
    cursor = cursor or mysql.cursor()
    data = item_cleaned(item)
    sql = "INSERT INTO erp_spider.hot_goods_{datetime_} (record, id, site, title, price, currency, total_sold, hit_count, goods_category, goods_url, shop_name, shop_feedback_score, shop_feedback_percentage, shop_open_time, publish_time, weeks_sold, last_weeks_sold, default_image, other_images, trade_increase_rate, day_sold, weeks_sold_money)" \
          "VALUES (%(record)s, %(id)s, %(site)s, %(title)s, %(price)s, %(currency)s, %(total_sold)s, %(hit_count)s, %(goods_category)s, %(goods_url)s, %(shop_name)s, %(shop_feedback_score)s, %(shop_feedback_percentage)s, %(shop_open_time)s, %(publish_time)s, %(weeks_sold)s, %(last_weeks_sold)s, %(default_image)s, %(other_images)s, %(trade_increase_rate)s, %(day_sold)s, %(weeks_sold_money)s)"
    sql = sql.format(datetime_=datetime)
    cursor.execute(sql, {
        'id': data.get('id', 0),
        'site': data.get('site', 0),
        'title': data.get('title', 0),
        'default_image': data.get('default_image', 0),
        'price': data.get('price', 0),
        'currency': data.get('currency', 0),
        'total_sold': data.get('total_sold', 0),
        'hit_count': data.get('hit_count', 0),
        'goods_category': data.get('goods_category', 0),
        'goods_url': data.get('goods_url', 0),
        'shop_name': data.get('shop_name', 0),
        'shop_feedback_score': data.get('shop_feedback_score', 0),
        'shop_feedback_percentage': data.get('shop_feedback_percentage', 0),
        'shop_open_time': data.get('shop_open_time'),
        'publish_time': data.get('publish_time'),
        'day_sold': data.get('day_sold', 0),
        'weeks_sold': data.get('weeks_sold', 0),
        'last_weeks_sold': data.get('last_weeks_sold', 0),
        'other_images': data.get('other_images'),
        'trade_increase_rate': data.get('trade_increase_rate'),
        'record': data.get('record'),
        'weeks_sold_money': float(data.get('price', 0)) * int(data.get('weeks_sold', 0)),
    })
    mysql.commit()


def item_cleaned(item):
    ''' 返回为插入 mysql 而清洗后的商品数据 '''
    registration_date = item.get('registrationDate', '0000-00-00 00:00:00.00')
    start_time = item.get('startTime', '0000-00-00 00:00:00.00')
    o = {}
    o['id'] = item.get('itemId')
    o['site'] = item.get('site')
    o['title'] = item.get('title')
    o['price'] = item.get('price')
    o['currency'] = item.get('currency')
    o['total_sold'] = item.get('quantitySold')
    o['hit_count'] = item.get('hitCount')
    o['goods_category'] = item.get('categoryID')
    o['goods_url'] = item.get('viewItemURL')
    o['shop_name'] = item.get('seller')
    o['shop_feedback_score'] = item.get('feedbackScore')
    o['shop_feedback_percentage'] = item.get('positiveFeedbackPercent')
    o['shop_open_time'] = ' '.join([registration_date[0:10], registration_date[11:19]])
    o['publish_time'] = ' '.join([start_time[0:10], start_time[11:19]])
    o['day_sold'] = int(item.get('quantitySoldYesterday', 0))
    o['weeks_sold'] = int(item.get('quantitySoldLastWeek', 0))
    o['last_weeks_sold'] = int(item.get('quantitySoldTwoWeeksAgo', 0))
    o['record'] = str(item.get('record', 0))
    o['is_hot'] = str(item.get('isHot', 0))
    o['is_new'] = str(item.get('isNew', 0))
    o['default_image'] = item.get('image')
    other_images = item.get('otherImages', [" "])
    other_images = other_images if type(other_images) is list else [other_images]
    other_images = json.dumps([{'url': img} for img in other_images]) if other_images != [" "] else '[]'
    o['other_images'] = other_images
    if o['last_weeks_sold'] > 0 and o['weeks_sold'] > 0:
        o['trade_increase_rate'] = (o['weeks_sold'] - o['last_weeks_sold']) / o['last_weeks_sold']
    else:
        o['trade_increase_rate'] = 0
    return o


if __name__ == '__main__':
    pass
