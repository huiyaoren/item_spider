from ebay.statics import *
from multiprocessing import Pool
from datetime import datetime
from run import run as run_spider

from ebay.utils.data import copy_item_ids_to_clean


def run(date=None):
    d = datetime.now()
    p = Pool()
    p.apply_async(count_sales_last_week, args=(date,))
    p.apply_async(copy_sales_two_weeks_ago, args=(date,))
    p.apply_async(judge_is_new, args=(date,))
    p.apply_async(judge_is_hot, args=(date,))
    p.close()
    p.join()
    print(datetime.now() - d)


def run_multi(name, processes=8):
    p = Pool()
    for i in range(processes):
        p.apply_async(run_spider, args=(name,))
    p.close()
    p.join()


def init():
    copy_item_ids_to_clean()


if __name__ == '__main__':
    init()
    run_multi('clean_spider', 16)
