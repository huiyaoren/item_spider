# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from scrapy import Request, Spider
from ..items import ListingItem

logger = logging.getLogger(__name__)


class ListingSpider(Spider):
    name = "listing_spider"
    start_urls = [
        'https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?limit=3&category_ids=179697&fieldgroups=FULL',
    ]
    headers = {
        'Authorization': 'Bearer v^1.1#i^1#r^0#p^1#f^0#I^3#t^H4sIAAAAAAAAAOVXa2wUVRTe7W4LDbZFJPKQmGU0Io+ZvTO7s4+BLmxbmm7YPnDXglACd2futFNmZ5a5M7aLmNSaQARJVYyBBA0/NJHEGEEi8MNHGiUmqBVJNMYfiIgPfgCGmIaEoHdml7KtBCqUSOL+2dxzzz33O9/5zr1zQV9F5YKtTVuHq9yTyvb1gb4yt5udAioryhdWe8pml7tAiYN7X9+jfd5+z29LMMyqOeEJhHO6hpGvN6tqWHCMtZRlaIIOsYIFDWYRFkxRSMWbkwLHACFn6KYu6irlSzTUUiLLBgJARhkpEhXDIkus2rWYaZ3MZ+SICEOiFBQDGVmKknmMLZTQsAk1s5biABumQZQGbBpEBB4IfIjh2NAayteODKzoGnFhABVz4ArOWqME682hQoyRYZIgVCwRb0y1xhMNy1vSS/wlsWJFHlImNC08elSvS8jXDlUL3Xwb7HgLKUsUEcaUP1bYYXRQIX4NzG3Ad6iOyJAX+TBEnMRCAEMTQmWjbmSheXMctkWRaNlxFZBmKmb+VowSNjLdSDSLoxYSItHgs/9WWlBVZAUZtdTyuvhT8bY2KtYFNVXRNnfRxDmnIpijU3WraVbKiGxUQjzNyqEQJ3HR4kaFaEWax+xUr2uSYpOGfS26WYcIajSWm2AJN8SpVWs14rJpIyrxY0GRQzYaXmMXtVBFy+zS7LqiLCHC5wxvXYGR1aZpKBnLRCMRxk44FNVSMJdTJGrspKPFonx6cS3VZZo5we/v6elhegKMbnT6OQBY/+rmZErsQllIEV+71wv+yq0X0IqTiojISqwIZj5HsPQSrRIAWicV48KhAMsXeR8NKzbW+g9DSc7+0R0xUR0ispEgFwQZyIUBz4riRHRIrChSv40DZWCezkJjIzJzKhQRLRKdWVlkKJIQ4GUuEJERLYWiMh2MyjKd4aUQ0S5CAKFMRoxG/k+NMl6pp0Q9h9p0VRHzEyL4CRN7wJDaoGHm66w8GaeQSpjvHK/2b5gqtlO9i0navX4bidoxMAkCcwpjK5wR9axfh+Ros03rHdS+8Tj5M1ae6bQQNgkKidwu416kEIkwpFGk8S8ptOGdlkQhF/Y9pTqSbiFvRSrctIyTPIOfFhkDYd0yyEcG02pfPGl9I9JIG5uGrqrIaGfviImJu3L+o+vmhlmJqkJoXH+vZfYvz/Eb5O7td18Zj76heW9lzvIgyPF8hA/dUV3rnbqm83f1PL2N9Jp0bCLpLnwh+Ue/12Iu58f2uz8E/e6j5MkHwoBmF4L5FZ4nvZ77KEyOVAZDTcrovYwCZQYrnRp5jhiI2YjyOagYZRXutQ+dW3ql5KW4bx2YOfJWrPSwU0oejmDO9ZlytmZGFRsGUcCCCA/40BrwyPVZL/ugd3p8dbT5a+X3TyN9gwOHPG2Da3fv1UHViJPbXe4iEnbt/HKowaiuOfn9kqHZiNnfPXfyC9kT1e/vPeU7feznZcPW/Y9tpk7vufTXMrVzx4FPFlf0P/fn8ZWLzje2zk/un743MSvd9e0RF9h2hFkxc+abiHsW/xj/fNHUyIuXuRWpyY0XB5vPT8PtyWOzznonDS1o6j48e9vApgvvTYMHu6d2bLl8kk/O3X426J2R2nJ14IwA1+2sTLo2/CD9NFgzzT20a0rV8IHsYH3P85ci6TMfNMR+afjmu0OJmo6vPj485xWX+szxz4YPHjl34dfdHS+vaglvW/xF6i3x3dRh8OrQqpc6dm19/eo7/LrH511cuufoAxte+2NhNdgx66Pkhe1vzKtoajlx6mHPpreVQhn/BvNL7vbDDwAA',
        'Content-Type': 'application/json',
        'X-EBAY-C-ENDUSERCTX': 'affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>',
    }

    def start_requests(self):
        for url in self.start_urls:
            logger.info("start_request: " + url)
            yield Request(url, dont_filter=True, headers=self.headers, method='GET')

    def parse(self, response):
        logger.info(response)

        item = ListingItem()
        data = json.loads(response.text)

        # 商品数据
        if 'itemSummaries' in data.keys():
            for i in data['itemSummaries']:
                self.clean_item(item, i)
                yield item

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
