# -*- coding: utf-8 -*-
from scrapy import Item, Field, Request, Spider


class TestSpider(Spider):
    name = "test_spider"
    start_urls = [
        'http://www.baidu.com',
        'http://www.baidu.com',
        'http://www.baidu.com',
    ]

    def start_requests(self):
        # for url in self.start_urls:
        #     yield Request(url, dont_filter=True)
        yield get_new_token()

    def parse(self, response):
        print(response.text)
