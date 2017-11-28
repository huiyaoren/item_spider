import json
import traceback
from datetime import datetime
import logging

from .tests.time_recoder import log_time_with_name
from .utils.common import date, previous_date, last_week, is_within_eight_weeks, is_within_six_mouths, previous_days
from .utils.data import db_mongodb, items_from_mongodb, db_redis

logger = logging.getLogger(__name__)


class Cleaner():
    def __init__(self, date, mongodb):
        self.date = date
        self.mongodb = mongodb or db_mongodb('mongodb_remote')
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

    def is_hot(self, item, record):
        ''' 指定商品是否为爆款 '''
        date_list = sorted(record['sold'].keys(), reverse=True)[:7]
        if is_within_six_mouths(item['startTime']) \
                and int(item['quantitySold']) > 50 \
                and len(set(record['sold'][d] for d in date_list if record['sold'][d] > 0)) > 3:
            # and Cleaner.is_had_sales_in_a_week(self.date, item['itemId'], 3, self.mongodb):
            return 1
        else:
            return 0

    def variations(self, item):
        variations = item['variations']
        if variations is None:
            return json.dumps(0)

        try:
            # 图片列表转换为图片字符串
            if variations.get('Pictures') is not None:
                if (isinstance(variations['Pictures']['VariationSpecificPictureSet'], list)):
                    for key, set in enumerate(variations['Pictures']['VariationSpecificPictureSet']):
                        if isinstance(set['PictureURL'], list):
                            variations['Pictures']['VariationSpecificPictureSet'][key]['PictureURL'] = \
                                variations['Pictures']['VariationSpecificPictureSet'][key]['PictureURL'][0]
                else:
                    if isinstance(variations['Pictures']['VariationSpecificPictureSet']['PictureURL'], list):
                        variations['Pictures']['VariationSpecificPictureSet']['PictureURL'] = \
                            variations['Pictures']['VariationSpecificPictureSet']['PictureURL'][0]

            # 筛选键值
            for key, var in enumerate(variations['Variation']):
                variations['Variation'][key] = {
                    'SKU': var['SKU'],
                    'StartPrice': var['StartPrice'],
                    'Quantity': var['Quantity'],
                    'VariationSpecifics': var['VariationSpecifics']['NameValueList'] if isinstance(
                        var['VariationSpecifics']['NameValueList'], list) else [
                        var['VariationSpecifics']['NameValueList']],
                    'SellingStatus': var['SellingStatus'],
                }

            variations['VariationSpecificsSet'] = variations['VariationSpecificsSet']['NameValueList'] if isinstance(
                variations['VariationSpecificsSet']['NameValueList'], list) else [
                variations['VariationSpecificsSet']['NameValueList']]

        except Exception as e:
            info = traceback.format_exc()
            logger.warning("Unknown Error While Get Variations Data. Exception: \n{0}\n{1}".format(e, info))
            variations = 0

        return json.dumps(variations)

    def category_id_top(self, item):
        id = item['categoryID']
        top = self.redis.hget('ebay:top_category_id', id)
        return int(top)

    def record_14_days(self, item):
        record = {'sold': {}, 'price': {}, 'hit': {}, 'sold_yesterday': 0, }
        # 1. get record of item yesterday
        id = item['itemId']
        date = self.date
        item_y = self.item_someday(id, previous_date(date))
        if item_y is not None:
            r = item_y.get('record')
            record = json.loads(r) if r is not None else record
            record['sold_yesterday'] = int(item['quantitySold']) - int(item_y['quantitySold'])

        # * 避免出现漏失一天数据导致的记录丢失 向前继续查找 record 并添加到新 record 中 '''
        if record['price'] == {}:
            for i in range(14):
                date = previous_date(date)
                item_y = self.item_someday(id, date) or {}
                if item_y.get('record') is not None:
                    r = item_y.get('record')
                    r = json.loads(r) if r is not None else record
                    record['sold'].update(r.get('recordSold', {}))
                    record['price'].update(r.get('recordPrice', {}))
                    record['hit'].update(r.get('recordHit', {}))
                    break
                else:
                    record['sold'].update({date: item_y.get('quantitySoldYesterday', 0)})
                    record['price'].update({date: item_y.get('price', 0)})
                    record['hit'].update({date: item_y.get('hitCount', 0)})
        # 2. old record add record_of_today(sold, hit , price)
        record['sold'].update({self.date: record['sold_yesterday']})
        record['price'].update({self.date: item.get('price', 0.00)})
        record['hit'].update({self.date: item.get('hitCount', 0)})
        # 3. old record delete record_14_days_ago if(len > 14)
        if len(record['sold']) > 14:
            keys = sorted(record['sold'].keys(), reverse=True)[14:]
            for key in keys:
                record['sold'].pop(key)
                record['price'].pop(key)
                record['hit'].pop(key)
        # 4. old record become new record and return
        sold_yesterday = record['sold_yesterday']
        record.pop('sold_yesterday')
        return record, sold_yesterday

    @staticmethod
    def is_had_sales_in_a_week(date, item_id, days_have_sales=3, mongodb=None):
        ''' 商品一周内有销量的天数是否达到指定值 '''
        # fixme-已弃用
        m = mongodb or db_mongodb()
        days = days_have_sales
        sales = set([])
        for i in range(7, -1, -1):
            d = previous_days(date, i)
            c = 'd_{0}'.format(d)
            item = m[c].find_one({'itemId': item_id})
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

    @log_time_with_name('data_cleaned')
    def data_cleaned(self, item):
        ''' 返回指定商品的统计数据 '''
        data = {}
        data['quantitySoldLastWeek'], data['quantitySoldTwoWeeksAgo'] = self.sales_last_week(item)
        data['topCategoryID'] = self.category_id_top(item)
        record, sold_yesterday = self.record_14_days(item)
        # data['quantitySoldYesterday'] = self.sales_yesterday(item)
        data['quantitySoldYesterday'] = sold_yesterday
        data['record'] = json.dumps(record)
        data['isHot'] = self.is_hot(item, record)
        data['isNew'] = self.is_new(item)
        data['variations'] = self.variations(item)
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
