import logging
from datetime import datetime

from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from ..utils.data import db_mongodb
from ..utils.common import bytes_to_str
from ..statics import Cleaner

logger = logging.getLogger(__name__)


class CleanSpider(RedisSpider):
    name = "clean_spider"
    redis_key = "ebay:item_ids_unclean"
    date = datetime.now().strftime("%Y%m%d")
    mongodb = db_mongodb()

    def __init__(self):
        super().__init__()
        self.cleaner = Cleaner(self.date, self.mongodb)

    def make_request_from_data(self, data):
        item_id = bytes_to_str(data, self.redis_encoding)
        print(item_id)
        self.cleaner.clean(item_id)

    def parse(self, response):
        print('parse')
        return
