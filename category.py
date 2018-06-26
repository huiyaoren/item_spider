from multiprocessing.pool import Pool

import xmltodict
from requests import Request, Session
from lxml import etree

from ebay.ebay.utils.data import db_redis, db_mysql

'''
商品分类数据预处理
'''

def get_category_ids():
    url = 'https://api.ebay.com/ws/api.dll'
    headers = {
        'X-EBAY-API-SITEID': '0',
        'X-EBAY-API-COMPATIBILITY-LEVEL': '967',
        'X-EBAY-API-CALL-NAME': 'GetCategories',
    }
    data = '''
    <?xml version="1.0" encoding="utf-8"?>
        <GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
          <RequesterCredentials>
            <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**WJK3WQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6ABlYekDJGLqAydj6x9nY+seQ**ouMDAA**AAMAAA**ehZWrotDgQd9pDcPuDpINGM0QkytaRP+BCQpMxUEOaMHJDipqsYTIG2TBWTQzdK6XlTsg8y35SfTIU0BkYct92LeysRUz3PFmlVmozj9lDhinpP9PchYELQstQaw3WptY+a7a2aEluksC6f2uQ8MmSC09DSPph42cSfiE2BPAjyMVrJh2asx9zdZSqVv7v+f12YshxWOG5rRY41b5nWkTsQgnTULvY9hy85s5Kd7TDdJ+0RhkuFqfSRRkm7mr7YPbNkJFcVlbL0X2wWIwrDsize/0I/ut8l8CZ1gBQ8AadUwuhr9ngy8z3DEaSeFjlLy9voK82UUgasKMJMKp9otTa7nkM6oey5PhHoEXuj07u12pGzbrtI9wRKNqEA8hh0bm5cuq84eUcTENQ33Z6wxjXJl94DEzRw5Otk4iuetBVtpRIHgmGAeXNcw6r7ez9KUhaTUdXDFURCsC9hEaJStOhInpRVQZt3nckwcS2cHeySexFfDzHGkecGEp6ULfPFpw0Te9w7LMCgjyWCSAXLf4S1QLxRLTsH6dmbiWnpRSq9uvgH/P6NIPgKrhhAEVw7zvp4+BmaWGeg8O0/7OC4UiSP5wAxvc1i0v7RQxUxUkJfR0tqokcwfJQJ2Acp40iVidC52CnuMRR9THvx1Iyr5kGax1Qqcd43n+CiMMB2rL6FFwcHhvnBK9QQbyQZLmy4octpPCK3tY8gl864X1htDH1Le+zu87dSx+j+PIX8oElfRubcNroHFjZyJwoS3g/3B</eBayAuthToken>
          </RequesterCredentials>
            <ErrorLanguage>en_US</ErrorLanguage>
            <WarningLevel>High</WarningLevel>
             <!--Ensure that site ID, in the Header, is set to the site you want-->
          <DetailLevel>ReturnAll</DetailLevel>
          <ViewAllNodes>true</ViewAllNodes>
        </GetCategoriesRequest>
    '''
    method = 'POST'
    s = Session()
    req = Request(headers=headers, url=url, method=method, data=data)
    prepped = req.prepare()
    resp = s.send(prepped)
    print(resp.content)
    r = str(resp.content, encoding='utf8')
    data = dict(xmltodict.parse(r).get('GetCategoriesResponse'))
    print(data)


def save_leaf_category(file):
    redis = db_redis()

    with open('{0}.xml'.format(file)) as f:
        xml = bytes(f.read(), 'utf8')
    data = etree.HTML(xml)
    result = data.xpath('//html/body/getcategoriesresponse/categoryarray/category')

    count = 0
    for category in result:
        leaf = category.xpath('leafcategory/text()')
        if len(leaf) > 0 and leaf[0] == 'true':
            count += 1
            id = category.xpath('categoryid/text()')[0]
            redis.sadd('ebay:leaf_category_ids_us', int(id))

    print()
    print(file)
    print(count)
    print(len(result))


mysql = db_mysql()


def get_parent(category_id):
    # sql = 'SELECT platform_parent_id FROM erp_saas_goods_category WHERE platform_category_id=%(category_id)s LIMIT 1'
    sql = 'SELECT platform_parent_id FROM erp_saas_goods_category WHERE platform_category_id=%(category_id)s and site=0 limit 1'
    c = mysql.cursor()
    c.execute(sql, {'category_id': category_id})
    result = c.fetchall()
    return result


