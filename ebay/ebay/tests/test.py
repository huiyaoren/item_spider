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


def test_get_detail_json():
    url = 'https://api.ebay.com/buy/browse/v1/item/v1|132310376016|0'
    headers = {
        'Authorization': 'Bearer v^1.1#i^1#r^0#f^0#I^3#p^1#t^H4sIAAAAAAAAAOVXe2wURRzu9doijwoxCIqkHgsSq+zu7N3e7d2GO3NtqRRLH1xBhZAyuzvb27K3u9nZoz2QpjRCEEkMqEj8qyQkBtQENQgkBiVGQRKJjzSRqlEIJsTwEI0IPqKz2wfXSngWIfH+uezMb37zfd/v+83ugM6S0Y+sm7vut1LfqMLuTtBZ6PNxY8HokuJH7/YXTikuAHkBvu7OGZ1FXf6TszHM6Ja4AGHLNDAKtGd0A4veYJzK2oZoQqxh0YAZhEVHFlPJ+bVikAGiZZuOKZs6FaipilMxLsJxEifInBSVIYRk1BjI2WTGKRhRIjKSIqogCEoY8GQe4yyqMbADDSdOBQEn0CBGA6EJxESOF3nA8EF+MRVYhGysmQYJYQCV8OCK3lo7D+uVoUKMke2QJFSiJlmdqk/WVM2pa5rN5uVK9OuQcqCTxUOfKk0FBRZBPYuuvA32osVUVpYRxhSb6NthaFIxOQDmBuB7UvMC4tUIVKAahWE+BEdEymrTzkDnyjjcEU2hVS9URIajObmrKUrUkFqR7PQ/1ZEUNVUB968xC3VN1ZAdp+ZUJJ9ONjRQiTQ0dM1YmaZJsKUjaNENC6roMIgBIRRFEh1Tg0EYRLH+jfqy9cs8bKdK01A0VzQcqDOdCkRQo+HagDxtSFC9UW8nVcdFlBfHcQMaciSOHahi1kkbbl1RhggR8B6vXoHB1Y5ja1LWQYMZhk94EpG2sSxNoYZPel7st087jlNpx7FElm1ra2PaQoxpt7BBADj2qfm1KTmNMsQh7Rm31/vitasvoDWPiozISqyJTs4iWNqJVwkAo4VKBPlIODxQhaGwEsNH/zWQx5kd2hEj1SEIRKOhGJAUiORoFEVHokMS/SZlXRxIgjk6A+3lyLF0KCNaJj7LZpCtKWIorAZDURXRSiSm0nxMVWkprERoTkUIICRJciz6f2qUa7V6SjYt1GDqmpwbEcOPmNlDttIAbSeXQjrRvOVaXX9Zktglecvpub1+XRTdHJgkgZbGuN5mZDPDmpAcau5Qs4f6pnhr5H14RxWVEOxjqil9LzLGo8vgFTJjI2xmbfIOZ+rdc73JXI4M0iWObeo6shdxN6XEyJ3ot+k0vywrWdeIjM13GrPrPCZv0NvQuY2si7p8Sy7DnCPf2IIQjkTBTXGr9OralPsPDq3rKuxcEztIuQUfIOzQ61CiwPtxXb7doMv3FrlRARY8xE0H00r8C4v846ZgzUGMBlUGay0G+cq3EbMc5Syo2YUlviVTd+1ozruAdS8F9w1ewUb7ubF59zEw9dJMMTd+ciknuDYFMY7nwWIw/dJsETepaOLOE2OCFy9UbF29acbpxwIr1V/PZA+A0sEgn6+4gDijoPednve2bF7D/ND90tLa7B9r7zXjva+ssmI0XH2YaTx0tOP4rBOrNjJHjm7tWS+0BszSB16nn/vg0/Mf/Z45V/7CVxs+3/tM2dnJH5+qrW7+fswE3n943uKw+lPloQvUrE/ejZ7b9K3wsPRzS+Emqe6Jxr3zyrdfKBy3/eTaLdK2PTvYY/PGn9mvHrPuT68Ir2/dt3uZb8/4na/1vl/VMXPmKOfVezYsO1hGH7y4Z3PFqV2Z+NSOfQ82/v32xPLzfGkycf7DVvj4m192Hw9ts9Idfy2sLiv77q7yN/av2Xj0rP7k6d5J+oTeZ3887O/485evp6lt7GcvogPfWC/3LKTXg2Vji7gj6Z65XzyfntVXvn8AW68uWBoPAAA=',
        'Content-Type': 'application/json',
        'X-EBAY-C-ENDUSERCTX': 'contextualLocation=country=<2_character_country_code>,zip=<zip_code>,affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>'
    }
    method = 'GET'
    s = Session()
    req = Request(headers=headers, url=url, method=method)
    prepped = req.prepare()
    resp = s.send(prepped)
    return resp.content


