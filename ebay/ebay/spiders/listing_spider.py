# -*- coding: utf-8 -*-
from scrapy import Item, Field, Request, Spider
from ..utils.ebay import get_new_token


class ListingSpider(Spider):
    name = "listing_spider"
    start_urls = [
        'http://www.baidu.com',
        'http://www.baidu.com',
        'http://www.baidu.com',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True)
        get_new_token()

    def parse(self, response):
        print(response.text)


class LinkItem(Item):
    name = Field()
    link = Field()
