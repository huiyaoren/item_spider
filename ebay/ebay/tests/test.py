# -*- coding: utf-8 -*-
import logging

from requests import Session, Request

logger = logging.getLogger(__name__)


def test_get_items():
    url = 'https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?limit=3&category_ids=179697&fieldgroups=FULL'
    headers = {
        'Authorization': 'Bearer v^1.1#i^1#r^0#p^1#f^0#I^3#t^H4sIAAAAAAAAAOVXa2wUVRTudvugwdrw8knMdjAarTN7Z2Z3uzPprtm2EIrQFrctT8U7M3faobszk7mzbFcqWWqCJYoRJSYYMUTFkAgJETHFyEP8JRI09oe8oiGBqBiCISIRa/DO7FK2lUCFEkncP5t77rnnfuc737l3LsiWVTy+Zvaai5We8uLNWZAt9njYiaCirLTmbm/xA6VFoMDBszn7cLakz/tTHYbJhCk+jbBp6Bj5epIJHYuuMUKlLF00INawqMMkwqIti/HYvLkixwDRtAzbkI0E5WtqjFBBKNdybEDh1XCYl6BCrPqVmG1GhJKRJCCgynJIQJwiATKPcQo16diGuh2hOMDW0kCgAdsGQmKAF9kAwwX5xZSvA1lYM3TiwgAq6sIV3bVWAdbrQ4UYI8smQahoU2xWvCXW1Dizua3OXxArmuchbkM7hUeOGgwF+TpgIoWuvw12vcV4SpYRxpQ/mtthZFAxdgXMTcB3qVaQBDhFllUlzKmwVhkXKmcZVhLa18fhWDSFVl1XEem2ZmduxChhQ1qOZDs/aiYhmhp9zt/8FExoqoasCDWzPrYo1tpKRbugntD057to4mwmEDTpeP1CmlUkmRUUFKRZNRTiFE7Ib5SLlqd51E4Nhq5oDmnY12zY9YigRqO54Qu4IU4teosVU20HUaFf+AqHAbDYKWquiim7S3fqipKECJ87vHEFhlfbtqVJKRsNRxg94VIUoaBpago1etLVYl4+PThCddm2Kfr96XSaSfOMYXX6OQBY/8J5c+NyF0pCivg6vZ7z1268gNbcVGREVmJNtDMmwdJDtEoA6J1UlKsN8Wwwz/tIWNHR1n8YCnL2j+yI8eoQNsijkMBKPBcIkgNnXDokmhep38GBJJihk9DqRraZgDKiZaKzVBJZmiLyQZXjwyqilZCg0gFBVWkpqISIdhECCEmSLIT/T40yVqnHZcNErUZCkzPjIvhxEztvKa3QsjP1qQwZx1GCMN85Vu1fM1XspHobk3R6/SYSdWJgEgSaGuMonJGNpN+A5GhzTMtc1L6xOPmlVIbpTCFsExQKuV3GvEgjEmFIoyhjX5Jrw1stiUYu7DtKdSTdXN6akrtpGTd5Bq+QGQthI2WRjwymxbl42oxupJM2ti0jkUBWB3tLTIzflfMfXTfXzEpOaITGZXdaZv/yHL9G7iV9nqGx6Bvad1bmbBAEuECYFQK3VNcGt65tmdt6nt5EerMNbCPlNnwh+Ue+16JF7o/t8+wBfZ7d5MkHagHN1oDHyrztJd67KEyOVAZDXZGMHkaDKoO1Tp08RyzEdKOMCTWruMyz5MEzTw4VvBQ3PwPuG34rVnjZiQUPRzD96kwpW3VvJVsLBMCCUIBnA4vBjKuzJew9JVPTG3+ZUH+5d/UfdVtnnqzbFcvO3RoClcNOHk9pEZFw0ab9+/qrm+fdv7fkiHfJAFN16eUPqfeWHPOGJnW/+uiBnVNPnPh8OhxMV3zx7rEX3prcvsf6dlU1Prvz3IqBhy52n6n2zdmwbu0Mofi8mt5rDob1+YNHDnZvquo7f7yqbv2kczWPdGz4jf/1o2nbxC2h/mWeExRYd7l6wZaXPp5A+Y72Ltr+9ezf39w+WPP2rqHs0SnHv1pafmnOobPPvjh51RtHfyz/M9jf9eWW16d9uvbC0GGq9ZND6z39F5YHDiyto5q+AWF9e3/ZK9+thM+V7t7xzo6G8v0ro8JTQvWUip89B1+bKFanhVNZfuOC9ZWHT+37q/f709sOtZeefH+o1/hs9eQfjjV+cPryE9ZArox/A1pyfU7DDwAA',
        'Content-Type': 'application/json',
        'X-EBAY-C-ENDUSERCTX': 'affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>'
    }
    method = 'GET'
    s = Session()
    req = Request(headers=headers, url=url, method=method)
    prepped = req.prepare()
    resp = s.send(prepped)
    return resp.content


