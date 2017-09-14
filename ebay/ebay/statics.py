# statics
from .utils.common import date, previous_date, last_week
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
            m[c].update_one({'itemId': id}, {'$set': {filed: -1}})


def copy_sales_two_weeks_ago(day=None, mongodb=None):
    ''' 统计上上周销量 '''
    pass
