# -*- coding: utf-8 -*-
import logging

from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from scrapy.utils.project import get_project_settings

from ..tests.time_recoder import log_time_with_name
from ..utils.common import bytes_to_str
from ..utils.data import token, insert_item_id_to_redis
from lxml import etree

logger = logging.getLogger(__name__)


class ListingXmlRedisSpider(RedisSpider):
    name = "listing_xml_redis_spider"
    redis_key = "ebay:category_ids"
    headers = {
        'X-EBAY-SOA-SECURITY-APPNAME': '',
        'X-EBAY-SOA-OPERATION-NAME': 'findItemsByCategory',
    }
    data = '''
        <?xml version="1.0" encoding="UTF-8"?>
        <findItemsByCategoryRequest xmlns="http://www.ebay.com/marketplace/search/v1/services">
            <categoryId>{0}</categoryId>
            <outputSelector>AspectHistogram</outputSelector>
            <paginationInput>
                <entriesPerPage>200</entriesPerPage>
                <pageNumber>{1}</pageNumber>
            </paginationInput>
        </findItemsByCategoryRequest>
    '''
    url = 'https://svcs.ebay.com/services/search/FindingService/v1'
    settings = get_project_settings()

    def make_request_from_data(self, data):
        category_id, page = bytes_to_str(data, self.redis_encoding).split(':')
        body = self.data.format(category_id, page).strip()
        self.headers['X-EBAY-SOA-SECURITY-APPNAME'] = token.one_appid()

        return Request(
            url=self.url,
            headers=self.headers,
            dont_filter=True,
            method='POST',
            body=body
        )

    # @log_time_with_name('parse')
    def parse(self, response):
        t = etree.HTML(bytes(response.text, encoding='utf8'))
        s = '/html/body/finditemsbycategoryresponse'

        # 异常处理
        ack = t.xpath(s + '/ack/text()')
        for ack_str in ack:
            if ack_str != 'Success':
                logger.warning('Response fail or warning. response: \n{0}'.format(response.text))
            break

        # 商品分类
        for page_current in t.xpath(s + '/paginationoutput/pagenumber/text()'):
            if int(page_current) == 1:
                category_ids = t.xpath(s + '/searchresult/item/primarycategory/categoryid/text()')
                category_id = max(category_ids, key=category_ids.count)

                page_total = t.xpath(s + '/paginationoutput/totalpages/text()')[0]
                for page in range(2, int(page_total) + 1):
                    if page > self.settings['CRAWL_PAGES']:
                        break
                    self.server.lpush('ebay:category_ids', '{0}:{1}'.format(category_id, page))
            break

        # 商品 id
        items = t.xpath(s + '/searchresult/item/itemid/text()')
        for item_id in items:
            insert_item_id_to_redis(item_id, self.server)
