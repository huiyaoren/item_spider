import json
import logging
from datetime import datetime, timedelta
from multiprocessing.pool import Pool

import pymysql

from ebay.ebay.tests.time_recoder import log_time_with_name
from ebay.ebay.utils.common import date
from ebay.ebay.utils.data import db_redis, db_mongodb, db_mysql

logger = logging.getLogger(__name__)


class Statistician():
    def __init__(self, redis=None, mongodb=None, mysql=None):
        self.redis = redis or db_redis()
        self.mongodb = mongodb or db_mongodb('mongodb_remote')
        self.mysql = mysql or db_mysql()
        self.mysql_cursor = self.mysql.cursor()
        self.date = date()

    def execute_sql(self, sql, data=None, mysql=None, cursor=None):
        mysql = mysql or db_mysql()
        cursor = cursor or mysql.cursor()
        try:
            cursor.execute(sql, data)
            mysql.commit()
        except pymysql.err.IntegrityError:
            logger.warning('Duplicate. data:\n{0}'.format(data))

    def chunks(self, list, length):
        for i in range(0, len(list), length):
            yield list[i:i + length]


class GoodsStatistician(Statistician):
    @log_time_with_name('GoodsStatistician.save')
    def save(self):
        m = self.mongodb

        c = m['d_{0}'.format(self.date)]
        # from pymongo import ASCENDING
        # c.create_index([('quantitySoldYesterday', ASCENDING)])
        # c.create_index([('quantitySoldLastWeek', ASCENDING)])
        # c.create_index([('categoryID', ASCENDING)])
        # c.create_index([('seller', ASCENDING)])
        # 初始化
        data = {}
        data['total_goods_num'] = 0
        data['sales_goods_num'] = 0
        data['total_sold_info'] = {}
        data['shop_sold_info'] = {}
        data['goods_sold_info'] = {}
        data['hot_category_ids_info'] = {}
        data['hot_goods_ids_info'] = []
        #
        data['total_goods_num'] = self.total_goods_num(c)
        data['sales_goods_num'] = self.sales_goods_num(c)
        data['total_sold_info'] = json.dumps(self.total_sold_info(c, data['sales_goods_num']))
        data['shop_sold_info'] = json.dumps(self.shop_sold_info(c))
        data['goods_sold_info'] = json.dumps(self.goods_sold_info(c, data['total_goods_num']))
        data['hot_category_ids_info'] = self.hot_category_ids_info(c, data['total_goods_num'])
        data['hot_goods_ids_info'] = json.dumps(self.hot_goods_ids_info(c))
        #
        self.insert_to_mysql(data)

    # @log_time_with_name('total_goods_num')
    def total_goods_num(self, collection):
        ''' 商品总数 '''
        return collection.count()

    # @log_time_with_name('sales_goods_num')
    def sales_goods_num(self, collection):
        ''' 有销量商品总数 '''
        return collection.find({"quantitySoldYesterday": {'$gt': 0}}).count()

    # @log_time_with_name('total_sold_info')
    def total_sold_info(self, collection, sales_goods_num):
        c = collection
        data = {}
        data['count'] = sales_goods_num
        result = c.aggregate([
            {'$match': {"quantitySoldYesterday": {'$gt': 0}}},
            {"$project": {
                "total_sold_info_money": {"$multiply": ["$quantitySoldYesterday", "$price"]},
                "_id": 0,
                "categoryID": 1,
                "quantitySold": 1, },
            },
        ])
        data['money'] = round(sum([i['total_sold_info_money'] for i in result]), 2)
        return data

    @log_time_with_name('shop_sold_info')
    def shop_sold_info(self, collection):
        ''' 店铺相关 '''
        c = collection
        data = {}
        result = c.aggregate([
            {'$match': {"quantitySoldYesterday": {'$gt': 0}}},
            {'$group': {'_id': '$seller', 'quantitySoldYesterday': {'$sum': '$quantitySoldYesterday'}}},
        ])
        # todo-1
        shop_num = self.redis.hlen('ebay:shop:count')
        data['shop_num'] = shop_num if shop_num > 0 else len(c.distinct('seller'))
        data['has_sold_count'] = 0
        data['has_sold_101'] = 0
        data['has_sold_61_100'] = 0
        data['has_sold_31_60'] = 0
        data['has_sold_11_30'] = 0
        data['has_sold_1_10'] = 0
        for i in result:
            data['has_sold_count'] += 1
            if i['quantitySoldYesterday'] > 0 and i['quantitySoldYesterday'] <= 10:
                data['has_sold_1_10'] += 1
            elif i['quantitySoldYesterday'] > 10 and i['quantitySoldYesterday'] <= 30:
                data['has_sold_11_30'] += 1
            elif i['quantitySoldYesterday'] > 30 and i['quantitySoldYesterday'] <= 60:
                data['has_sold_31_60'] += 1
            elif i['quantitySoldYesterday'] > 60 and i['quantitySoldYesterday'] <= 100:
                data['has_sold_61_100'] += 1
            elif i['quantitySoldYesterday'] > 100:
                data['has_sold_101'] += 1
        return data

    # @log_time_with_name('goods_sold_info')
    def goods_sold_info(self, collection, total_goods_num):
        ''' 商品相关 '''
        c = collection
        data = {}
        data['goods_num'] = total_goods_num
        data['has_sold_count'] = 0
        data['has_sold_101'] = 0
        data['has_sold_61_100'] = 0
        data['has_sold_31_60'] = 0
        data['has_sold_11_30'] = 0
        data['has_sold_1_10'] = 0

        data['has_sold_count'] = c.find({"quantitySoldYesterday": {'$gt': 0}}).count()
        data['has_sold_101'] = c.find({"quantitySoldYesterday": {'$gt': 100}}).count()
        data['has_sold_61_100'] = c.find({"quantitySoldYesterday": {'$gt': 60, '$lte': 100}}).count()
        data['has_sold_31_60'] = c.find({"quantitySoldYesterday": {'$gt': 30, '$lte': 61}}).count()
        data['has_sold_11_30'] = c.find({"quantitySoldYesterday": {'$gt': 10, '$lte': 30}}).count()
        data['has_sold_1_10'] = c.find({"quantitySoldYesterday": {'$gt': 0, '$lte': 10}}).count()

        # for i in c.find({"quantitySoldYesterday": {'$gt': 0}}):
        #     data['has_sold_count'] += 1
        #     if i['quantitySoldYesterday'] > 0 and i['quantitySoldYesterday'] <= 10:
        #         data['has_sold_1_10'] += 1
        #     elif i['quantitySoldYesterday'] > 10 and i['quantitySoldYesterday'] <= 30:
        #         data['has_sold_11_30'] += 1
        #     elif i['quantitySoldYesterday'] > 30 and i['quantitySoldYesterday'] <= 60:
        #         data['has_sold_31_60'] += 1
        #     elif i['quantitySoldYesterday'] > 60 and i['quantitySoldYesterday'] <= 100:
        #         data['has_sold_61_100'] += 1
        #     elif i['quantitySoldYesterday'] > 100:
        #         data['has_sold_101'] += 1
        return data

    # @log_time_with_name('hot_category_ids_info')
    def hot_category_ids_info(self, collection, total_goods_num):
        ''' 商品分类 '''
        # fixme 12w => 0.3s 有待性能优化
        result = collection.aggregate([{'$group': {'_id': '$categoryID', 'quantity': {'$sum': 1}}}])
        return {str(i['_id']): i['quantity'] for i in result if i['quantity'] > total_goods_num * 0.0001}

    # @log_time_with_name('hot_goods_ids_info')
    def hot_goods_ids_info(self, collection):
        ''' 周销量排行前二十商品 '''
        # fixme 12w => 0.4s 有待性能优化
        return [i['itemId'] for i in
                collection.find({"quantitySoldLastWeek": {'$gt': 0}}).sort('quantitySoldLastWeek').limit(20)]

    # @log_time_with_name('save_goods_statics')
    def insert_to_mysql(self, statics_data):
        print(statics_data['hot_category_ids_info'])
        # fixme 12w => 0.4s 有待性能优化
        cursor = self.mysql_cursor
        print(statics_data)
        # 获取分类名
        sql = "SELECT english_name, platform_category_id FROM erp_spider.erp_saas_goods_category WHERE platform_category_id IN ({0}) AND site=2;"
        cursor.execute(sql.format(','.join(statics_data['hot_category_ids_info'])))
        result = cursor.fetchall()
        # 组合分类名
        hot_category_ids_info = {
            i[1]: statics_data['hot_category_ids_info'][i[0]]
            for i in {r[1]: r[0] for r in result}.items()
        }
        statics_data['hot_category_ids_info'] = json.dumps(hot_category_ids_info)
        # 写入所有统计数据
        sql = "DELETE FROM erp_spider.goods_statistics WHERE `date`={0};".format(self.date)
        sql += """INSERT INTO erp_spider.goods_statistics (platform, `date`, total_goods_num, sales_goods_num, total_sold_info, shop_sold_info, goods_sold_info, hot_goods_ids_info, hot_category_ids_info)
                  VALUES (%(platform)s, %(date_)s, %(total_goods_num)s, %(sales_goods_num)s, %(total_sold_info)s, %(shop_sold_info)s, %(goods_sold_info)s, %(hot_goods_ids_info)s, %(hot_category_ids_info)s) """
        cursor.execute(sql, {
            'platform': 'ebay',
            'date_': self.date,
            'total_goods_num': statics_data['total_goods_num'],
            'sales_goods_num': statics_data['sales_goods_num'],
            'total_sold_info': statics_data['total_sold_info'],
            'shop_sold_info': statics_data['shop_sold_info'],
            'goods_sold_info': statics_data['goods_sold_info'],
            'hot_goods_ids_info': statics_data['hot_goods_ids_info'],
            'hot_category_ids_info': statics_data['hot_category_ids_info'],
        })
        self.mysql.commit()


