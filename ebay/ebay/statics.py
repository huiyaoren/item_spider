from datetime import datetime

from .utils.common import date, previous_date, last_week, is_within_eight_weeks, is_within_six_mouths, previous_days
from .utils.data import db_mongodb, items_from_mongodb


def count_sales_yesterday(day=None, mongodb=None):
    ''' 统计昨日销量 '''
    m = mongodb or db_mongodb()
    day = day or date()
    c = 'd_{0}'.format(day)
    c_y = 'd_{0}'.format(previous_date(day))
    count_sales(c, c_y, m, 'quantitySoldYesterday')
    print('Count Sales Yesterday Done.')


def count_sales_last_week(day=None, mongodb=None):
    ''' 统计上周销量 '''
    m = mongodb or db_mongodb()
    day = day or date()
    c = 'd_{0}'.format(day)
    c_y = 'd_{0}'.format(last_week(day))
    count_sales(c, c_y, m, 'quantitySoldLastWeek')
    print('Count Sales Last Week Done.')


def count_sales(collection, collection_other_day, mongodb, filed):
    ''' 计算某天到指定日期间的销量并记录到当天数据的某字段中 '''
    m = mongodb
    c = collection
    c_y = collection_other_day
    for item in items_from_mongodb(c):
        id = item['itemId']
        item_y = m[c_y].find_one({'itemId': id})
        if item_y is not None:
            sold = int(item['quantitySold']) - int(item_y['quantitySold'])
            m[c].update_one({'itemId': id}, {'$set': {filed: sold}})
        else:
            m[c].update_one({'itemId': id}, {'$set': {filed: 0}})


def copy_sales_two_weeks_ago(day=None, mongodb=None):
    ''' 将上周数据中的上周销量复制到当天数据中 '''
    m = mongodb or db_mongodb()
    d = day or date()
    c = 'd_{0}'.format(d)
    c_y = 'd_{0}'.format(last_week(d))
    for item in items_from_mongodb(c):
        id = item['itemId']
        item_y = m[c_y].find_one({'itemId': id})
        if item_y is not None:
            sold = item_y.get('quantitySoldLastWeek', 0)
            m[c].update_one({'itemId': id}, {'$set': {'quantitySoldTwoWeeksAgo': sold}})
        else:
            m[c].update_one({'itemId': id}, {'$set': {'quantitySoldTwoWeeksAgo': 0}})
    print('Copy Sales Two Weeks Ago Done.')


def judge_is_new(day=None, mongodb=None):
    ''' 八周内新上架 且出过单'''
    m = mongodb or db_mongodb()
    d = day or date()
    c = 'd_{0}'.format(d)
    for item in items_from_mongodb(c):
        id = item['itemId']
        if is_within_eight_weeks(item['startTime']) and int(item['quantitySold']) > 0:
            m[c].update_one({'itemId': id}, {'$set': {'is_new': 1}})
        else:
            m[c].update_one({'itemId': id}, {'$set': {'is_new': 0}})
    print('Judge Is New Done.')


def judge_is_hot(day=None, mongodb=None):
    ''' 六个月内上架 总售出大于50 前7天至少有三天出单 '''
    m = mongodb or db_mongodb()
    d = day or date()
    c = 'd_{0}'.format(d)
    for item in items_from_mongodb(c):
        id = item['itemId']
        if is_within_six_mouths(item['startTime']) and int(item['quantitySold']) > 50 and is_had_sales_in_a_week(d, id,
                                                                                                                 3, m):
            m[c].update_one({'itemId': id}, {'$set': {'is_hot': 1}})
        else:
            m[c].update_one({'itemId': id}, {'$set': {'is_hot': 0}})
    print('Judge Is Hot Done.')

# fixme 以上函数将已被 Cleaner 替代

# fixme 此函数将成为 Cleaner 方法
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


class Cleaner():
    def __init__(self, date, mongodb):
        self.date = date
        self.mongodb = mongodb or db_mongodb()
        self.collection = self.mongodb['d_{0}'.format(date)]

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
        if is_within_six_mouths(item['startTime']) and int(item['quantitySold']) > 50 and is_had_sales_in_a_week(
                self.date, item['itemId'], 3, self.mongodb):
            return 1
        else:
            return 0

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
        t0 = datetime.now()
        data['isHot'] = self.is_hot(item)
        t1 = datetime.now()
        print('t1-t2', t1-t0)
        data['isNew'] = self.is_new(item)
        t2 = datetime.now()
        print('t1-t2', t2-t1)
        data['quantitySoldLastWeek'] = self.sales_last_week(item)[0]
        t3 = datetime.now()
        print('t1-t2', t3-t2)
        data['quantitySoldTwoWeeksAgo'] = self.sales_last_week(item)[1]
        t4 = datetime.now()
        print('t1-t2', t4-t3)
        data['quantitySoldYesterday'] = self.sales_yesterday(item)
        t5 = datetime.now()
        print('t1-t2', t5-t4)
        return data
