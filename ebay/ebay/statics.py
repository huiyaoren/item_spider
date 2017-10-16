from datetime import datetime

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
        # todo-1 全站统计
        self.add_up(data)
        return data

    def add_up(self, item_cleaned):
        r = self.redis
        # start = datetime.now()
        i = item_cleaned
        # i = {'date': '20171016', 'site': 'US', 'shipToLocations': 'US', 'storeURL': None, 'registrationDate': '2012-10-04T03:52:32.000Z', 'quantitySold': 1, 'seller': 'yx-123', 'categoryID': '58730', 'startTime': '2017-10-08T23:54:35.000Z', 'quantitySoldYesterday': 0, 'feedbackScore': 126, 'itemId': '162705047456', 'positiveFeedbackPercent': 100.0, 'price': 45.0, 'isNew': 0, 'title': 'DREAM WITH ME (OSTRICH PILLOW)', 'viewItemURL': 'http://www.ebay.com/itm/DREAM-ME-OSTRICH-PILLOW-/162705047456', 'hitCount': 10, 'image': 'https://i.ebayimg.com/00/s/MTYwMFg5MDA=/z/cIEAAOSwygJXht7s/$_1.JPG?set_id=880000500F', 'otherImages': ['https://i.ebayimg.com/00/s/MTYwMFg5MDA=/z/cIEAAOSwygJXht7s/$_1.JPG?set_id=880000500F', 'https://i.ebayimg.com/00/s/MTYwMFg5MDA=/z/FRgAAOSwyKxXht7w/$_1.JPG?set_id=880000500F', 'https://i.ebayimg.com/00/s/MTYwMFg5MDA=/z/Av0AAOSw0kNXht7z/$_1.JPG?set_id=880000500F'], 'quantitySoldLastWeek': 0, 'quantitySoldTwoWeeksAgo': 0, 'currency': 'USD', 'isHot': 0}

        sold = i.get('quantitySold', 0)
        if sold > 0:
            r.zincrby('ebay:sold_info:total', 'count', 1)
            r.zincrby('ebay:sold_info:total', 'money', sold * i['price'])
            r.zincrby('ebay:sold_info:goods', 'has_sold_count', 1)
            r.zincrby('ebay:sold_info:shop', i.get('seller', '_'), 1)
        else:
            r.zincrby('ebay:sold_info:shop', i.get('seller', '_'), 0)

        if sold > 100:
            r.zincrby('ebay:sold_info:goods', 'has_sold_100', 1)
        elif sold > 60:
            r.zincrby('ebay:sold_info:goods', 'has_sold_60_100', 1)
        elif sold > 30:
            r.zincrby('ebay:sold_info:goods', 'has_sold_31_60', 1)
        elif sold > 10:
            r.zincrby('ebay:sold_info:goods', 'has_sold_11_30', 1)
        else:
            r.zincrby('ebay:sold_info:goods', 'has_sold_1_10', 1)

        # end = datetime.now()
        # print(end - start)