class ShopStatistician(Statistician):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.execute_sql("TRUNCATE TABLE erp_spider.shop_statistics;")

    @log_time_with_name('ShopStatistician.save')
    def save(self, process=64):
        r = self.redis
        result = r.hvals('ebay:shop:basic')

        t1 = datetime.now()
        func = self.insert_to_mysql
        pool = Pool(process)
        for shop_list in self.chunks(result, 100):
            pool.apply_async(func, args=(shop_list,))
            # self.insert_to_mysql(shop_list)
        pool.close()
        pool.join()
        t2 = datetime.now()
        try:
            assert t2 - t1 > timedelta(0, 2, 0)  # 耗时太短, 大概率多线程执行异常
        except AssertionError:
            for shop_list in self.chunks(result, 100):
                self.insert_to_mysql(shop_list)

    @staticmethod
    def insert_to_mysql(shop_list, mysql=None, redis=None):
        redis = redis or db_redis()
        mysql = mysql or db_mysql()
        cursor = mysql.cursor()

        def shop_values(shop_list, redis=None):
            r = redis or db_redis()
            values = "(\'{shop_name}\', {shop_feedback_score}, {shop_feedback_percent}, {has_sold_count}, {count}, {total_sold}, {week_sold}, {last_week_sold}, {amount}, \'{shop_open_time}\', {weeks_inc_ratio})"
            for i in shop_list:
                shop = json.loads(str(i, encoding='utf8'))
                shop['count'] = int(r.hget('ebay:shop:count', shop['shop_name']) or 0)
                shop['week_sold'] = int(r.hget('ebay:shop:week_sold', shop['shop_name']) or 0)
                shop['last_week_sold'] = int(r.hget('ebay:shop:last_week_sold', shop['shop_name']) or 0)
                shop['has_sold_count'] = int(r.hget('ebay:shop:has_sold_count', shop['shop_name']) or 0)
                shop['total_sold'] = int(r.hget('ebay:shop:total_sold', shop['shop_name']) or 0)
                shop['amount'] = round(float(r.hget('ebay:shop:amount', shop['shop_name']) or 0),2)
                yield values.format(
                    shop_name=shop['shop_name'],
                    shop_feedback_score=shop['shop_feedback_score'],
                    shop_feedback_percent=shop['shop_feedback_percent'],
                    has_sold_count=shop['has_sold_count'],
                    count=shop['count'],
                    total_sold=shop['total_sold'],
                    week_sold=shop['week_sold'],
                    last_week_sold=shop['last_week_sold'],
                    amount=shop['amount'],
                    shop_open_time=shop['shop_open_time'],
                    weeks_inc_ratio=(shop['week_sold'] - shop['last_week_sold']) / (shop['last_week_sold'] + 1)
                )

        sql = "INSERT INTO erp_spider.shop_statistics (shop_name, shop_feedback_score, shop_feedback_percentage, sold_goods_count, total_goods_count, total_sold, weeks_sold, last_weeks_sold, amount, shop_open_time, weeks_inc_ratio) VALUES"
        sql += ','.join([i for i in shop_values(shop_list, redis)])

        try:
            cursor.execute(sql)
            mysql.commit()
        except pymysql.err.IntegrityError:
            logger.warning('Duplicate. sql:\n{0}'.format(sql))


def main():
    redis = db_redis()
    mongodb = db_mongodb('mongodb_remote')
    mysql = db_mysql()

    g = GoodsStatistician(redis=redis, mongodb=mongodb, mysql=mysql)
    g.save()

    s = ShopStatistician(redis=redis, mongodb=mongodb, mysql=mysql)
    s.save(process=64)


if __name__ == '__main__':
    main()
