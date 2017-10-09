class Token:
    def __init__(self, mongodb=None, redis=None):
        self.token = None
        self.redis = redis
        self.mongodb = mongodb
        self.collection = None if self.mongodb is None else self.mongodb['tokens']

    def one(self, redis=None):
        r = redis or self.redis
        self.token = r.zrange('ebay:tokens', 0, 0)[0]
        return str(self.token, encoding='utf8')

    def all(self, collection=None):
        c = collection or self.collection
        for i in c.find():
            yield str(i.get('token', ''), encoding='utf8')

    def use(self, redis=None):
        r = redis or self.redis
        r.zincrby('ebay:tokens', self.token, 1)

    def reset_all(self, redis=None):
        r = redis or self.redis
        r.delete('ebay:tokens')
        c = self.collection
        for i in c.find():
            r.zadd('ebay:tokens', i['token'], 0)
        print('Reset Token Done.')

    def copy_all(self, mongodb_remote):
        c = self.collection
        c_remote = mongodb_remote['tokens']
        c_remote.remove()
        for i in c.find():
            i.pop('_id')
            c_remote.insert_one(i)
        print('Copy Token Done.')

