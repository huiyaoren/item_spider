# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

import xmltodict
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from ..configs.ebay_config import config
from ..items import ListingItem
from ..utils.common import bytes_to_str
from ..utils.data import token_from_redis

logger = logging.getLogger(__name__)


class DetailXmlRedisSpider(RedisSpider):
    name = "detail_xml_redis_spider"
    redis_key = "ebay:item_ids"
    token = config['product'][2]['token_old']
    url = 'https://api.ebay.com/ws/api.dll'
    headers = {
        'X-EBAY-API-SITEID': '0',
        'X-EBAY-API-COMPATIBILITY-LEVEL': '967',
        'X-EBAY-API-CALL-NAME': 'GetItem',
    }
    data = '''
        <?xml version="1.0" encoding="utf-8"?>
            <GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
                <RequesterCredentials>
                    <eBayAuthToken>{0}</eBayAuthToken>
                </RequesterCredentials>
                <ErrorLanguage>en_US</ErrorLanguage>
                <WarningLevel>High</WarningLevel>
                <!--Enter an ItemID-->
                <ItemID>{1}</ItemID>
            </GetItemRequest>
    '''

    def make_request_from_data(self, data):
        item_id = bytes_to_str(data, self.redis_encoding)
        token = token_from_redis(self.server)
        body = self.data.format(token, item_id)
        return Request(self.url, dont_filter=True, headers=self.headers, method='POST', body=body)

    def parse(self, response):
        item = {}
        data = dict(xmltodict.parse(response.text))
        data = data.get('GetItemResponse')

        if 'Ack' not in data.keys() or data.get('Ack') == 'Failure':
            logger.warning('Request Failre. \n\nurl: {0} data: {1}'.format(response.url, response.text))
            return
        try:
            i = self.clean_item(item, data.get('Item'))
        except AttributeError:
            logger.warning('Get Item Error. \n\nurl: {0} data: {1}'.format(response.url, response.text))
        else:
            del data
            yield i

    def clean_item(self, item, data):
        i = data
        item['price'] = i.get('SellingStatus').get('CurrentPrice').get('#text')
        item['country'] = i.get('Country')
        item['currency'] = i.get('Currency')
        item['itemId'] = i.get('ItemID')
        item['startTime'] = i.get('ListingDetails').get('StartTime')
        item['viewItemURL'] = i.get('ListingDetails').get('ViewItemURL')
        item['categoryID'] = i.get('PrimaryCategory').get('CategoryID')
        item['feedbackScore'] = i.get('Seller').get('FeedbackScore')
        item['positiveFeedbackPercent'] = i.get('Seller').get('PositiveFeedbackPercent')
        item['newUser'] = i.get('Seller').get('NewUser')
        item['registrationDate'] = i.get('Seller').get('RegistrationDate')
        item['storeURL'] = i.get('Seller').get('SellerInfo').get('StoreURL')
        item['quantitySold'] = i.get('SellingStatus').get('QuantitySold')
        item['image'] = i.get('PictureDetails').get('GalleryURL')
        item['hitCount'] = i.get('HitCount')
        item['title'] = i.get('Title')
        item['shipToLocations'] = i.get('ShipToLocations')
        item['site'] = i.get('Site')
        item['seller'] = i.get('Seller').get('UserID')
        return item
