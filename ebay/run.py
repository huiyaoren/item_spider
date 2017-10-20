try:
    from ebay.utils.data import *
except ImportError:
    from .ebay.utils.data import *


def run(name='listing_redis_spider'):
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())

    process.crawl(name)
    process.start()


def init():
    is_testing = True
    delete_item_ids_filter()
    delete_item_ids()
    if is_testing:
        # 测试
        # delete_item_ids()
        # read_item_ids_from_file()
        # copy_item_ids()
        insert_category_id([
            179457, 37802, 15274, 172024, 45002, 165437, 122962, 20690, 44999, 46305, 181415, 33721, 58730, 181962,
            # 181114, 183125, 182173, 182178, 3768,
        ])
    else:
        # 生产
        insert_category_ids('redis')
    reset_token()
    # todo 重启 mongod
    # todo mongodb create collection
    # todo mongodb create unique key
    print('Init Done.')


def run_multi(name, processes=8, prepared=0):
    from multiprocessing import Pool
    p = Pool(processes)
    if prepared:
        for i in range(prepared):
            p.apply_async(run, args=('listing_xml_redis_spider',))
            # p.apply_async(run, args=('listing_redis_spider',))
    for i in range(processes - prepared):
        p.apply_async(run, args=(name,))
    p.close()
    p.join()


if __name__ == '__main__':
    init()
    run_multi('detail_xml_redis_spider', 32, 8)