def test_ebay_api():
    from ebaysdk.exception import ConnectionError
    from ebaysdk.trading import Connection as Trading

    try:
        api = Trading(config_file='ebay.yaml', debug=True)
        print(api.config.get('token'), 123)

        api.execute('GetTokenStatus', {'CharityID': 3897})
        # dump(api)
        print(api.response.reply)
        return api.response.reply

    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        return e.response.dict()


def test_mongodb():
    from pymongo import MongoClient

    # 连接 MongoClient
    Client = MongoClient()

    # 获取数据库
    db = Client['test_database']
    db = Client.test_database

    # 获取 collection
    collection = db['test_collection']
    collection = db.test_collection

    # 储存数据
    import datetime
    post = {
        'type': 'BSON',
        'data': datetime.datetime.utcnow(),
    }

    document_1 = {'x': 1}
    document_2 = {'x': 2}
    posts = db.posts
    post_1 = posts.insert_one(document_1).inserted_id
    post_2 = posts.insert_one(document_2).inserted_id
    print(post_1, post_2)

    # 插入多个文档
    new_document = [
        {'x': 1},
        {'x': 2},
    ]
    result = posts.insert_many(new_document)
    print(result.inserted_ids)

    # 从 MongoDB 中调用数据
    d = posts.find_one()
    print(d)

    for data in posts.find():
        print(data)

    for post in posts.find({'x': 1}):
        print(post)

    # 更新数据
    posts.update_one({'x': 1}, {'$set': {'x': 10}})

    # 删除数据
    posts.delete_one({'x': 10})

    # 计数
    c = posts.count()
    print(c)


def test_mysql():
    import pymysql
    db = pymysql.connect('192.168.1.248', 'root', 'root', 'erp')
    cursor = db.cursor()
    sql = 'select * from erp_saas_goods_category where platform_category_id = 179697;'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except:
        print("Error: unable to fetch data")
    db.close()
    return


