from scrapy_redis.dupefilter import RFPDupeFilter

class NoneDupeFilter(RFPDupeFilter):

    def request_seen(self, request):
        return False