def test_get_detail_xml():
    url = 'https://api.ebay.com/ws/api.dll'
    data = '''
    <?xml version="1.0" encoding="utf-8"?>
        <GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
          <RequesterCredentials>
            <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**TFk/WQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6ACkoWoD5CHoQydj6x9nY+seQ**kMADAA**AAMAAA**7VtL67+uDGoPGwpzzegnSCLgL9ZwsNRQHBaZ8T6zTQuqDg8NXWGU37zosAe7c/KcRGEzb60QX3nV1ujxFDsMwI9Kw4CAPTqVOBXz72l6mhT9m2oiVX0dCAsYd0GKMTgIrO1+uhizmiIXej3Uh7NIF8L/76k/tiS/E304JsrTmKrk2r2Rr+dST1ONfj8fb5TFzeDen0hmBzgRctchyjPesIFTRd7WupOtbi6ciScQ/yYCqfH7GRGQADCIaiMnIpdQUfnwigoNoi4OyP/mH7tr03WfCDlHTAi1Ret2LsfXh0UAYi8rwuMtVSAvP52fRtwe4lom3DzBt2jB7U7rj8KZ89ea30SAIXVsag/vo3B0jkl64pSB5/zKbBPRrG5qZ+28aDKuUSuAfn9lPNCF//esp4QIF7HIPUeioLgQK5WoPT9/BCPmn0Y+tNMAPSEcUWTY42WwahoN1eYpBgqX/hZolTvupd5907NkDTxYHfij6WtcGQdHfHBWCPGHrgWcdLefochtz7pDpVzdHYCUQbv4bVzHQNbVfhNHCMp4LZ63qrkJVpWsmSeSgZi5dVECI7gp0t/Rq1y5uBsRJK6OViZS02jYw0MR7kjAyrIsK43bP4Pz8wwvpfyuaoxkgvziCaM35taQuB3qlUPeawULUSFX6olCC0kMZqdUT5HPqYD2+YTj2n0wBXvP7Lbkj3gejSbelCwS6XHdKqAXP2gY93eBtbogLic7//FGdnQvbbISceo/9hgdXKbNBcMh0zoQ0KRm</eBayAuthToken>
          </RequesterCredentials>
            <ErrorLanguage>en_US</ErrorLanguage>
            <WarningLevel>High</WarningLevel>
              <!--Enter an ItemID-->
          <ItemID>112548339313</ItemID>
        </GetItemRequest>
    '''
    headers = {
        'X-EBAY-API-SITEID': '0',
        'X-EBAY-API-COMPATIBILITY-LEVEL': '967',
        'X-EBAY-API-CALL-NAME': 'GetItem',
    }
    method = 'POST'
    s = Session()
    req = Request(headers=headers, url=url, method=method, data=data)
    prepped = req.prepare()
    resp = s.send(prepped)
    return resp.content


