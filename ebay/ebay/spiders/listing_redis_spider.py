# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy_redis.spiders import RedisSpider

from ..items import ListingItem
from ..utils.ebay import new_token
from ..utils.common import bytes_to_str, clean_item_id
from ..utils.data import insert_item_id_to_redis, is_item_ids_enough

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
        self.token = new_token()  # todo 若要改为分布式 此项应存至 Redis
        self.headers['Authorization'] += self.token

    def make_request_from_data(self, data):
        # 生成 20000 条 item 测试队列 todo
        if False and is_item_ids_enough(20000):
            raise CloseSpider('Item ids are enough.')
        #
        url = bytes_to_str(data, self.redis_encoding)
        return Request(url, dont_filter=True, headers=self.headers, method='GET')

    def parse(self, response):
        logger.info(response)
        item = ListingItem()
        data = json.loads(response.text)
        # 下一页请求
        print('Offset: {0}. Total: {1}'.format(data['offset'], data['total']))
        if 'next' in data.keys() and int(data['offset']) <= int(data['total']):
            url_next = data['next']
            self.server.lpush('ebay:category_urls', url_next)
        # 商品数据
        if 'itemSummaries' in data.keys():
            for i in data['itemSummaries']:
                # yield self.clean_item(item, i)
                ''' Insert item url or item id '''
                if 'itemHref' in i.keys():
                    item_id = int(clean_item_id(i['itemId']))
                    insert_item_id_to_redis(item_id, self.server)
                    # insert_item_url_to_redis(item_id, i['itemHref'], self.server)

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
        item['itemId'] = clean_item_id(i.get('itemId'))
        item['itemAffiliateWebUrl'] = i.get('itemAffiliateWebUrl')
        item['itemWebUrl'] = i.get('itemWebUrl')
        item['itemHref'] = i.get('itemHref')
        item['additionalImages'] = i.get('additionalImages')
        item['time'] = datetime.utcnow()
        item['data'] = i
        return item
