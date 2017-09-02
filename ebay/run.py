# -*- coding: utf-8 -*-

def run():
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())

    process.crawl('listing_spider')
    process.start()


def test():
    from ebay.utils import common
    common.insert_category_ids()


if __name__ == '__main__':
    # run()
    test()
