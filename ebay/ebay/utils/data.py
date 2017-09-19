# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from pymysql import connect, IntegrityError
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from redis import Redis

from ..utils.common import bytes_to_str
from ..configs.database_config import config
from ..configs.ebay_config import config as ebay_config

logger = logging.getLogger(__name__)


# db


def db_mongodb_base(db_name, host, port):
    Client = MongoClient(host, port)
    db = Client[db_name]
    return db


def db_mongodb():
    return db_mongodb_base(
        config['mongodb']['database'],
        config['mongodb']['host'],
        config['mongodb']['port'])


def db_mysql_base(db_name, host, username, password):
    db = connect(host=host, user=username, passwd=password, db=db_name, charset='utf8')
    return db


def db_mysql():
    return db_mysql_base(
        config['mysql']['database'],
        config['mysql']['host'],
        config['mysql']['username'],
        config['mysql']['password'],
    )


def create_table_in_mysql(date):
    mysql = db_mysql()
    cursor = mysql.cursor()
    sql = '''
        create table if not EXISTS goods_{0}(
            id varchar(100) not null comment '商品id'primary key,
            site varchar(255) null comment '商品所属站点',
            title varchar(255) null comment '商品信息',
            price decimal(10,2) null comment '商品售价',
            currency varchar(255) null comment '货币符号',
            total_sold int null comment '总销量',
            hit_count int null comment '访问量',
            goods_category varchar(255) null comment '商品分类',
            goods_url varchar(255) null comment '商品页面访问地址',
            shop_name varchar(255) null comment '店铺名称',
            shop_feedback_score int null comment '店铺评分',
            shop_feedback_percentage double(10,2) null comment '店铺好评率',
            shop_open_time timestamp null comment '店铺开张时间',
            publish_time timestamp null comment '上架时间',
            weeks_sold int null comment '周销量',
            last_weeks_sold int null comment '上上周销量',
            is_hot enum('0', '1') default '0' null comment '是否爆款，0-否，1-是',
            is_new enum('0', '1') default '0' null comment '是否新品，0-否，1-是',
            created_at timestamp default CURRENT_TIMESTAMP not null comment '添加时间',
            platform varchar(20) default 'ebay' not null comment '平台',
            default_image varchar(0) null comment '主图',
            other_images text null comment '商品其他图片，json格式',
            trade_increase_rate double(10,4) null comment '交易增幅比率，比如：0.1256 表示12.56%'
        );
        comment '商品表';
        create index idx_goods_category on goods_{0} (goods_category);
        create index idx_shop_name on goods_{0} (shop_name);
        create index idx_title on goods_{0} (title);
        create index idx_price on goods_{0} (price);
        create index idx_total_sold on goods_{0} (total_sold);
        create index idx_weeks_sold on goods_{0} (weeks_sold);
        create index idx_shop_open_time on goods_{0} (shop_open_time);
        create index idx_trade_increase_rate on goods_{0} (trade_inicrease_rate);'''

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
    redis = Redis(host=config['redis']['host'],
                  password=config['redis']['password'])
    return redis


# category


def category_ids():
    db = db_mongodb()
    c = db.category_ids
    # todo-1 改为 pop 操作 | 取一条删一条
    for data in c.find():
        yield data['category_id']


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


def insert_category_id(category_ids, redis=None):
    r = redis or db_redis()
    r.delete('ebay:category_urls')
    for i in category_ids:
        url = 'https://api.ebay.com/buy/browse/v1/item_summary/search?limit=200&category_ids={0}&fieldgroups=FULL'
        url = url.format(i)
        r.lpush('ebay:category_urls', url)
    print('Insert Category Id Done. Count: {0}'.format(r.llen('ebay:category_ids')))


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


# token


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


# item_id


def insert_item_url_to_redis(item_id, item_url, redis=None):
    r = redis or db_redis()
    if not is_item_id_duplicated(item_id, r):
        r.lpush('ebay:item_urls', item_url)


def insert_item_id_to_redis(item_id, redis=None):
    r = redis or db_redis()
    if not is_item_id_duplicated(item_id, r):
        r.lpush('ebay:item_ids', item_id)


def delete_item_ids_filter(redis=None):
    r = redis or db_redis()
    r.delete('ebay:item_ids_filter')


def delete_item_ids(redis=None):
    r = redis or db_redis()
    r.delete('ebay:item_ids')


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
    m = mongodb or db_mongodb()
    c = m[collection]
    for data in c.find():
        yield data


def insert_items_into_mysql(day='20170914'):
    ''' 将商品数据从 mongodb 转移至 mysql'''
    date = day or datetime.now().strftime("%Y%m%d")
    c = 'd_{0}'.format(date)
    m = db_mongodb()
    if not create_table_in_mysql(date):
        return False
    for item in items_from_mongodb(c, m):
        print(item)
        item['registrationDate'] = ' '.join([item['registrationDate'][0:10], item['registrationDate'][11:19]])
        item['startTime'] = ' '.join([item['startTime'][0:10], item['startTime'][11:19]])
        insert_item_into_mysql(item, date)


def insert_item_into_mysql(item, datetime):
    ''' 插入单条商品数据至 mysql '''
    mysql = db_mysql()
    cursor = mysql.cursor()
    data = item
    sql = "INSERT INTO erp_spider.goods_{datetime} (id, site, title, price, total_sold, hit_count, goods_category, goods_url, shop_name, shop_feedback_score, shop_feedback_percentage, shop_open_time, publish_time, weeks_sold, last_weeks_sold, is_hot, is_new, default_image, other_images, trade_inicrease_rate)" \
          "VALUES (%(id)s, %(site)s, %(title)s, %(price)s, %(total_sold)s, %(hit_count)s, %(goods_category)s, %(goods_url)s, %(shop_name)s, %(shop_feedback_score)s, %(shop_feedback_percentage)s, %(shop_open_time)s, %(publish_time)s, %(weeks_sold)s, %(last_weeks_sold)s, %(is_hot)s, %(is_new)s, %(default_image)s, %(other_images)s, %(trade_inicrease_rate)s)"
    sql = sql.format(datetime=datetime)
    print(sql)
    try:
        cursor.execute(sql, {
            'id': data.get('itemId', 0),
            'site': data.get('site', 0),
            'title': data.get('title', 0),
            'default_image': data.get('image', 0),
            'price': data.get('price', 0),
            'total_sold': data.get('quantitySold', 0),
            'hit_count': data.get('hitCount', 0),
            'goods_category': data.get('categoryID', 0),
            'goods_url': data.get('viewItemURL', 0),
            'shop_name': data.get('shop_name', 0),
            'shop_feedback_score': data.get('feedbackScore', 0),
            'shop_feedback_percentage': data.get('positiveFeedbackPercent', 0),
            'shop_open_time': data.get('registrationDate', '0000-00-00 00:00:00'),
            'publish_time': data.get('startTime', '0000-00-00 00:00:00'),
            'weeks_sold': data.get('quantitySoldLastWeek', 0),
            'last_weeks_sold': data.get('quantitySoldTwoWeeksAgo', 0),
            'is_hot': data.get('is_hot') or data.get('isHot', 0),
            'is_new': data.get('is_new') or data.get('isNew', 0),
            'other_images': 0,
            'trade_increase_rate': 0,
        })
    except IntegrityError:
        print("Error: Duplicate")
    else:
        mysql.commit()
        mysql.close()


if __name__ == '__main__':
    pass