def get_top_parent(category_id):
    parent = None
    l = 1
    while l > 0:
        result = get_parent(category_id)
        l = len(result)
        parent = result[0][0]
        if parent == category_id:
            break
        category_id = parent
    return parent


def all_category_in_mysql():
    sql = 'SELECT platform_category_id FROM erp_saas_goods_category GROUP BY platform_category_id'
    c = mysql.cursor()
    c.execute(sql)
    result = c.fetchall()
    for category_id in result:
        yield category_id[0]


def all_category_in_redis(key='ebay:leaf_category_ids_us'):
    r = db_redis()
    ids = r.smembers('ebay:leaf_category_ids_us')
    for id in ids:
        yield int(id)


def save_all_top_category():
    redis = db_redis()
    top_set = set()
    # todo 由 mysql 改为从 redis leaf_category 获取
    for id in all_category_in_redis():
        top = get_top_parent(id)
        top_set.add(top)
        # print(id, top)
        redis.hset('ebay:top_category_id_us', int(id), int(top))
    print(top_set)
    print(len(top_set))


def save_all_leaf_category():
    # todo 只选取美国站点的分类 而不是所有站点
    list = [0, 2, 3, 15, 16, 71, 77, 101, 193, 201, 210]
    for i in list[:1]:
        save_leaf_category(i)


def count_category(category_id):
    url = 'https://svcs.ebay.com/services/search/FindingService/v1'
    headers = {
        'X-EBAY-SOA-SECURITY-APPNAME': 'hanlinzh-sampleap-PRD-5090738eb-9f22a2e9',
        'X-EBAY-SOA-OPERATION-NAME': 'findItemsByCategory',
        'X-EBAY-SOA-GLOBAL-ID': 'EBAY-US',
    }
    data = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <findItemsByCategoryRequest xmlns="http://www.ebay.com/marketplace/search/v1/services">
      <categoryId>{0}</categoryId>
      <paginationInput>
        <entriesPerPage>1</entriesPerPage>
      </paginationInput>
    </findItemsByCategoryRequest>
    '''.format(category_id).strip()
    method = 'POST'
    s = Session()
    req = Request(headers=headers, url=url, method=method, data=data)
    prepped = req.prepare()
    resp = s.send(prepped)
    result = etree.HTML(resp.content)
    data = result.xpath('/html/body/finditemsbycategoryresponse/paginationoutput/totalentries/text()')[0]
    print('{0}: {1}'.format(category_id, data))
    return int(data)


def count_categories(category_list=None):
    category_list = category_list or [1, 10542, 11116, 11232, 11233, 11450, 11700, 11730, 1249, 12576, 1281, 1293, 1305,
                                      131090, 142313, 14308, 14339, 14675, 15032, 159912, 170638, 170769, 172008,
                                      172009, 172176, 20081, 20710, 220, 22128, 237, 260, 26395, 267, 281, 293, 2984,
                                      316, 3187, 3252, 353, 40005, 45099, 45100, 550, 58058, 6000, 619, 625, 62682, 63,
                                      64482, 870, 888, 9800, 9815, 99, ]
    pool = Pool()
    for category in category_list:
        # count_category(category)
        # break
        pool.apply_async(func=count_category, args=(int(category),))
    pool.close()
    pool.join()

def main():
    # 1.从 xml 文件中提取末级分类 id 至 redis
    save_leaf_category(0)
    # 2.从 redis 中的末级分类搜索 mysql 中的顶级分类 将映射关系写入 redis
    save_all_top_category()


if __name__ == '__main__':
    count_categories()
    dic = {
        11232: 4895679,
        11233: 13556103,
        1: 33300653,
        1249: 2660856,
        11450: 48956298,
        11700: 39753582,
        1281: 4107796,
        1305: 559210,
        12576: 23934377,
        14308: 1203716,
        14339: 13896309,
        159912: 5409333,
        172008: 19061,
        172009: 7821,
        15032: 34869272,
        20081: 2681660,
        20710: 767176,
        220: 14768448,
        237: 1893366,
        260: 4724418,
        26395: 17905569,
        293: 7067239,
        316: 130522,
        2984: 2182334,
        267: 37461836,
        281: 37855249,
        3252: 415998,
        3187: 3393966,
        45100: 3532554,
        550: 4692978,
        619: 2506340,
        58058: 12760319,
        625: 2248727,
        63: 3864432,
        6000: 63366019,
        870: 3021750,
        64482: 29742728,
        888: 17537810,
        99: 454650
    }
    # for j in [i for i in sorted(dic.items(), key=lambda x: x[1])]:
    #     print(j)
