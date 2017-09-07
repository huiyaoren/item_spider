# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from ..items import ListingItem
from ..utils.ebay import new_token
from ..utils.common import bytes_to_str

logger = logging.getLogger(__name__)


class DetailJsonRedisSpider(RedisSpider):
    name = "detail_json_redis_spider"
    redis_key = "ebay:item_urls"
    token = None
    headers = {
        'Authorization': 'Bearer ',
        'Content-Type': 'application/json',
        'X-EBAY-C-ENDUSERCTX': 'contextualLocation=country=<2_character_country_code>,zip=<zip_code>,affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>',
    }

    def __init__(self):
        super().__init__()
        self.token = new_token()  # todo 若要改为分布式 此项应存至 Redis
        self.headers['Authorization'] += self.token

    def make_request_from_data(self, data):
        url = bytes_to_str(data, self.redis_encoding)
        return Request(url, dont_filter=True, headers=self.headers, method='GET')

    def parse(self, response):
        item = ListingItem()
        data = json.loads(response.text)
        item = self.clean_item(item, data)
        yield item

    def clean_item(self, item, data):
        i = data
        item['itemId'] = i.get('itemId')
        item['title'] = i.get('title')
        item['image'] = i.get('image')
        item['itemWebUrl'] = i.get('itemWebUrl')

        item['time'] = datetime.utcnow()
        item['data'] = i

        item['itemLocation'] = i.get('itemLocation.country')
        item['sold'] = i.get('estimatedAvailabilities.estimatedSoldQuantity')
        item['price'] = i.get('price.value')
        item['currency'] = i.get('price.currency')
        item['sellerName'] = i.get('seller.username')
        item['sellerFeedbackPercentage'] = i.get('seller.feedbackPercentage')
        item['sellerFeedbackScore'] = i.get('seller.feedbackScore')
        return item
