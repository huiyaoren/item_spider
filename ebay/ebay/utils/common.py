# -*- coding: utf-8 -*-
import six
from datetime import datetime, timedelta


def date():
    return datetime.now().strftime("%Y%m%d")


def is_within_eight_weeks(utc_date):
    u = utc_date
    y = u[0:4]
    m = u[5:7]
    d = u[8:10]
    h = u[11:13]
    i = u[14:16]
    s = u[17:19]
    return (datetime.now() - datetime(int(y), int(m), int(d), int(h), int(i), int(s))) < timedelta(days=7 * 8)


def is_within_six_mouths(utc_date):
    u = utc_date
    y = u[0:4]
    m = u[5:7]
    d = u[8:10]
    h = u[11:13]
    i = u[14:16]
    s = u[17:19]
    return (datetime.now() - datetime(int(y), int(m), int(d), int(h), int(i), int(s))) < timedelta(days=30 * 6)


def last_week(date):
    y = date[0:4]
    m = date[4:6]
    d = date[6:8]
    date = datetime(int(y), int(m), int(d)) - timedelta(days=7)
    return date.strftime("%Y%m%d")


def previous_date(date):
    y = date[0:4]
    m = date[4:6]
    d = date[6:8]
    date = datetime(int(y), int(m), int(d)) - timedelta(days=1)
    return date.strftime("%Y%m%d")


def previous_days(date, count):
    y = date[0:4]
    m = date[4:6]
    d = date[6:8]
    date = datetime(int(y), int(m), int(d)) - timedelta(days=count)
    return date.strftime("%Y%m%d")


def clean_item_id(item_id):
    '''
    :param item_id: v1|292191373015|591122882367
    :return: 292191373015
    '''
    i = item_id.split('|')[1]
    return i


def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s


if __name__ == '__main__':
    date()
