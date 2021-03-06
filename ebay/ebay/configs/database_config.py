# -*- coding: utf-8 -*-

config = {
    'mysql_local': {
        'host': '192.168.1.248',
        'database': 'erp_spider',
        'username': 'root',
        'password': 'root',
        'port': 3306,
    },
    'mysql_remote': {
        'host': '192.168.1.248',
        'database': 'erp_spider',
        'username': 'root',
        'password': 'root',
        'port': 3306,
    },
    'mongodb_remote': {
        'host': '192.168.1.253',
        'database': 'test_database',
        'port': 27017,
    },
    'mongodb_local': {
        'host': '192.168.1.140',
        'database': 'test_database',
        'port': 27017,
    },
    'redis': {
        'host': '192.168.1.253',
        'password': 'redis',
        'port': 6379,
    }
}

config['mongodb'] = config['mongodb_remote']
config['mysql'] = config['mysql_remote']
