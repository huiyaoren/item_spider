from lxml import etree

import requests


class Token:
    def __init__(self, mongodb=None, redis=None):
        self.token = None
        self.redis = redis
        self.mongodb = mongodb
        self.collection = None if self.mongodb is None else self.mongodb['tokens']

    def one(self, redis=None):
        r = redis or self.redis
        token = r.zrange('ebay:tokens', 0, 0)[0]
        return str(token, encoding='utf8')

    def all(self, collection=None):
        c = collection or self.collection
        for i in c.find():
            yield i

    def use(self, redis=None):
        r = redis or self.redis
        r.zincrby('ebay:tokens', self.token, 1)

    def reset_all(self, redis=None):
        r = redis or self.redis
        r.delete('ebay:tokens')
        for token in self.all():
            r.zadd('ebay:tokens', token['token'], 0)
        print('Reset Token Done.')

    def copy_all(self, mongodb_remote=None):
        c_remote = mongodb_remote['tokens']
        c_remote.remove()
        for token in self.all():
            token.pop('_id')
            c_remote.insert_one(token)
        print('Copy Token Done.')

    def check_all(self):
        for token in self.all():
            self.check(token)

    def check(self, token):
        print(token)
        url = 'https://api.ebay.com/ws/api.dll'
        headers = {
            'X-EBAY-API-SITEID': '0',
            'X-EBAY-API-COMPATIBILITY-LEVEL': '967',
            'X-EBAY-API-CALL-NAME': 'GetTokenStatus',
            'X-EBAY-API-APP-NAME': token['app_id'],
            'X-EBAY-API-DEV-NAME': token['dev_id'],
            'X-EBAY-API-CERT-NAME': token['cert_id'],
        }
        data = '''
        <?xml version="1.0" encoding="utf-8"?>
            <GetTokenStatusRequest xmlns="urn:ebay:apis:eBLBaseComponents">
              <RequesterCredentials>
                <eBayAuthToken>{token}</eBayAuthToken>
              </RequesterCredentials>
                <ErrorLanguage>en_US</ErrorLanguage>
                <WarningLevel>High</WarningLevel>
            </GetTokenStatusRequest>'''.format(token=token['token'])

        resp = requests.post(url=url, headers=headers, data=data)
        result = etree.HTML(resp.content)

        ack = result.xpath('/html/body/gettokenstatusresponse/ack/text()')[0]
        if ack != 'Success':
            print('Ack is not success. response: \n{0}'.format(resp.text))
            return False

        status = result.xpath('/html/body/gettokenstatusresponse/tokenstatus/status/text()')[0]
        if status != 'Active':
            print('Token is not active. response: \n{0}'.format(resp.text))
            return False

        print('Token is active')
        return True
