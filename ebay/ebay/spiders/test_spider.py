# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from scrapy import Request, Spider
from scrapy_redis.spiders import RedisSpider
from ..items import ListingItem
from ..utils.data import category_ids
from ..utils.ebay import new_token


logger = logging.getLogger(__name__)


class ListingRedisSpider(RedisSpider):
    name = "listing_redis_spider"
    redis_key = "ebay:start_urls"
    token = None
    headers = {
        'Authorization': 'Bearer ',
        'Content-Type': 'application/json',
        'X-EBAY-C-ENDUSERCTX': 'affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>',
    }

    def __init__(self):
        super().__init__()
        # 为 header 添加 token
        # self.token = new_token()  # todo 若要改为分布式 此项应存至 Redis
        # self.headers['Authorization'] += self.token

    # def start_requests(self):
    #     for category_id in category_ids():
    #         url = 'https://api.ebay.com/buy/browse/v1/item_summary/search?limit=200&category_ids={0}&fieldgroups=FULL'
    #         url = url.format(category_id)
    #         logger.info("start_request: " + url)
    #         yield Request(url, dont_filter=True, headers=self.headers, method='GET')

    def make_request_from_data(self, data):
        # todo 重写 添加 header
        url = bytes_to_str(data, self.redis_encoding)
        return Request(url='http://www.baidu.com')

    def parse(self, response):
        yield Request(url='http://www.baidu.com')

        # logger.info(response)
        # item = ListingItem()
        # data = json.loads(response.text)
        # # 下一页请求
        # if 'next' in data.keys():
        #     url_next = data['next']
        #     yield Request(url_next, dont_filter=True, headers=self.headers, method='GET')
        # # 商品数据
        # if 'itemSummaries' in data.keys():
        #     for i in data['itemSummaries']:
        #         l = self.clean_item(item, i)
        #         yield l


    def clean_item(self, item, data):
        i = data
        item['price'] = i.get('price')
        item['categories'] = i.get('categories')
        item['itemLocation'] = i.get('itemLocation')
        item['shippingOptions'] = i.get('shippingOptions')
        item['seller'] = i.get('seller')
        item['title'] = i.get('title')
        item['conditionId'] = i.get('conditionId')
        item['image'] = i.get('image')
        item['currentBidPrice'] = i.get('currentBidPrice')
        item['buyingOptions'] = i.get('buyingOptions')
        item['condition'] = i.get('condition')
        item['itemId'] = i.get('itemId')
        item['itemAffiliateWebUrl'] = i.get('itemAffiliateWebUrl')
        item['itemWebUrl'] = i.get('itemWebUrl')
        item['itemHref'] = i.get('itemHref')
        item['additionalImages'] = i.get('additionalImages')
        item['time'] = datetime.utcnow()
        item['data'] = i
        return item

import six


def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s