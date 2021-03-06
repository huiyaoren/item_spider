import json
import logging
import traceback
from datetime import datetime, timedelta
from multiprocessing.pool import Pool

import pymongo
import pymysql

from ebay.ebay.sqls.sqls import SQL
from ebay.ebay.tests.time_recoder import log_time_with_name
from ebay.ebay.utils.common import date
from ebay.ebay.utils.data import db_redis, db_mongodb, db_mysql, create_table_in_mysql

logger = logging.getLogger(__name__)

'''
商品数据统计
'''


class Statistician():
    def __init__(self, redis=None, mongodb=None, mysql=None, datetime=None):
        self.redis = redis or db_redis()
        self.mongodb = mongodb or db_mongodb('mongodb_remote')
        self.mysql = mysql or db_mysql()
        self.mysql_cursor = self.mysql.cursor()
        self.date = datetime or date()
        try:
            self.mysql_local = db_mysql('mysql_local')
            self.mysql_cursor_local = self.mysql_local.cursor()
        except:
            pass
        self.start_statistician()

    def start_statistician(self):
        pass

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
    def start_statistician(self):
        pass

    @log_time_with_name('GoodsStatistician.save')
    def save(self):
        m = self.mongodb
        c = m['d_{0}'.format(self.date)]
        # 保证索引已生成
        print('Start goods statistic...')
        print('Check index...')
        c.create_index([('topCategoryID', pymongo.ASCENDING)])
        c.create_index([('quantitySoldYesterday', pymongo.DESCENDING)])
        c.create_index([('quantitySoldLastWeek', pymongo.DESCENDING)])
        # 数据初始化
        data = {}
        data['total_goods_num'] = 0
        data['sales_goods_num'] = 0
        data['total_sold_info'] = '{}'
        data['shop_sold_info'] = '{}'
        data['goods_sold_info'] = '{}'
        data['hot_category_ids_info'] = {'0': '0'}
        data['hot_goods_ids_info'] = '[]'
        # 开始统计
        print('Start statistics...')
        data['total_goods_num'] = self.total_goods_num(c)
        data['sales_goods_num'] = self.sales_goods_num(c)
        data['total_sold_info'] = json.dumps(self.total_sold_info(c))
        data['shop_sold_info'] = json.dumps(self.shop_sold_info(c))
        data['goods_sold_info'] = json.dumps(self.goods_sold_info(c, data['total_goods_num']))
        data['hot_category_ids_info'] = self.hot_category_ids_info(c)
        data['hot_goods_ids_info'] = json.dumps(self.hot_goods_ids_info(c))
        # 数据写入
        try:
            self.insert_to_mysql(statics_data=data)
            self.insert_to_mysql(statics_data=data, cursor=self.mysql_cursor_local, mysql=self.mysql_local)
        except Exception as e:
            info = traceback.format_exc()
            logger.warning('Insert to mysql error... \n\nException: {0}\n{1}\n'.format(e, info))

    @log_time_with_name('total_goods_num')
    def total_goods_num(self, collection):
        ''' 商品总数 '''
        return collection.count()

    @log_time_with_name('sales_goods_num')
    def sales_goods_num(self, collection):
        ''' 有销售商品总量 '''
        return collection.find({"quantitySoldYesterday": {'$gt': 0}}).count()

    @log_time_with_name('total_sold_info')
    def total_sold_info(self, collection):
        ''' 单天销量与单天销售额 '''
        c = collection
        data = {}
        # 单天销量
        result = c.aggregate([
            {'$match': {"quantitySoldYesterday": {'$gt': 0}}},
            {'$group': {'_id': 0, 'total_sold_info_count': {'$sum': "$quantitySoldYesterday"}}}
        ])
        data['count'] = 0
        for r in result:
            data['count'] = r.get('total_sold_info_count')
        # 单天销售额
        result = c.aggregate([
            {'$match': {"quantitySoldYesterday": {'$gt': 0}}},
            {'$group': {'_id': 0,
                        'total_sold_info_money': {'$sum': {"$multiply": ["$quantitySoldYesterday", "$price"]}}}}
        ])
        data['money'] = 0
        for r in result:
            data['money'] = r.get('total_sold_info_money')
        #
        return data

    @log_time_with_name('shop_sold_info')
    def shop_sold_info(self, collection):
        ''' 店铺相关 '''
        c = collection
        data = {}
        result = c.aggregate([
            {'$match': {"quantitySoldLastWeek": {'$gt': 0}}},
            {'$group': {'_id': '$seller', 'quantitySoldLastWeek': {'$sum': '$quantitySoldLastWeek'}}},
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
            if i['quantitySoldLastWeek'] > 0 and i['quantitySoldLastWeek'] <= 10:
                data['has_sold_1_10'] += 1
            elif i['quantitySoldLastWeek'] > 10 and i['quantitySoldLastWeek'] <= 30:
                data['has_sold_11_30'] += 1
            elif i['quantitySoldLastWeek'] > 30 and i['quantitySoldLastWeek'] <= 60:
                data['has_sold_31_60'] += 1
            elif i['quantitySoldLastWeek'] > 60 and i['quantitySoldLastWeek'] <= 100:
                data['has_sold_61_100'] += 1
            elif i['quantitySoldLastWeek'] > 100:
                data['has_sold_101'] += 1
        return data

    @log_time_with_name('goods_sold_info')
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

        data['has_sold_count'] = c.find({"quantitySoldLastWeek": {'$gt': 0}}).count()
        data['has_sold_101'] = c.find({"quantitySoldLastWeek": {'$gt': 100}}).count()
        data['has_sold_61_100'] = c.find({"quantitySoldLastWeek": {'$gt': 60, '$lte': 100}}).count()
        data['has_sold_31_60'] = c.find({"quantitySoldLastWeek": {'$gt': 30, '$lte': 61}}).count()
        data['has_sold_11_30'] = c.find({"quantitySoldLastWeek": {'$gt': 10, '$lte': 30}}).count()
        data['has_sold_1_10'] = c.find({"quantitySoldLastWeek": {'$gt': 0, '$lte': 10}}).count()

        return data

    @log_time_with_name('hot_category_ids_info')
    def hot_category_ids_info(self, collection):
        ''' 商品分类 '''
        hot_category_ids_info = collection.aggregate([
            {'$match': {"quantitySoldLastWeek": {'$gt': 0}, }},
            {'$group': {'_id': "$topCategoryID", 'sold': {'$sum': "$quantitySoldLastWeek"}}}
        ])
        result = {
            str(category_data['_id']): category_data['sold']
            for category_data in hot_category_ids_info
        }
        return result

    @log_time_with_name('hot_goods_ids_info')
    def hot_goods_ids_info(self, collection):
        ''' 周销量排行前二十商品 '''
        # fixme 12w => 0.4s 有待性能优化
        return [
            str(i['itemId']) for i in collection.find(
                {"quantitySoldLastWeek": {'$gt': 1000}}
            ).sort(
                'quantitySoldLastWeek', pymongo.DESCENDING
            ).limit(20)
        ]

    @log_time_with_name('save_goods_statics')
    def insert_to_mysql(self, statics_data=None, cursor=None, mysql=None):
        cursor = cursor or self.mysql_cursor
        mysql = mysql or self.mysql
        # 获取分类名
        sql = "SELECT english_name, platform_category_id FROM erp_spider.erp_saas_goods_category WHERE platform_category_id IN ({0}) AND site=2;"
        cursor.execute(sql.format(','.join(statics_data['hot_category_ids_info'])))
        result = cursor.fetchall()
        # 组合分类名
        hot_category_ids_info = {
            i[1]: statics_data['hot_category_ids_info'][i[0]]
            for i in {r[1]: r[0] for r in result}.items()
        }
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
            'hot_category_ids_info': json.dumps(hot_category_ids_info),
        })
        mysql.commit()


