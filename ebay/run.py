import sys

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
        'ebay:item_ids_filter_hyper',
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
        insert_category_id([
            177664, 36865, 28162, 20485, 102411, 80913, 9745, 40979, 175636, 123417, 52762, 175643, 20509, 102430,
            123422, 546, 64035, 48677, 20518, 102953, 13866, 150059, 4660, 1082, 4669, 4670, 165437, 11843, 146504,
            179273, 177741, 122962, 177754, 177760, 36449, 6755, 146531, 179811, 16494, 7279, 116848, 20593, 20594,
            146545, 40054, 170103, 158840, 20605, 33919, 3199, 181887, 57990, 9355, 52365, 166030, 42132, 181909,
            177816, 86174, 162, 80546, 45220, 82597, 181415, 58540, 45230, 20654, 57520, 58543, 9394, 20659, 62134,
            36024, 113337, 3768, 165560, 74941, 46782, 86207, 14014, 20163, 139973, 132297, 181962, 80077, 178893,
            183502, 183503, 20690, 71378, 3286, 80087, 172024, 94940, 11484, 96991, 46305, 180962, 50914, 163560, 3820,
            36589, 183545, 27386, 50431, 163583, 179457, 11522, 31492, 31493, 11530, 67858, 26388, 31510, 56092, 43304,
            296, 43307, 15662, 182064, 182065, 182066, 182067, 26420, 182069, 58166, 116022, 182068, 182073, 166725,
            180040, 176973, 182094, 182095, 182096, 182097, 182098, 61779, 51027, 183125, 38229, 20311, 15709, 3422,
            107876, 58730, 56172, 63855, 33649, 146290, 35190, 33657, 63866, 181114, 20349, 183169, 44932, 20357,
            33161, 33164, 79759, 112529, 11667, 88468, 20373, 182173, 20381, 182178, 15274, 37802, 428, 50602, 33721,
            954, 42425, 58300, 48571, 68030, 37822, 42428, 182213, 112581, 44999, 45002, 45515, 181708, 50637, 50647,
            14295, 1500, 155101, 51169, 149987, 48618, 43504, 43506, 177652, 1524, 118261, 50677, 116724, 100345,
        ], 3000)
    reset_token()
    # insert_category_ids('redis')
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


def main():
    args = dict(enumerate(sys.argv))
    print(args)

    type = args.get(1, 'master')
    processes = int(args.get(2, 128))
    prepared = 0

    if type == 'master':
        init()
        prepared = int(args.get(3, 16))
    if type == 'slave':
        prepared = int(args.get(3, 0))

    print(type, processes, prepared)


    run_multi('detail_xml_redis_spider', processes, prepared)


if __name__ == '__main__':
    main()
