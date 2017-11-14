import os
from datetime import datetime

from ebay.ebay.tests.time_recoder import log_time_with_name


class Dumper():
    def __init__(self, date=None):
        self.date = date or datetime.now().strftime("%Y%m%d")

    def chunks(self, list, length):
        for i in range(0, len(list), length):
            yield list[i:i + length]


class MysqlDumper(Dumper):
    def __init__(self, table=None, source=None, target=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_source = source or {'host': '192.168.1.248',
                                        'database': 'erp_spider',
                                        'username': 'root',
                                        'password': 'root',
                                        'port': 3306, }
        self.config_target = target or {'host': '45.126.121.187',
                                        'database': 'erp_spider',
                                        'username': 'erp_spider',
                                        'password': 'fyEnzfwZjT',
                                        'port': 3306, }
        self.table = table

    @log_time_with_name('dump')
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

    @log_time_with_name('import')
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

    @log_time_with_name('run')
    def run(self, table=None):
        self.dump(table)
        self.import_(table)


class MongodbDumper(Dumper):

    def __init__(self, source=None, target=None, collection=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_source = source or {'host': '192.168.1.192',
                                        'database': 'test_database',
                                        'port': 27017, }
        self.config_target = target or {'host': '192.168.1.140',
                                        'database': 'test_database',
                                        'port': 27017, }
        self.collection = collection

    @log_time_with_name('dump')
    def dump(self, collection=None):
        config = self.config_source
        command_dump = 'mongodump -h {host} -d {database} -c {collection} -o dump'.format(
            host=config['host'],
            database=config['database'],
            collection=collection or self.collection
        )
        print(command_dump)
        os.system(command_dump)

    @log_time_with_name('import')
    def import_(self, collection=None):
        config = self.config_target
        command_dump = r'mongorestore -h {host} -d {database} -c {collection}  --dir dump\{database}\{collection}.bson'.format(
            host=config['host'],
            database=config['database'],
            collection=collection or self.collection
        )
        print(command_dump)
        os.system(command_dump)

    @log_time_with_name('run')
    def run(self, collection=None):
        self.dump(collection)
        self.import_(collection)


def main():
    goods = 'goods_{0}'.format(datetime.now().strftime("%Y%m%d"))
    new = 'new_goods_{0}'.format(datetime.now().strftime("%Y%m%d"))
    hot = 'hot_goods_{0}'.format(datetime.now().strftime("%Y%m%d"))
    dumper = MysqlDumper(
        target={'host': '192.168.1.248', 'database': 'erp_spider', 'username': 'root', 'password': 'root',
                'port': 3306, },
        source={'host': '45.126.121.187', 'database': 'erp_spider', 'username': 'erp_spider', 'password': 'fyEnzfwZjT',
                'port': 3306, }
    )
    dumper.run(goods)
    dumper.run(hot)
    dumper.run(new)
    # dumper = MongodbDumper(
    #     source={'host': '192.168.1.192', 'database': 'test_database', 'port': 27017, },
    #     target={'host': '192.168.1.253', 'database': 'test_database', 'port': 27017, },
    # )
    # dumper.dump('d_{0}'.format(datetime.now().strftime("%Y%m%d")))


if __name__ == '__main__':
    main()