def test_ebay_api():
    from ebaysdk.exception import ConnectionError
    from ebaysdk.trading import Connection as Trading

    # try:
    #     api = Trading(config_file='ebay.yaml', debug=True)
    #     print(api.config.get('token'), 123)
    #
    #     api.execute('GetTokenStatus', {'CharityID': 3897})
    #     # dump(api)
    #     print(api.response.reply)
    #     return api.response.reply
    #
    # except ConnectionError as e:
    #     print(e)
    #     print(e.response.dict())
    #     return e.response.dict()

    api = Trading(config_file='ebay.yaml', debug=True)
    print(api.config.get('token'))
    api.execute('GetItem', {'ItemID': 'v1|292191373015|591122882367'})
    print(api.response.reply)


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


def sample_detail_json_data():
    detail = {
        "itemId": "v1|122677536317|0",
        "title": "YUNEEC CGO3 4K 3-Axis Gimbal Camera for Typhoon Q500 4K Quadcopter YUNCGO3US",
        "shortDescription": "Removed from Working Drone. Works Perfectly. Comes only as shown. You get nothing else.",
        "price": {
            "value": "180.00",
            "currency": "USD"
        },
        "categoryPath": "Cameras & Photo|Camera Drones",
        "condition": "Used",
        "conditionId": "3000",
        "itemLocation": {
            "city": "Los Angeles",
            "stateOrProvince": "California",
            "postalCode": "90046",
            "country": "US"
        },
        "image": {
            "imageUrl": "http://i.ebayimg.com/00/s/MTA1OVgxNjAw/z/u1IAAOSwKM9Zp084/$_57.JPG?set_id=8800005007"
        },
        "additionalImages": [
            {
                "imageUrl": "http://i.ebayimg.com/00/s/MTA1OVgxNjAw/z/nz0AAOSwDcpZp086/$_57.JPG?set_id=8800005007"
            },
            {
                "imageUrl": "http://i.ebayimg.com/00/s/MTA1OVgxNjAw/z/IUwAAOSw791Zp089/$_57.JPG?set_id=8800005007"
            },
            {
                "imageUrl": "http://i.ebayimg.com/00/s/MTA1OVgxNjAw/z/u4gAAOSwKM9Zp08~/$_57.JPG?set_id=8800005007"
            }
        ],
        "brand": "Yuneec",
        "itemEndDate": "2017-09-02T07:58:45.000Z",
        "seller": {
            "username": "hollywood.tennis",
            "feedbackPercentage": "99.3",
            "feedbackScore": 1528
        },
        "mpn": "YUNCGO3US",
        "epid": "1976960895",
        "estimatedAvailabilities": [
            {
                "deliveryOptions": [
                    "SHIP_TO_HOME"
                ],
                "estimatedAvailabilityStatus": "OUT_OF_STOCK",
                "estimatedAvailableQuantity": 0,
                "estimatedSoldQuantity": 1
            }
        ],
        "shippingOptions": [
            {
                "shippingServiceCode": "Standard Shipping",
                "type": "Standard Shipping",
                "shippingCost": {
                    "value": "0.00",
                    "currency": "USD"
                },
                "quantityUsedForEstimate": 1,
                "minEstimatedDeliveryDate": "2017-09-12T10:00:00.000Z",
                "maxEstimatedDeliveryDate": "2017-09-19T10:00:00.000Z",
                "shipToLocationUsedForEstimate": {
                    "country": "US"
                },
                "additionalShippingCostPerUnit": {
                    "value": "0.00",
                    "currency": "USD"
                },
                "shippingCostType": "FIXED"
            }
        ],
        "shipToLocations": {
            "regionIncluded": [
                {
                    "regionName": "United States",
                    "regionType": "COUNTRY"
                }
            ],
            "regionExcluded": [
                {
                    "regionName": "Alaska/Hawaii",
                    "regionType": "COUNTRY_REGION"
                },
                {
                    "regionName": "US Protectorates",
                    "regionType": "COUNTRY_REGION"
                },
                {
                    "regionName": "Africa",
                    "regionType": "WORLD_REGION"
                },
                {
                    "regionName": "Asia",
                    "regionType": "WORLD_REGION"
                },
                {
                    "regionName": "Central America and Caribbean",
                    "regionType": "WORLD_REGION"
                },
                {
                    "regionName": "Europe",
                    "regionType": "WORLD_REGION"
                },
                {
                    "regionName": "Middle East",
                    "regionType": "WORLD_REGION"
                },
                {
                    "regionName": "North America",
                    "regionType": "WORLD_REGION"
                },
                {
                    "regionName": "Oceania",
                    "regionType": "WORLD_REGION"
                },
                {
                    "regionName": "Southeast Asia",
                    "regionType": "WORLD_REGION"
                },
                {
                    "regionName": "South America",
                    "regionType": "WORLD_REGION"
                }
            ]
        },
        "returnTerms": {
            "returnsAccepted": False
        },
        "localizedAspects": [
            {
                "type": "STRING",
                "name": "Brand",
                "value": "Yuneec"
            },
            {
                "type": "STRING",
                "name": "MPN",
                "value": "YUNCGO3US"
            },
            {
                "type": "STRING",
                "name": "Camera Integration",
                "value": "Camera Included"
            },
            {
                "type": "STRING",
                "name": "Model",
                "value": "CGO3"
            },
            {
                "type": "STRING",
                "name": "Type",
                "value": "4K 3-Axis Gimbal Camera"
            }
        ],
        "primaryProductReviewRating": {
            "reviewCount": 0,
            "averageRating": "0.0",
            "ratingHistograms": [
                {
                    "rating": "5",
                    "count": 0
                },
                {
                    "rating": "4",
                    "count": 0
                },
                {
                    "rating": "3",
                    "count": 0
                },
                {
                    "rating": "2",
                    "count": 0
                },
                {
                    "rating": "1",
                    "count": 0
                }
            ]
        },
        "topRatedBuyingExperience": False,
        "buyingOptions": [
            "FIXED_PRICE"
        ],
        "itemAffiliateWebUrl": "https://rover.ebay.com/rover/1/711-53200-19255-0/1?campid=%3CePNCampaignId%3E&customid=%3CreferenceId%3E&toolid=10050&mpre=http%3A%2F%2Fwww.ebay.com%2Fitm%2FYUNEEC-CGO3-4K-3-Axis-Gimbal-Camera-for-Typhoon-Q500-4K-Quadcopter-YUNCGO3US-%2F122677536317",
        "itemWebUrl": "http://www.ebay.com/itm/YUNEEC-CGO3-4K-3-Axis-Gimbal-Camera-for-Typhoon-Q500-4K-Quadcopter-YUNCGO3US-/122677536317",
        "description": "<font rwr='1' size='4' style='font-family:Arial'>You are bidding on a <b>YUNEEC CGO3 4K 3-Axis Gimbal Camera for Typhoon Q500 4K Quadcopter YUNCGO3US<br><br>Condition:</b><br><blockquote>Removed from Working Drone. Works Perfectly. Comes only as shown. You get nothing else.<br></blockquote><b>Includes:</b><br><ul><li>YUNEEC CGO3 4K 3-Axis Gimbal Camera for Typhoon Q500 4K Quadcopter YUNCGO3US<br></li></ul></font>"
    }


