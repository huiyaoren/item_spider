# -*- coding: utf-8 -*-
import logging
from requests import Request, Session
from base64 import b64encode

logger = logging.getLogger(__name__)


def get_new_token():
    """ Get new ebay application token """
    credentials = b'hanlinzh-sampleap-SBX-1dbc19de5-1f662d29:SBX-dbc19de52c7f-0bb2-46d9-aba5-e2ac'
    header = {
        'Authorization': b'Basic ' + b64encode(credentials),
    }
    print(header['Authorization'])
    query = '?grant_type=client_credentials&redirect_uri=hanlin_zheng-hanlinzh-sample-wbcrx&scope=https://api.ebay.com/oauth/api_scope'
    url = 'https://api.sandbox.ebay.com/identity/v1/oauth2/token' + query
    method = 'POST'
    # return Request(headers=header, url=url, method=method)

    s = Session()
    req = Request(headers=header, url=url, method=method)
    prepped = req.prepare()
    resp = s.send(prepped)
    logger.info(' '.join(["Get new ebay application token | http_code:", str(resp.status_code)]))
    logger.info(' '.join(['resp.content:', str(resp.content)]))
    return resp.content


def ebay_test():
    from ebaysdk.exception import ConnectionError
    from ebaysdk.trading import Connection as Trading

    try:
        api = Trading(config_file='ebay.yaml', debug=True)
        print(api.config.get('token'), 123)

        api.execute('GetTokenStatus', {'CharityID': 3897})
        # dump(api)
        print(api.response.reply)
        return api.response.reply

    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        return e.response.dict()


if __name__ == '__main__':
    get_new_token()
    # ebay_test()
