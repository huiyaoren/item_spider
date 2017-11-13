import xmltodict
from requests import Request, Session
from lxml import etree

from ebay.ebay.utils.data import db_redis, db_mysql


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
            redis.sadd('ebay:leaf_category_ids', int(id))

    print()
    print(file)
    print(count)
    print(len(result))


mysql = db_mysql()


def get_parent(category_id):
    sql = 'SELECT platform_parent_id FROM erp_saas_goods_category WHERE platform_category_id = %(category_id)s LIMIT 1'
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


def all_category():
    sql = 'SELECT platform_category_id FROM erp_saas_goods_category GROUP BY platform_category_id'
    c = mysql.cursor()
    c.execute(sql)
    result = c.fetchall()
    for category_id in result:
        yield category_id[0]


def save_all_top_category():
    redis = db_redis()
    top_set = set()
    for id in all_category():
        top = get_top_parent(id)
        top_set.add(top)
        # print(id, top)
        redis.hset('ebay:top_category_id', int(id), int(top))
    print(top_set)
    print(len(top_set))


def save_all_leaf_category():
    list = [0, 2, 3, 15, 16, 71, 77, 101, 193, 201, 210]
    for i in list:
        save_leaf_category(i)


if __name__ == '__main__':
    save_all_leaf_category()
