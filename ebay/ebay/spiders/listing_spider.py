# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from scrapy import Request, Spider
from ..items import ListingItem
from ..utils.data import category_ids
from ..utils.ebay import new_token

logger = logging.getLogger(__name__)


class ListingSpider(Spider):
    name = "listing_spider"
    start_urls = [
        'https://api.ebay.com/buy/browse/v1/item_summary/search?limit=200&category_ids=179697&fieldgroups=FULL',
    ]
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

    def start_requests(self):
        for category_id in category_ids():
            url = 'https://api.ebay.com/buy/browse/v1/item_summary/search?limit=200&category_ids={0}&fieldgroups=FULL'
            url = url.format(category_id)
            logger.info("start_request: " + url)
            yield Request(url, dont_filter=True, headers=self.headers, method='GET')

    def parse(self, response):
        logger.info(response)
        item = ListingItem()
        data = json.loads(response.text)
        # 商品数据
        if 'itemSummaries' in data.keys():
            for i in data['itemSummaries']:
                l = self.clean_item(item, i)
                yield l
        # 下一页请求
        if 'next' in data.keys():
            url_next = data['next']
            yield Request(url_next, dont_filter=True, headers=self.headers, method='GET')

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
