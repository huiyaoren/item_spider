# -*- coding: utf-8 -*-
import json
import logging
import os
from datetime import datetime
from pprint import pprint

from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from ..items import ListingItem
from ..utils.ebay import new_token
from ..utils.common import bytes_to_str, clean_item_id

logger = logging.getLogger(__name__)


class DetailJsonRedisSpider(RedisSpider):
    name = "detail_json_redis_spider"
    redis_key = "ebay:item_ids"
    token = None
    headers = {
        'Authorization': 'Bearer ',
        'Content-Type': 'application/json',
        'X-EBAY-C-ENDUSERCTX': 'contextualLocation=country=<2_character_country_code>,zip=<zip_code>',
    }

    def __init__(self):
        super().__init__()
        self.token = new_token()
        self.headers['Authorization'] += self.token

    def make_request_from_data(self, data):
        item_id = bytes_to_str(data, self.redis_encoding)
        url = 'https://api.ebay.com/buy/browse/v1/item/get_item_by_legacy_id?legacy_item_id={0}'
        url = url.format(item_id)
        return Request(url, dont_filter=True, headers=self.headers, method='GET')

    def parse(self, response):
        item = ListingItem()
        data = json.loads(response.text)
        item = self.clean_item(item, data)
        yield item

    def clean_item(self, item, data):
        i = data
        item['itemId'] = clean_item_id(i.get('itemId'))
        item['title'] = i.get('title')
        item['price'] = i.get('price').get('value')
        item['currency'] = i.get('price').get('currency')
        item['category'] = i.get('categoryPath')
        item['itemLocation'] = i.get('itemLocation').get('country')
        item['imageURL'] = i.get('image').get('imageUrl')
        item['sellerName'] = i.get('seller').get('username')
        item['sellerFeedbackPercentage'] = i.get('seller').get('feedbackPercentage')
        item['sellerFeedbackScore'] = i.get('seller').get('feedbackScore')
        item['quantitySold'] = i.get('estimatedAvailabilities')[0].get('estimatedSoldQuantity')
        item['itemURL'] = i.get('itemWebUrl')
        return item
