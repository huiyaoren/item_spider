# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from scrapy import Request, Spider
from scrapy_redis.spiders import RedisSpider
from ..items import ListingItem
from ..utils.data import category_ids, db_redis
from ..utils.ebay import new_token
from ..utils.common import bytes_to_str

logger = logging.getLogger(__name__)


class ListingRedisSpider(RedisSpider):
    name = "listing_redis_spider"
    redis_key = "ebay:category_urls"
    token = None
    headers = {
        'Authorization': 'Bearer ',
        'Content-Type': 'application/json',
        'X-EBAY-C-ENDUSERCTX': 'affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>',
    }

    def __init__(self):
        super().__init__()
        # 为 header 添加 token
        self.token = new_token()  # todo 若要改为分布式 此项应存至 Redis
        self.headers['Authorization'] += self.token

    def make_request_from_data(self, data):
        # todo 重写 添加 header
        url = bytes_to_str(data, self.redis_encoding)
        return Request(url, dont_filter=True, headers=self.headers, method='GET')

    def parse(self, response):
        logger.info(response)
        item = ListingItem()
        data = json.loads(response.text)
        # 下一页请求
        if 'next' in data.keys():
            url_next = data['next']
            self.server.lpush('ebay:category_urls', url_next)
        # # 商品数据
        if 'itemSummaries' in data.keys():
            for i in data['itemSummaries']:
                l = self.clean_item(item, i)
                yield l

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
