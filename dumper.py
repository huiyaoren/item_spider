import os
from datetime import datetime
from multiprocessing.pool import Pool

import sys

from ebay.ebay.tests.time_recoder import log_time_with_name

'''
定时数据库备份
'''

class Dumper():
    def __init__(self, date=None):
        self.date = date or datetime.now().strftime("%Y%m%d")

    def chunks(self, list, length):
        for i in range(0, len(list), length):
            yield list[i:i + length]


class MysqlDumper(Dumper):
    def __init__(self, table=None, source=None, target=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_source = source
        self.config_target = target
        self.table = table

    @log_time_with_name('MysqlDumper.dump')
    def dump(self, table=None):
        config = self.config_source
        command_dump = 'mysqldump -q -h{host} -u{username} -p{password} {database} {table} > {table}.sql'.format(
            host=config['host'],
            username=config['username'],
            password=config['password'],
            database=config['database'],
            table=table or self.table
        )
        print(command_dump)
        os.system(command_dump)

    @log_time_with_name('MysqlDumper.import')
    def import_(self, table=None):
        config = self.config_target
        command_dump = 'mysql -h{host} -u{username} -p{password} {database} < {table}.sql'.format(
            host=config['host'],
            username=config['username'],
            password=config['password'],
            database=config['database'],
            table=table or self.table
        )
        print(command_dump)
        os.system(command_dump)

    @log_time_with_name('MysqlDumper.run')
    def run(self, table=None):
        self.dump(table)
        self.import_(table)


class MongodbDumper(Dumper):
    def __init__(self, source=None, target=None, collection=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_source = source
        self.config_target = target
        self.collection = collection

    @log_time_with_name('MongodbDumper.dump')
    def dump(self, collection=None):
        config = self.config_source
        command_dump = 'mongodump -h {host} -d {database} -c {collection} -o dump'.format(
            host=config['host'],
            database=config['database'],
            collection=collection or self.collection
        )
        print(command_dump)
        os.system(command_dump)

    @log_time_with_name('MongodbDumper.import')
    def import_(self, collection=None):
        config = self.config_target
        command_dump = r'mongorestore -h {host} -d {database} -c {collection}  --dir dump\{database}\{collection}.bson'.format(
            host=config['host'],
            database=config['database'],
            collection=collection or self.collection
        )
        print(command_dump)
        os.system(command_dump)

    @log_time_with_name('MongodbDumper.run')
    def run(self, collection=None):
        self.dump(collection)
        self.import_(collection)

# todo 修改数据库配置
def dump_mysql(table):
    source = {
        'host': '125.77.23.94',
        'database': 'erp_spider',
        'username': 'erp_spider',
        'password': 'jb6KPZmd6d',
        'port': 3306,
    }
    target = {
        'host': '192.168.1.248',
        'database': 'erp_spider',
        'username': 'root',
        'password': 'root',
        'port': 3306,
    }
    mysql_dumper = MysqlDumper(target=target, source=source)
    mysql_dumper.run(table)


def dump_mongodb(collection):
    source = {
        'host': '192.168.1.253',
        'database': 'test_database',
        'port': 27017,
    }
    target = {
        'host': '192.168.1.253',
        'database': 'test_database',
        'port': 27017,
    }
    mongodb_dumper = MongodbDumper(source=source, target=target, )
    mongodb_dumper.dump(collection)


@log_time_with_name('MongodbDumper.import')
def main():
    args = dict(enumerate(sys.argv))
    day = args.get(1) or datetime.now().strftime("%Y%m%d")
    if len(day) != 8:
        raise Exception
    print('date={0}'.format(day))
    print('Start dumper...')

    goods = 'goods_{0}'.format(day)
    new = 'new_goods_{0}'.format(day)
    hot = 'hot_goods_{0}'.format(day)
    shop = 'shop_statistics_{0}'.format(day)
    detail = 'd_{0}'.format(day)
    monitor = 'm_{0}'.format(day)

    # todo 保存目录为可选项
    # todo 保存目录为 linux windows 兼容

    pool = Pool()
    pool.apply_async(func=dump_mongodb, args=(detail,))
    pool.apply_async(func=dump_mongodb, args=(monitor,))
    pool.apply_async(func=dump_mysql, args=(goods,))
    pool.apply_async(func=dump_mysql, args=(new,))
    pool.apply_async(func=dump_mysql, args=(hot,))
    pool.apply_async(func=dump_mysql, args=(shop,))
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
