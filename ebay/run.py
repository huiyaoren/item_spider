# -*- coding: utf-8 -*-

def run():
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())

    process.crawl('listing_spider')
    process.start()


def test():
    from ebay.utils import ebay as e
    from ebay.utils import common as c
    from ebay.utils import data as d
    from ebay.tests import test as t

    return c.clean_item_id()


def init():
    from ebay.utils.data import insert_category_ids
    insert_category_ids('redis')


if __name__ == '__main__':
    # todo 每天第一次执行时在 MongoDB 生成 category_ids 数据
    # run()
    init()
