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
    c = config['product'][2]

    credentials = ':'.join([c['appid'], c['certid']])
    header = {'Authorization': b'Basic ' + b64encode(bytes(credentials, encoding="utf8")), }
    query = '?grant_type=client_credentials&redirect_uri={0}&scope=https://api.ebay.com/oauth/api_scope'
    query = query.format(c['runame'])
    url = 'https://api.ebay.com/identity/v1/oauth2/token' + query
    method = 'POST'

    s = Session()
    req = Request(headers=header, url=url, method=method)
    prepped = req.prepare()
    resp = s.send(prepped)
    logger.info(' '.join(["Get new ebay application token | http_code:", str(resp.status_code)]))
    logger.info(' '.join(['resp.content:', str(resp.content)]))
    result = json.loads(str(resp.content, encoding="utf-8"))
    print(result)
    return result['access_token']


if __name__ == '__main__':
    token = new_token()
    print(token)
