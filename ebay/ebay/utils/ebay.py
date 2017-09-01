# -*- coding: utf-8 -*-
from requests import Request, Session
from base64 import b64encode


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
    return resp.content


if __name__ == '__main__':
    get_new_token()