class ShopStatistician(Statistician):
    def start_statistician(self):
        create_table_in_mysql(self.date, SQL['shop_statistics'])

    def is_not_empty(self):
        ''' 判断当天商店统计数据是否有效 '''
        redis = self.redis
        if redis.hlen('ebay:shop:basic') > 100000:
            return 1
        else:
            return 0

    @log_time_with_name('ShopStatistician.save')
    def save(self, process=64):
        r = self.redis
        print('Get shop data...')
        result = r.hvals('ebay:shop:basic')
        #
        print('Start shop statistic...')
        t1 = datetime.now()
        func = self.insert_to_mysql
        pool = Pool(process)
        for shop_list in self.chunks(result, 1000):
            pool.apply_async(func, args=(shop_list,))
            # self.insert_to_mysql(shop_list)
        pool.close()
        pool.join()
        t2 = datetime.now()
        #
        try:
            assert t2 - t1 > timedelta(0, 2, 0)  # 耗时太短, 大概率多进程执行异常
        except AssertionError:
            print('AssertionError...')
            print('Start plan B...')
            for shop_list in self.chunks(result, 100):
                self.insert_to_mysql(shop_list)

    @staticmethod
    def insert_to_mysql(shop_list, mysql=None, redis=None):
        redis = redis or db_redis()
        mysql = mysql or db_mysql()
        cursor = mysql.cursor()

        #
        def shop_values(shop_list, redis=None):
            r = redis or db_redis()
            for i in shop_list:
                shop = json.loads(str(i, encoding='utf8'))
                shop['count'] = int(r.hget('ebay:shop:count', shop['shop_name']) or 0)
                shop['week_sold'] = int(r.hget('ebay:shop:week_sold', shop['shop_name']) or 0)
                shop['last_week_sold'] = int(r.hget('ebay:shop:last_week_sold', shop['shop_name']) or 0)
                shop['has_sold_count'] = int(r.hget('ebay:shop:has_sold_count', shop['shop_name']) or 0)
                shop['total_sold'] = int(r.hget('ebay:shop:total_sold', shop['shop_name']) or 0)
                shop['amount'] = round(float(r.hget('ebay:shop:amount', shop['shop_name']) or 0), 2)
                yield {
                    'shop_name': shop['shop_name'],
                    'shop_feedback_score': shop['shop_feedback_score'],
                    'shop_feedback_percentage': shop['shop_feedback_percent'],
                    'sold_goods_count': shop['has_sold_count'],
                    'total_goods_count': shop['count'],
                    'total_sold': shop['total_sold'],
                    'weeks_sold': shop['week_sold'],
                    'last_weeks_sold': shop['last_week_sold'],
                    'amount': shop['amount'],
                    'shop_open_time': shop['shop_open_time'],
                    'weeks_inc_ratio': (shop['week_sold'] - shop['last_week_sold']) / (shop['last_week_sold'] + 1)
                }

        #
        sql = """
            INSERT INTO erp_spider.shop_statistics_{0} (shop_name, shop_feedback_score, shop_feedback_percentage, sold_goods_count, total_goods_count, total_sold, weeks_sold, last_weeks_sold, amount, shop_open_time, weeks_inc_ratio ) 
            VALUES (%(shop_name)s, %(shop_feedback_score)s, %(shop_feedback_percentage)s, %(sold_goods_count)s, %(total_goods_count)s, %(total_sold)s, %(weeks_sold)s, %(last_weeks_sold)s, %(amount)s, %(shop_open_time)s, %(weeks_inc_ratio)s)
        """.format(date())
        data = [i for i in shop_values(shop_list, redis)]
        #
        try:
            cursor.executemany(sql, data)
            mysql.commit()
        except pymysql.err.IntegrityError:
            logger.warning('Duplicate. sqls:\n{0}'.format(data[0]))


def main():
    redis = db_redis()
    mongodb = db_mongodb('mongodb_remote')
    mysql = db_mysql('mysql_remote')
    datetime = date()
    # 全站商品数据统计
    g = GoodsStatistician(redis=redis, mongodb=mongodb, mysql=mysql, datetime=datetime)
    g.save()
    # 全站店铺数据统计
    s = ShopStatistician(redis=redis, mongodb=mongodb, mysql=mysql, datetime=datetime)
    s.save(process=32)


if __name__ == '__main__':
    main()