def sample_detail_xml_data():
    detail = '''
    <?xml version="1.0" encoding="UTF-8"?>
<GetItemResponse 
  xmlns="urn:ebay:apis:eBLBaseComponents">
  <Timestamp>2017-09-07T03:37:56.407Z</Timestamp>
  <Ack>Success</Ack>
  <Version>1031</Version>
  <Build>E1031_CORE_API_18531762_R1</Build>
  <Item>
    <AutoPay>true</AutoPay>
    <BuyerProtection>ItemEligible</BuyerProtection>
    <BuyItNowPrice currencyID="USD">0.0</BuyItNowPrice>
    <Country>US</Country>
    <Currency>USD</Currency>
    <GiftIcon>0</GiftIcon>
    <HitCounter>NoHitCounter</HitCounter>
    <ItemID>122677536317</ItemID>
    <ListingDetails>
      <Adult>false</Adult>
      <BindingAuction>false</BindingAuction>
      <CheckoutEnabled>true</CheckoutEnabled>
      <ConvertedBuyItNowPrice currencyID="USD">0.0</ConvertedBuyItNowPrice>
      <ConvertedStartPrice currencyID="USD">180.0</ConvertedStartPrice>
      <HasReservePrice>false</HasReservePrice>
      <StartTime>2017-08-30T23:59:34.000Z</StartTime>
      <EndTime>2017-09-02T07:58:45.000Z</EndTime>
      <ViewItemURL>http://www.ebay.com/itm/YUNEEC-CGO3-4K-3-Axis-Gimbal-Camera-Typhoon-Q500-4K-Quadcopter-YUNCGO3US-/122677536317</ViewItemURL>
      <HasUnansweredQuestions>true</HasUnansweredQuestions>
      <HasPublicMessages>false</HasPublicMessages>
      <ViewItemURLForNaturalSearch>http://www.ebay.com/itm/YUNEEC-CGO3-4K-3-Axis-Gimbal-Camera-Typhoon-Q500-4K-Quadcopter-YUNCGO3US-/122677536317</ViewItemURLForNaturalSearch>
    </ListingDetails>
    <ListingDuration>Days_30</ListingDuration>
    <ListingType>FixedPriceItem</ListingType>
    <Location>Los Angeles, California</Location>
    <PaymentMethods>PayPal</PaymentMethods>
    <PrimaryCategory>
      <CategoryID>179697</CategoryID>
      <CategoryName>Cameras &amp; Photo:Camera Drones</CategoryName>
    </PrimaryCategory>
    <PrivateListing>false</PrivateListing>
    <Quantity>1</Quantity>
    <ReviseStatus>
      <ItemRevised>false</ItemRevised>
    </ReviseStatus>
    <Seller>
      <AboutMePage>true</AboutMePage>
      <Email>Invalid Request</Email>
      <FeedbackScore>1528</FeedbackScore>
      <PositiveFeedbackPercent>99.3</PositiveFeedbackPercent>
      <FeedbackPrivate>false</FeedbackPrivate>
      <FeedbackRatingStar>Red</FeedbackRatingStar>
      <IDVerified>false</IDVerified>
      <eBayGoodStanding>true</eBayGoodStanding>
      <NewUser>false</NewUser>
      <RegistrationDate>2009-12-14T23:07:16.000Z</RegistrationDate>
      <Site>US</Site>
      <Status>Confirmed</Status>
      <UserID>hollywood.tennis</UserID>
      <UserIDChanged>false</UserIDChanged>
      <UserIDLastChanged>2009-12-14T23:07:14.000Z</UserIDLastChanged>
      <VATStatus>NoVATTax</VATStatus>
      <SellerInfo>
        <AllowPaymentEdit>false</AllowPaymentEdit>
        <CheckoutEnabled>true</CheckoutEnabled>
        <CIPBankAccountStored>false</CIPBankAccountStored>
        <GoodStanding>true</GoodStanding>
        <LiveAuctionAuthorized>false</LiveAuctionAuthorized>
        <MerchandizingPref>OptIn</MerchandizingPref>
        <QualifiesForB2BVAT>false</QualifiesForB2BVAT>
        <StoreOwner>true</StoreOwner>
        <StoreURL>http://www.stores.ebay.com/hollywoodtennisstore</StoreURL>
        <SafePaymentExempt>false</SafePaymentExempt>
      </SellerInfo>
      <MotorsDealer>false</MotorsDealer>
    </Seller>
    <SellingStatus>
      <BidCount>0</BidCount>
      <BidIncrement currencyID="USD">0.0</BidIncrement>
      <ConvertedCurrentPrice currencyID="USD">180.0</ConvertedCurrentPrice>
      <CurrentPrice currencyID="USD">180.0</CurrentPrice>
      <HighBidder>
        <AboutMePage>false</AboutMePage>
        <FeedbackScore>4</FeedbackScore>
        <PositiveFeedbackPercent>100.0</PositiveFeedbackPercent>
        <FeedbackRatingStar>None</FeedbackRatingStar>
        <IDVerified>false</IDVerified>
        <eBayGoodStanding>true</eBayGoodStanding>
        <NewUser>false</NewUser>
        <Status>Confirmed</Status>
        <UserID>i***s</UserID>
        <VATStatus>NoVATTax</VATStatus>
        <UserAnonymized>true</UserAnonymized>
      </HighBidder>
      <MinimumToBid currencyID="USD">180.0</MinimumToBid>
      <QuantitySold>1</QuantitySold>
      <ReserveMet>true</ReserveMet>
      <SecondChanceEligible>false</SecondChanceEligible>
      <ListingStatus>Completed</ListingStatus>
      <QuantitySoldByPickupInStore>0</QuantitySoldByPickupInStore>
    </SellingStatus>
    <ShippingDetails>
      <ApplyShippingDiscount>false</ApplyShippingDiscount>
      <CalculatedShippingRate>
        <WeightMajor measurementSystem="English" unit="lbs">0</WeightMajor>
        <WeightMinor measurementSystem="English" unit="oz">0</WeightMinor>
      </CalculatedShippingRate>
      <SalesTax>
        <SalesTaxPercent>0.0</SalesTaxPercent>
        <ShippingIncludedInTax>false</ShippingIncludedInTax>
      </SalesTax>
      <ShippingServiceOptions>
        <ShippingService>ShippingMethodStandard</ShippingService>
        <ShippingServiceCost currencyID="USD">0.0</ShippingServiceCost>
        <ShippingServicePriority>1</ShippingServicePriority>
        <ExpeditedService>false</ExpeditedService>
        <ShippingTimeMin>1</ShippingTimeMin>
        <ShippingTimeMax>5</ShippingTimeMax>
        <FreeShipping>true</FreeShipping>
      </ShippingServiceOptions>
      <ShippingType>Flat</ShippingType>
      <ThirdPartyCheckout>false</ThirdPartyCheckout>
      <ShippingDiscountProfileID>0</ShippingDiscountProfileID>
      <InternationalShippingDiscountProfileID>0</InternationalShippingDiscountProfileID>
      <ExcludeShipToLocation>Alaska/Hawaii</ExcludeShipToLocation>
      <ExcludeShipToLocation>US Protectorates</ExcludeShipToLocation>
      <ExcludeShipToLocation>Africa</ExcludeShipToLocation>
      <ExcludeShipToLocation>Asia</ExcludeShipToLocation>
      <ExcludeShipToLocation>Central America and Caribbean</ExcludeShipToLocation>
      <ExcludeShipToLocation>Europe</ExcludeShipToLocation>
      <ExcludeShipToLocation>Middle East</ExcludeShipToLocation>
      <ExcludeShipToLocation>North America</ExcludeShipToLocation>
      <ExcludeShipToLocation>Oceania</ExcludeShipToLocation>
      <ExcludeShipToLocation>Southeast Asia</ExcludeShipToLocation>
      <ExcludeShipToLocation>South America</ExcludeShipToLocation>
      <SellerExcludeShipToLocationsPreference>false</SellerExcludeShipToLocationsPreference>
    </ShippingDetails>
    <ShipToLocations>US</ShipToLocations>
    <Site>US</Site>
    <StartPrice currencyID="USD">180.0</StartPrice>
    <Storefront>
      <StoreCategoryID>1</StoreCategoryID>
      <StoreCategory2ID>0</StoreCategory2ID>
      <StoreURL>http://www.stores.ebay.com/hollywoodtennisstore</StoreURL>
    </Storefront>
    <TimeLeft>PT0S</TimeLeft>
    <Title>YUNEEC CGO3 4K 3-Axis Gimbal Camera for Typhoon Q500 4K Quadcopter YUNCGO3US</Title>
    <HitCount>114</HitCount>
    <LocationDefaulted>true</LocationDefaulted>
    <GetItFast>false</GetItFast>
    <BuyerResponsibleForShipping>false</BuyerResponsibleForShipping>
    <PostalCode>90046</PostalCode>
    <PictureDetails>
      <GalleryType>Gallery</GalleryType>
      <GalleryURL>http://i.ebayimg.com/00/s/MTA1OVgxNjAw/z/u1IAAOSwKM9Zp084/$_57.JPG?set_id=8800005007</GalleryURL>
      <PhotoDisplay>PicturePack</PhotoDisplay>
      <PictureURL>http://i.ebayimg.com/00/s/MTA1OVgxNjAw/z/u1IAAOSwKM9Zp084/$_57.JPG?set_id=8800005007</PictureURL>
      <PictureURL>http://i.ebayimg.com/00/s/MTA1OVgxNjAw/z/nz0AAOSwDcpZp086/$_57.JPG?set_id=8800005007</PictureURL>
      <PictureURL>http://i.ebayimg.com/00/s/MTA1OVgxNjAw/z/IUwAAOSw791Zp089/$_57.JPG?set_id=8800005007</PictureURL>
      <PictureURL>http://i.ebayimg.com/00/s/MTA1OVgxNjAw/z/u4gAAOSwKM9Zp08~/$_57.JPG?set_id=8800005007</PictureURL>
    </PictureDetails>
    <DispatchTimeMax>3</DispatchTimeMax>
    <ProxyItem>false</ProxyItem>
    <BuyerGuaranteePrice currencyID="USD">20000.0</BuyerGuaranteePrice>
    <BuyerRequirementDetails>
      <LinkedPayPalAccount>true</LinkedPayPalAccount>
    </BuyerRequirementDetails>
    <IntangibleItem>false</IntangibleItem>
    <ReturnPolicy>
      <ReturnsAcceptedOption>ReturnsNotAccepted</ReturnsAcceptedOption>
      <ReturnsAccepted>No returns accepted</ReturnsAccepted>
    </ReturnPolicy>
    <ConditionID>3000</ConditionID>
    <ConditionDescription>Removed from Working Drone. Works Perfectly. Comes only as shown. You get nothing else.</ConditionDescription>
    <ConditionDisplayName>Used</ConditionDisplayName>
    <PostCheckoutExperienceEnabled>false</PostCheckoutExperienceEnabled>
    <ShippingPackageDetails>
      <ShippingIrregular>false</ShippingIrregular>
      <ShippingPackage>PackageThickEnvelope</ShippingPackage>
      <WeightMajor measurementSystem="English" unit="lbs">0</WeightMajor>
      <WeightMinor measurementSystem="English" unit="oz">0</WeightMinor>
    </ShippingPackageDetails>
    <HideFromSearch>false</HideFromSearch>
    <eBayPlus>false</eBayPlus>
    <eBayPlusEligible>false</eBayPlusEligible>
  </Item>
</GetItemResponse>'''


def test_pprint():
    from pprint import pprint
    l = {'x': 1, 'y': 2, }
    pprint(l)
    pprint(locals())
    pprint(globals())
    print(vars(l))


def test_insert_category_ids_to_redis():
    from ..utils.data import db_redis
    redis = db_redis()
    ids = [11450, 15724, 63869, 15775, 155226, 11567, 63865, 11556, 11553, 63863, 11554, ]
    for id in ids:
        url = 'https://api.ebay.com/buy/browse/v1/item_summary/search?limit=200&category_ids={0}&fieldgroups=FULL'
        url = url.format(id)
        redis.lpush('ebay:category_urls', url)


if __name__ == '__main__':
    test_get_detail()
