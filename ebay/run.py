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
    delete_redis_key([
        'ebay:item_ids_filter',
        'ebay:item_ids',

        'ebay:shop:basic',
        'ebay:shop:count',
        'ebay:shop:has_sold_count',
        'ebay:shop:total_sold',
        'ebay:shop:amount',
        'ebay:shop:week_sold',
        'ebay:shop:last_week_sold',
    ])
    if is_testing:
        # 测试
        # read_item_ids_from_file()
        # copy_item_ids()
        insert_category_id([
            179457, 37802, 15274, 172024, 45002, 165437, 122962, 20690, 44999, 46305, 181415, 33721, 58730, 181962,
            181114, 183125, 182173, 182178, 3768, 102953, 3422, 20654, 177816, 20605, 11873, 33164, 50914, 58540, 43504,
            43304, 20349, 36865, 107876, 74941, 123422, 33919, 57990, 15687, 43506, 20594, 175643, 177652, 183169,
            181887, 58166, 177754, 51027, 42132, 94940, 82597, 36024, 177664, 31510, 116724, 11511, 20518, 4660, 57520,
            44932, 15709, 80546, 86207, 52762, 80913, 102411, 78089, 50647, 178893, 123417, 182213, 14990, 2996, 1060,
            31387, 177760, 64035, 56172,
        ])
    else:
        # 生产
        insert_category_ids('redis')
    reset_token()
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
    run_multi('detail_xml_redis_spider', 100, 20)
