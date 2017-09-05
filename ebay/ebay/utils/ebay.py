# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from requests import Request, Session
from base64 import b64encode
from ..configs.ebay_config import config

logger = logging.getLogger(__name__)


def new_token():
    """ Get new ebay application token """
    c = config['product_1']

    credentials = ':'.join([c['appid'], c['certid']])
    header = {'Authorization': b'Basic ' + b64encode(bytes(credentials, encoding="utf8")), }
    query = '?grant_type=client_credentials&redirect_uri={0}&scope=https://api.ebay.com/oauth/api_scope'
    query = query.format(c['runame'])
    url = 'https://api.ebay.com/identity/v1/oauth2/token' + query
    method = 'POST'

    # credentials = b'hanlinzh-sampleap-SBX-1dbc19de5-1f662d29:SBX-dbc19de52c7f-0bb2-46d9-aba5-e2ac'
    # header = {'Authorization': b'Basic ' + b64encode(credentials), }
    # query = '?grant_type=client_credentials&redirect_uri=hanlin_zheng-hanlinzh-sample-wbcrx&scope=https://api.ebay.com/oauth/api_scope'
    # url = 'https://api.sandbox.ebay.com/identity/v1/oauth2/token' + query

    s = Session()
    req = Request(headers=header, url=url, method=method)
    prepped = req.prepare()
    resp = s.send(prepped)
    logger.info(' '.join(["Get new ebay application token | http_code:", str(resp.status_code)]))
    logger.info(' '.join(['resp.content:', str(resp.content)]))
    result = json.loads(str(resp.content, encoding="utf-8"))
    print(result)
    return result['access_token']


def item_detail():
    # todo-1
    header = {
       'X-EBAY-API-APP-ID': 'hanlinzh-sampleap-PRD-5090738eb-9f22a2e9',
       'X-EBAY-API-SITE-ID': '0',
       'X-EBAY-API-CALL-NAME': 'GetMultipleItems',
       'X-EBAY-API-VERSION': '863',
       'X-EBAY-API-REQUEST-ENCODING': 'xml',
    }
    url = 'https://open.api.ebay.com/shopping'
    method = 'POST'
    data='''<?xml version="1.0" encoding="utf-8"?>
<GetMultipleItemsRequest xmlns="urn:ebay:apis:eBLBaseComponents">
   	<!-- Enter valid item IDs that exist in the environment 
        (Sandbox, Production, etc.) you are using --> 
     <ItemID>xxxxxxxxxxxx</ItemID>
  	<ItemID>xxxxxxxxxxxx</ItemID>
</GetMultipleItemsRequest>'''

    s = Session()
    req = Request(headers=header, url=url, method=method, data=data)
    prepped = req.prepare()
    resp = s.send(prepped)
    print(resp)
    return resp


if __name__ == '__main__':
    token = new_token()
    print(token)
