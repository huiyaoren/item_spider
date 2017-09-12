# -*- coding: utf-8 -*-

def run(name='listing_redis_spider'):
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())

    process.crawl(name)
    process.start()


def test():
    from ebay.utils import ebay as e
    from ebay.utils import common as c
    from ebay.utils import data as d
    from ebay.tests import test as t

    return t.test_insert_category_ids_to_redis()


def init():
    from ebay.utils.data import insert_category_ids, delete_item_ids_filter, delete_item_ids, copy_item_ids, reset_token
    is_testing = True
    if is_testing:
        # 测试
        delete_item_ids()
        copy_item_ids()
    else:
        # 生产
        delete_item_ids_filter()
        delete_item_ids()
    insert_category_ids('redis')
    reset_token()
    # todo 重启 mongod
    print('Init Done.')


def run_multi(name, processes=8):
    from multiprocessing import Pool
    p = Pool()
    for i in range(processes):
        p.apply_async(run, args=(name,))
    p.close()
    p.join()


if __name__ == '__main__':
    run_multi('listing_redis_spider', 1)
