import os, time
from datetime import datetime

import sys

'''
定时清理过期的备份文件 [mysql / mongodb]
'''


class Dustman():
    def __init__(self, date=None, dir_='', day_ago=None, hour_ago=None, types=None, test=False):
        self.date = date or datetime.now().strftime('%Y%m%d')
        self.dir = dir_
        self.ago = hour_ago or day_ago * 24
        self.types = types.split(',')
        self.test = test
        self.deleted_list = []

    def log_info(self):
        print('==== Dustman info ====')
        if self.test: print('test_mode: TRUE')
        print('date: {0}'.format(self.date))
        print('dir: {0}'.format(self.dir))
        print('hour_ago: {0}'.format(self.ago))
        print('types: {0}'.format(','.join(self.types)))
        print('======================')

    def log_deleted(self):
        print('==== Deleted list ====')
        for item in self.deleted_list:
            print(item)
        print('======================')

    def dusting(self):
        print('preparing...')
        self.log_info()
        print('starting...')
        items = os.listdir(self.dir)
        for item in items:
            file_name = self.dir + item
            state = os.stat(file_name)
            now = time.time()
            ago = (now - state.st_mtime) / 3600
            if ago > self.ago and item.split('.')[-1] in self.types:  # type
                try:
                    print('deleting file: {0}...'.format(item))
                    if not self.test:
                        os.remove(file_name)
                    self.deleted_list.append(item)
                    print('deleted.')
                except IsADirectoryError:
                    print('pass... {0} is a Directory.'.format(item))
        print('done.')
        self.log_deleted()


def main():
    argv = dict(enumerate(sys.argv))
    dustman = Dustman(
        dir_=argv.get(1, '/host/DL/'),
        day_ago=int(argv.get(2, 9999)),
        types=argv.get(3, 'sql,bson,json'),
        test=False,
    )
    dustman.dusting()


if __name__ == '__main__':
    main()
