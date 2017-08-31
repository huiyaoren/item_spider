# -*- coding: utf-8 -*-

from scrapy import Item, Field, Request, Spider


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

    def parse(self, response):
        pass


class LinkItem(Item):
    name = Field()
    link = Field()
