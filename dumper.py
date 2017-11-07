import os
from datetime import datetime
from multiprocessing.pool import Pool

from ebay.ebay.tests.time_recoder import log_time
from ebay.ebay.utils.data import db_mongodb, db_mysql


class Dumper():
    def __init__(self, date=None):
        self.date = date or datetime.now().strftime("%Y%m%d")

    def chunks(self, list, length):
        for i in range(0, len(list), length):
            yield list[i:i + length]


class OldMysqlDumper(Dumper):
    ''' 已弃用 '''
    def __init__(self, table=None, start=0, range=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = table
        self.mysql_from = db_mysql('mysql_local')
        self.mysql_to = db_mysql('mysql')
        if table:
            self.create_table(table)
        if table == 'goods':
            self.table = '_'.join([table, self.date])

    def create_table(self, table=None, date=None, mysql=None):
        with open('ebay/ebay/sqls/{0}.sql'.format(table or self.table)) as f:
            sql = f.read().format(date or self.date)
            print(sql)
        mysql = mysql or self.mysql_to
        self.execute(sql, mysql)

    def execute(self, sql, mysql, cursor=None, data=None):
        # cursor = cursor or mysql.cursor()
        cursor = mysql.cursor()
        try:
            cursor.execute(sql, data)
            results = cursor.fetchall()
            mysql.commit()
        except Exception as e:
            print("Fail")
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()

    def insert_sql(self, insert_data, field_list):
        fields = ','.join(field_list)
        sql = 'INSERT INTO {table_} ({fields_}) VALUES '.format(table_=self.table, fields_=fields)

        def data_sql():
            for line in insert_data:
                yield '({0})'.format(
                    ','.join([r"'{0}'".format(str(i).replace(r"'", r"\'").replace(r'"', r'\"')) for i in line]))

        data_sql = ','.join(i for i in data_sql())
        sql = ' '.join([sql, data_sql])
        return sql

    def data_source(self, field_list, lines, mysql):
        fields = ','.join(field_list)
        for l in range(0, lines, 1000):
            print(l)
            sql = "SELECT {fields} FROM {table} limit {start}, {end} ".format(
                start=l, end=l + 1000, fields=fields, table=self.table)
            result = self.execute(sql, mysql)
            yield result

    @log_time
    def dump(self, field_list):
        # 获取源数据库数据总行数
        lines = self.total_rows()
        # 多线程循环每次读取 1000 行数据
        for data in self.data_source(field_list, lines, self.mysql_from):
            # 构造 SQL 语句写入目标数据库
            insert_sql = self.insert_sql(data, field_list)
            self.execute(insert_sql, self.mysql_to)
            del insert_sql

    def total_rows(self):
        sql = "SELECT count(*) AS rowcount FROM {table_}".format(table_=self.table)
        result = self.execute(sql, self.mysql_from)
        lines = result[0][0]
        return lines

    def __del__(self):
        self.mysql_to.close()
        self.mysql_from.close()


class MysqlDumper(Dumper):
    def __init__(self, table=None, config_source=None, config_target=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_source = config_source or {'host': '192.168.1.248',
                                               'database': 'erp_spider',
                                               'username': 'root',
                                               'password': 'root',
                                               'port': 3306, }
        self.config_target = config_target or {'host': '45.126.121.187',
                                               'database': 'erp_spider',
                                               'username': 'erp_spider',
                                               'password': 'fyEnzfwZjT',
                                               'port': 3306, }
        self.table = table

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

    def run(self, table=None):
        self.dump(table)
        self.import_(table)


class MongodbDumper(Dumper):
    mongodb = db_mongodb('mongodb_remote')


def main():
    dumper = MysqlDumper(table='goods_{0}'.format(datetime.now().strftime("%Y%m%d")))
    dumper.import_()


if __name__ == '__main__':
    main()
