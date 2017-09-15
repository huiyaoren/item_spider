from .ebay.statics import *
from multiprocessing import Pool
from datetime import datetime


def run(date=None):
    d = datetime.now()
    count_sales_yesterday(date)
    count_sales_last_week(date)
    copy_sales_two_weeks_ago(date)
    judge_is_new(date)
    judge_is_hot(date)
    print(datetime.now() - d)


def run_multi(date=None):
    d = datetime.now()
    p = Pool()
    p.apply_async(count_sales_yesterday, args=(date,))
    p.apply_async(count_sales_last_week, args=(date,))
    p.apply_async(copy_sales_two_weeks_ago, args=(date,))
    p.apply_async(judge_is_new, args=(date,))
    p.apply_async(judge_is_hot, args=(date,))
    p.close()
    p.join()
    print(datetime.now() - d)


if __name__ == '__main__':
    run_multi('20170912')
