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

        'ebay:category_ids',
        'ebay:category_urls',
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
            31387, 177760, 64035, 56172, 179273, 146290, 180962, 35190, 112529, 166725, 61779, 1082, 11484, 2993, 57989,
            50602, 146545, 11522, 11530, 3199, 116022, 181909, 20706, 176973, 33161, 20659, 163583, 45220, 163560,
            26420, 14295, 20163, 139973, 1524, 13866, 155101, 37822, 27386, 180040, 146531, 63855, 181708, 183545,
            63852, 48618, 50637, 20485, 26388, 11667, 179811, 175636, 6755, 177741, 546, 118261, 257, 16494, 71378,
            26388, 9745, 51071, 100345, 11843, 50677, 177, 86174, 102430, 33649, 52365, 45230, 170103, 50431, 33657,
            165560, 56092, 36449, 11837, 3820, 62134, 20593, 112581, 46782, 150059, 79759, 954, 36589, 38229, 162, 7279,
            113337, 428, 20509, 28162, 45515, 15662, 14014, 58543, 166030, 132297, 20357, 88468, 20373, 146504, 80077,
            43307, 96991, 48571, 68030, 48677, 42425, 182094, 31492, 67858, 51169, 58300, 31493, 182095, 182096, 158840,
            20311, 116848, 182097, 3668, 42428, 182073, 182098, 1500, 146492, 80087, 38331, 3286, 182064, 9394, 9355,
            40054, 4669, 4670, 149987, 296, 183502, 183503, 40979, 20381, 182069, 182067, 182065, 182066, 182068,
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
    for i in range(processes - prepared):
        p.apply_async(run, args=(name,))
    p.close()
    p.join()


if __name__ == '__main__':
    init()
    run_multi('detail_xml_redis_spider', 100, 20)
