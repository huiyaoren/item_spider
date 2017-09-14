# -*- coding: utf-8 -*-
import six
from datetime import datetime, timedelta


def date():
    return datetime.now().strftime("%Y%m%d")


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
