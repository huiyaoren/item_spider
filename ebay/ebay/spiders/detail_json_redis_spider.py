# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
from pprint import pprint

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
    # headers = {
    #     'Authorization': 'Bearer ',
    #     'Content-Type': 'application/json',
    #     'X-EBAY-C-ENDUSERCTX': 'contextualLocation=country=<2_character_country_code>,zip=<zip_code>,affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>',
    # }
    headers = {
        'Authorization': 'Bearer v^1.1#i^1#f^0#I^3#r^0#p^1#t^H4sIAAAAAAAAAOVXe2wURRjvXR+kIEgiomAhxyIpQW93du/2HpveJdeWC5XHHVzB0spjbneOLuztXnbmbC+glkIIjxBQEk2IJgXBoAYpsZZESYwRQ2IEReMj/CE1ETEhiAkCxgc4u3eUayU8i5B4d8llv/nmm+/3+37fzA7oqKictm7GuosjHcOcXR2gw+lw8CNAZUX5E6NKnePLS0CRg6Or4/GOss7Sn2swTGsZaR7CGUPHyNWe1nQs2cYQkzV1yYBYxZIO0whLRJYSkdmzJIEFUsY0iCEbGuNqqA8x3oDg83pR0ifyohBAKWrVr8RsNEKMH/F80ivL/qDgE0Xoo+MYZ1GDjgnUSYgRAO93gyD9NYKABATJA1ghGGxmXAuQiVVDpy4sYMJ2upI91yzK9fqpQoyRSWgQJtwQiSZikYb66XMaa7iiWOECDwkCSRYPfKozFORaALUsuv4y2PaWEllZRhgzXDi/wsCgUuRKMreRvk21CJCAgEcQvYGAH3qTQ0Jl1DDTkFw/D8uiKu6U7SohnagkdyNGKRvJ5Ugmhac5NERDvcv6m5uFmppSkRliptdGFkbicSacwgpMIWy627CGW6GuuePz6t1JUQlAj+z1u2U/CiRFERQWykcr0DxopTpDV1SLNOyaY5BaRLNGA7nxS2IRN9QppsfMSIpYGRX58aCfQ7HZKmq+ilnSqlt1RWlKhMt+vHEF+mcTYqrJLEH9EQYP2BSFGJjJqAozeNDWYkE+7TjEtBKSkTiura2NbfOwhrmMEwDguabZsxJyK0pDhvpavZ73V288wa3aUGREZ2JVIrkMzaWdapUmoC9jwlR7Pr+3wPvAtMKDrf8yFGHmBnbEUHWI4gGiByhQlAH0JUXPUHRIuCBSzsoDJWHOnYbmCkQyGpSRW6Y6y6aRqSqSR0wJnkAKuRVfMOX2BlMpS8A+N59CCCCUTMrBwP+pUW5W6gnZyKC4oalybkgEP2Ri95hKHJokl0CaRg03q/prgsQWyLsOz+r1W4JoxcA0CMyorKVtVjbSnAHppmaZlthZ3xFulZ6H91VRKcA8UlXJH2SsDZfFz8qsibCRNekZzsasfb3RWIF02iXENDQNmQv4O2Ji6Hb0e7SbXxOVrKmUxiX3G7Jb3CZvU9uQ3EPUZZ2Olmsg50XgDXq9/B1iq7Pr2pj7DzatWyrsDAMTpNyFFxBu4HUoXGJ/+E7He6DTsZ/eqAAHpvCTwaSK0vllpQ+MxypBrApTLFaX6fQt30TsCpTLQNV0VjhaqrrfXFJ0AetaBB7tv4JVlvIjiu5joOrqSDn/4CMjeT8I0m8ACB7QDCZfHS3jx5aN6fvti0t9u/vevcDtUb7u7rlk9s2Uwch+J4ejvIQqo+QY18v+9K1zz4Gvju+N7frwy1782NyWg+qxT17smPHx9tPduYOrD2xe/z35++jCsnH7Nz/5wqSXTj/H9/l/b3h65/wTy8/yq/Ty9cNOjllT3fTd6E3R4c7zf250gpr5nTvWbnj5ozNP1erq2dfnfbB66swt/iNR1/NTqlrXVi/uufjq+4Z+btH0zYI08Uxo7y912dCI1z7rXlM9oWnliXM1x3xv+bZ3tSwdP/aNT9dXrtr4zpaJp37ct+s8c/hw+7Z9P2zaWht7pXT18SN/JFfu9gg7Dx1tjp9q2vvwhVXN8c/3Xd5y8u0No2LP9Py188xD03qjwxcu3hEdvWgCWr7ydPTAoZapgqv65NJvtnGXfx1XlS/fP/a1YPUaDwAA',
        'Content-Type': 'application/json',
        'X-EBAY-C-ENDUSERCTX': 'contextualLocation=country=<2_character_country_code>,zip=<zip_code>,affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>'
    }

    def __init__(self):
        super().__init__()
        # self.token = new_token()  # todo 若要改为分布式 此项应存至 Redis
        # self.headers['Authorization'] += self.token

    def make_request_from_data(self, data):
        url = bytes_to_str(data, self.redis_encoding)
        # print(self.headers)
        print(url)
        # r = Request(url)
        r = Request(url, dont_filter=True, headers=self.headers, method='GET')
        # print(r)
        return r

    def parse(self, response):
        # print(response.text)
        item = ListingItem()
        # data = json.loads(response.text)
        # item = self.clean_item(item, data)
        # yield item

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
