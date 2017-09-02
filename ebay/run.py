# -*- coding: utf-8 -*-

def run():
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())

    process.crawl('listing_spider')
    process.start()


def get_category_ids():
    from ebay.utils.common import db_mysql
    mysql = db_mysql()
    cursor = mysql.cursor()
    sql = 'select platform_category_id from erp_saas_goods_category where site = 201'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print(row[0])
            data = {'category_id': row[0]}
            yield data
    except:
        print("Error: unable to fetch data")
    else:
        mysql.close()
    return


def insert_category_ids():
    import logging
    from pymongo.errors import DuplicateKeyError
    from ebay.utils.common import db_mongodb
    mongodb = db_mongodb()
    c = mongodb['category_ids']
    c.ensure_index('category_id', unique=True)
    for listing in get_category_ids():
        try:
            c.insert_one(listing)
        except DuplicateKeyError:
            print("Duplicate ")
            logging.info("Duplicate Item")
    print('count: ', c.count())


if __name__ == '__main__':
    # run()
    insert_category_ids()
