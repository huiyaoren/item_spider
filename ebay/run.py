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
    from ebay.utils.data import insert_category_ids, delete_item_ids_filter, delete_item_ids
    delete_item_ids_filter()
    delete_item_ids()
    insert_category_ids('redis')
    # todo 重启 mongod
    print('Init Done.')


def run_multi():
    from multiprocessing import Pool
    p = Pool(16)
    p.apply_async(run, args=('listing_redis_spider'))
    for i in range(16):
        p.apply_async(run, args=('detail_xml_redis_spider'))
    p.close()
    p.join()


if __name__ == '__main__':
    # todo 每天第一次执行时在 MongoDB 生成 category_ids 数据
    # run()
    test()
