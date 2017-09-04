# -*- coding: utf-8 -*-
from datetime import datetime


def date():
    return datetime.now().strftime("%Y%m%d")


def next_date(date):
    # todo 后一天日期
    pass


def previous_date(date):
    # todo 前一天日期
    pass


def clean_item_id(item_id='v1|292191373015|591122882367'):
    '''
    :param item_id: v1|292191373015|591122882367
    :return: 292191373015
    '''
    i = item_id.split('|')[1]
    return i


if __name__ == '__main__':
    date()