def sample_item_data():
    item = {
        'refinement': {
            'buyingOptionDistributions': [
                {
                    'buyingOption': 'AUCTION', 'matchCount': 0,
                    'refinementHref': 'https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?limit=3&category_ids=179697&fieldgroups=FULL&filter=buyingOptions%3A%7BAUCTION%7D'
                },
                {
                    'buyingOption': 'FIXED_PRICE', 'matchCount': 10,
                    'refinementHref': 'https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?limit=3&category_ids=179697&fieldgroups=FULL&filter=buyingOptions%3A%7BFIXED_PRICE%7D'
                }
            ],
            'conditionDistributions': [
                {
                    'condition': 'NEW', 'matchCount': 0,
                    'refinementHref': 'https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?limit=3&category_ids=179697&fieldgroups=FULL&filter=conditions%3A%7BNEW%7D'
                }
            ],
            'categoryDistributions': [
                {
                    'categoryName': 'Camera Drones',
                    'categoryId': '179697',
                    'refinementHref': 'https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?limit=3&fieldgroups=FULL&category_ids=179697'
                }
            ]
        },
        'next': 'https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?limit=3&category_ids=179697&fieldgroups=FULL&offset=3',
        'total': 10,
        'href': 'https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?limit=3&category_ids=179697&fieldgroups=FULL&offset=0',
        'offset': 0,
        'itemSummaries': [
            {
                'price': {'value': '399.95', 'currency': 'USD'},
                'categories': [{'categoryId': '179697'}, {'categoryId': '625'}],
                'itemLocation': {'country': 'US'},
                'shippingOptions': [
                    {
                        'shippingCostType': 'FIXED',
                        'shippingCost': {'value': '0.00', 'currency': 'USD'}
                    }
                ],
                'seller': {'feedbackPercentage': '0.0', 'feedbackScore': 1},
                'title': '3DR - Solo Gimbal - Black',
                'conditionId': '1000',
                'image': {'imageUrl': 'https://i.ebayimg.com/thumbs/images/m/mQJ8jAD-dLXC0_NAGG312eQ/s-l225.jpg'},
                'currentBidPrice': {'value': '399.95', 'currency': 'USD'},
                'buyingOptions': ['FIXED_PRICE'],
                'condition': 'New',
                'itemId': 'v1|110221819687|0',
                'itemAffiliateWebUrl': 'http://rover.ebay.com/rover/1/711-53200-19255-0/1?campid=%3CePNCampaignId%3E&customid=%3CreferenceId%3E&toolid=10049&mpre=http%3A%2F%2Fwww.sandbox.ebay.com%2Fitm%2F3DR-Solo-Gimbal-Black-%2F110221819687%3Fhash%3Ditem19a9bb7f27%3Am%3AmQJ8jAD-dLXC0_NAGG312eQ',
                'itemWebUrl': 'http://www.sandbox.ebay.com/itm/3DR-Solo-Gimbal-Black-/110221819687?hash=item19a9bb7f27:m:mQJ8jAD-dLXC0_NAGG312eQ',
                'itemHref': 'https://api.sandbox.ebay.com/buy/browse/v1/item/v1|110221819687|0',
                'additionalImages': [
                    {'imageUrl': 'https://galleryplus.ebayimg.com/ws/web/110221819687_2_0_1/225x225.jpg'},
                    {'imageUrl': 'https://galleryplus.ebayimg.com/ws/web/110221819687_3_0_1/225x225.jpg'}
                ]
            },
            {
                'price': {'value': '511.99', 'currency': 'USD'},
                'itemLocation': {'country': 'US'},
                'shippingOptions': [
                    {'shippingCostType': 'FIXED', 'shippingCost': {'value': '0.00', 'currency': 'USD'}}],
                'categories': [
                    {'categoryId': '179697'},
                    {'categoryId': '625'}
                ],
                'title': 'EHANG - Ghostdrone 2.0 VR Drone - Black/Orange',
                'conditionId': '1000', 'itemId': 'v1|110221879275|0',
                'currentBidPrice': {'value': '511.99', 'currency': 'USD'},
                'marketingPrice': {
                    'discountPercentage': '43',
                    'discountAmount': {'value': '388.00', 'currency': 'USD'},
                    'originalPrice': {'value': '899.99', 'currency': 'USD'}},
                'buyingOptions': ['FIXED_PRICE'], 'condition': 'New',
                'seller': {'feedbackPercentage': '0.0', 'feedbackScore': 1},
                'itemAffiliateWebUrl': 'http://rover.ebay.com/rover/1/711-53200-19255-0/1?campid=%3CePNCampaignId%3E&customid=%3CreferenceId%3E&toolid=10049&mpre=http%3A%2F%2Fwww.sandbox.ebay.com%2Fitm%2FEHANG-Ghostdrone-2-0-VR-Drone-Black-Orange-%2F110221879275%3Fhash%3Ditem19a9bc67eb%3Ai%3A110221879275',
                'itemWebUrl': 'http://www.sandbox.ebay.com/itm/EHANG-Ghostdrone-2-0-VR-Drone-Black-Orange-/110221879275?hash=item19a9bc67eb:i:110221879275',
                'itemHref': 'https://api.sandbox.ebay.com/buy/browse/v1/item/v1|110221879275|0',
                'additionalImages': [
                    {'imageUrl': 'https://galleryplus.ebayimg.com/ws/web/110221879275_2_0_1/225x225.jpg'},
                    {'imageUrl': 'https://galleryplus.ebayimg.com/ws/web/110221879275_3_0_1/225x225.jpg'}
                ]
            },
            {
                'price': {'value': '299.99', 'currency': 'USD'},
                'itemLocation': {'country': 'US'}, 'shippingOptions': [
                {'shippingCostType': 'FIXED',
                 'shippingCost': {'value': '0.00', 'currency': 'USD'}}],
                'categories': [{'categoryId': '179697'}, {'categoryId': '625'}],
                'title': '3DR - Solo Drone - Black', 'conditionId': '1000',
                'itemId': 'v1|110221879241|0',
                'currentBidPrice': {'value': '299.99', 'currency': 'USD'},
                'buyingOptions': ['FIXED_PRICE'], 'condition': 'New',
                'seller': {'feedbackPercentage': '0.0', 'feedbackScore': 1},
                'itemAffiliateWebUrl': 'http://rover.ebay.com/rover/1/711-53200-19255-0/1?campid=%3CePNCampaignId%3E&customid=%3CreferenceId%3E&toolid=10049&mpre=http%3A%2F%2Fwww.sandbox.ebay.com%2Fitm%2F3DR-Solo-Drone-Black-%2F110221879241%3Fhash%3Ditem19a9bc67c9%3Ai%3A110221879241',
                'itemWebUrl': 'http://www.sandbox.ebay.com/itm/3DR-Solo-Drone-Black-/110221879241?hash=item19a9bc67c9:i:110221879241',
                'itemHref': 'https://api.sandbox.ebay.com/buy/browse/v1/item/v1|110221879241|0',
                'additionalImages': [{
                    'imageUrl': 'https://galleryplus.ebayimg.com/ws/web/110221879241_2_0_1/225x225.jpg'},
                    {
                        'imageUrl': 'https://galleryplus.ebayimg.com/ws/web/110221879241_3_0_1/225x225.jpg'},
                    {
                        'imageUrl': 'https://galleryplus.ebayimg.com/ws/web/110221879241_4_0_1/225x225.jpg'},
                    {
                        'imageUrl': 'https://galleryplus.ebayimg.com/ws/web/110221879241_5_0_1/225x225.jpg'},
                    {
                        'imageUrl': 'https://galleryplus.ebayimg.com/ws/web/110221879241_6_0_1/225x225.jpg'}]}
        ],
        'limit': 3
    }


def test_pprint():
    from pprint import pprint
    l = {'x': 1, 'y': 2, }
    pprint(l)
    pprint(locals())
    pprint(globals())
    print(vars(l))


if __name__ == '__main__':
    test_mysql()
