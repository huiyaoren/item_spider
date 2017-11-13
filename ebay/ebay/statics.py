import json
from datetime import datetime

from .tests.time_recoder import log_time_with_name
from .utils.common import date, previous_date, last_week, is_within_eight_weeks, is_within_six_mouths, previous_days
from .utils.data import db_mongodb, items_from_mongodb, db_redis


class Cleaner():
    def __init__(self, date, mongodb):
        self.date = date
        self.mongodb = mongodb or db_mongodb()
        self.collection = self.mongodb['d_{0}'.format(date)]
        self.redis = db_redis()

    def item_someday(self, item_id, date):
        ''' 返回指定日期的指定商品数据 '''
        c = self.mongodb['d_{0}'.format(date)]
        item = c.find_one({'itemId': item_id})
        return item

    def sales_yesterday(self, item):
        ''' 返回指定商品的昨日数据 '''
        id = item['itemId']
        date = previous_date(self.date)
        item_y = self.item_someday(id, date)
        if item_y is None:
            return 0
        sold_yesterday = int(item['quantitySold']) - int(item_y['quantitySold'])
        return sold_yesterday

    def sales_last_week(self, item):
        ''' 返回指定商品的上周统计数据 '''
        id = item['itemId']
        date = last_week(self.date)
        item_y = self.item_someday(id, date)
        if item_y is None:
            return 0, 0
        sold_last_week = int(item['quantitySold']) - int(item_y['quantitySold'])
        sold_two_weeks_ago = item_y.get('quantitySoldLastWeek', 0)
        return sold_last_week, sold_two_weeks_ago

    def is_new(self, item):
        ''' 指定商品是否为新品 '''
        if is_within_eight_weeks(item['startTime']) and int(item['quantitySold']) > 0:
            return 1
        else:
            return 0

    def is_hot(self, item):
        ''' 指定商品是否为爆款 '''
        if is_within_six_mouths(item['startTime']) and int(
                item['quantitySold']) > 50 and Cleaner.is_had_sales_in_a_week(
            self.date, item['itemId'], 3, self.mongodb):
            return 1
        else:
            return 0

    def category_id_top(self, item):
        id = item['categoryID']
        top = self.redis.hget('ebay:top_category_id', int(id))
        print(top)
        return top

    @staticmethod
    def is_had_sales_in_a_week(date, item_id, days_have_sales=3, mongodb=None):
        ''' 商品一周内有销量的天数是否达到指定值 '''
        m = mongodb or db_mongodb()
        days = days_have_sales
        sales = set([])
        for i in range(7, -1, -1):
            d = previous_days(date, i)
            c = 'd_{0}'.format(d)
            item = m[c].find_one()
            if item is not None:
                sales.add(item['quantitySold'])
                if len(sales) > days:
                    return True
        return False

    def clean(self, item_id):
        ''' 统计指定商品数据 '''
        c = self.collection
        item = c.find_one({'itemId': item_id})
        if item is None:
            return
        data = self.data_cleaned(item)
        print(data)
        if data is None:
            return
        self.collection.update_one({'itemId': item_id}, {'$set': data})

    def data_cleaned(self, item):
        ''' 返回指定商品的统计数据 '''
        data = {}
        data['isHot'] = self.is_hot(item)
        data['isNew'] = self.is_new(item)
        data['quantitySoldLastWeek'], data['quantitySoldTwoWeeksAgo'] = self.sales_last_week(item)
        data['quantitySoldYesterday'] = self.sales_yesterday(item)
        data['topCategoryID'] = self.category_id_top(item)
        self.redis.hset('ebay:log', item['itemId'], data)
        return data

    def add_up_shop(self, item_cleaned):
        r = self.redis
        i = item_cleaned
        seller = i.get('seller')
        if seller is None:
            return
        # 基本信息
        shop = {}
        shop['shop_name'] = i['seller']
        shop['shop_open_time'] = ' '.join([i['registrationDate'][0:10], i['registrationDate'][11:19]])
        shop['shop_feedback_score'] = i['feedbackScore']
        shop['shop_feedback_percent'] = i['positiveFeedbackPercent']
        r.hsetnx('ebay:shop:basic', seller, json.dumps(shop))
        # 店铺商品总数
        r.hincrby('ebay:shop:count', seller, 1)
        # 店铺日销量
        if i['quantitySoldYesterday'] > 0:
            # 店铺单日有销量商品总数
            r.hincrby('ebay:shop:has_sold_count', seller, 1)
            # 店铺日销量
            r.hincrby('ebay:shop:total_sold', seller, i['quantitySoldYesterday'])
            # 店铺日销售额
            r.hincrbyfloat('ebay:shop:amount', seller, i['quantitySoldYesterday'] * i['price'])
        # 店铺周销量
        if i['quantitySoldLastWeek'] > 0:
            r.hincrby('ebay:shop:week_sold', seller, i['quantitySoldLastWeek'])
        # 店铺上周销量
        if i['quantitySoldTwoWeeksAgo'] > 0:
            r.hincrby('ebay:shop:last_week_sold', seller, i['quantitySoldTwoWeeksAgo'])

    def add_up(self, item_cleaned):
        # todo 弃用
        r = self.redis
        # start = datetime.now()
        i = item_cleaned
        # i = {'date': '20171016', 'site': 'US', 'shipToLocations': 'US', 'storeURL': None, 'registrationDate': '2012-10-04T03:52:32.000Z', 'quantitySold': 1, 'seller': 'yx-123', 'categoryID': '58730', 'startTime': '2017-10-08T23:54:35.000Z', 'quantitySoldYesterday': 0, 'feedbackScore': 126, 'itemId': '162705047456', 'positiveFeedbackPercent': 100.0, 'price': 45.0, 'isNew': 0, 'title': 'DREAM WITH ME (OSTRICH PILLOW)', 'viewItemURL': 'http://www.ebay.com/itm/DREAM-ME-OSTRICH-PILLOW-/162705047456', 'hitCount': 10, 'image': 'https://i.ebayimg.com/00/s/MTYwMFg5MDA=/z/cIEAAOSwygJXht7s/$_1.JPG?set_id=880000500F', 'otherImages': ['https://i.ebayimg.com/00/s/MTYwMFg5MDA=/z/cIEAAOSwygJXht7s/$_1.JPG?set_id=880000500F', 'https://i.ebayimg.com/00/s/MTYwMFg5MDA=/z/FRgAAOSwyKxXht7w/$_1.JPG?set_id=880000500F', 'https://i.ebayimg.com/00/s/MTYwMFg5MDA=/z/Av0AAOSw0kNXht7z/$_1.JPG?set_id=880000500F'], 'quantitySoldLastWeek': 0, 'quantitySoldTwoWeeksAgo': 0, 'currency': 'USD', 'isHot': 0}
        print(i)
        sold = i.get('quantitySold', 0)
        # 全站销售
        if sold > 0:
            r.zincrby('ebay:sold_info:total', 'money', sold * i['price'])
        # 店铺销售信息
        if sold > 0:
            r.zincrby('ebay:sold_info:shop', i.get('seller', '_'), 1)
        else:
            r.zincrby('ebay:sold_info:shop', i.get('seller', '_'), 0)
        # 热门商品分类ids信息
        if sold > 0:
            r.zincrby('ebay:sold_info:category', i.get('categoryID', '_'), 1)
        else:
            r.zincrby('ebay:sold_info:category', i.get('categoryID', '_'), 0)
        # 商品销售信息
        if sold > 100:
            r.zincrby('ebay:sold_info:goods', 'has_sold_100', 1)
        elif sold > 60:
            r.zincrby('ebay:sold_info:goods', 'has_sold_60_100', 1)
        elif sold > 30:
            r.zincrby('ebay:sold_info:goods', 'has_sold_31_60', 1)
        elif sold > 10:
            r.zincrby('ebay:sold_info:goods', 'has_sold_11_30', 1)
        elif sold > 0:
            r.zincrby('ebay:sold_info:goods', 'has_sold_1_10', 1)
            r.zincrby('ebay:sold_info:goods', 'has_sold_count', 1)
