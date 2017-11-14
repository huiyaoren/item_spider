from datetime import datetime

import logging
from requests import Request, Session

from . import app
from flask import render_template, json
import psutil
from redis import Redis
from pymongo import MongoClient

r = Redis(host='192.168.1.192')
m = MongoClient('192.168.1.192')['test_database']
cpu_count_logical = psutil.cpu_count()
cpu_count = psutil.cpu_count(logical=False)


# import multiprocessing
# logger = multiprocessing.log_to_stderr()
# logger.setLevel(multiprocessing.SUBDEBUG)

def response(request, queue):
    # s = Session()
    # req = Request(headers=request['headers'], url=request['url'], method=request['method'], data=request['data'])
    # prepped = req.prepare()
    # resp = s.send(prepped)
    # # queue.put(str(resp.content, encoding='utf8'))
    # result = str(resp.content, encoding='utf8')
    # print()
    # print(result[:200])
    # return result
    print(123)


@app.route('/')
def index():
    data = {}
    data['cpu_count_logical'] = psutil.cpu_count()
    data['cpu_count'] = psutil.cpu_count(logical=False)
    data['cpu_times'] = psutil.cpu_times()
    data['net_io_counters'] = psutil.net_io_counters()
    data['virtual_memory'] = psutil.virtual_memory()
    data['disk_partitions'] = psutil.disk_partitions()
    data['boot_time'] = psutil.boot_time()
    data['users'] = psutil.users()
    data['pids'] = psutil.pids()
    data['process'] = psutil.Process(data['pids'][0])
    data['cpu_percent'] = psutil.cpu_percent(interval=1)
    return render_template('index.html', data=data)
    # return 'hello world'


@app.route('/data', methods=['post', 'get'])
def data():
    data = {}
    # CPU
    data['cpu_percent'] = psutil.cpu_percent(interval=1)
    data['cpu_count_logical'] = cpu_count_logical
    data['cpu_count'] = cpu_count
    # MEM
    data['virtual_memory'] = psutil.virtual_memory()
    # NET
    network = psutil.net_io_counters(pernic=True)
    data['network'] = {}
    data['network']['device'] = ' | '.join(network.keys())
    data['network']['recv'] = sum([network[i].bytes_recv for i in network])
    data['network']['sent'] = sum([network[i].bytes_sent for i in network])
    del network
    # REDIS
    data['redis'] = {}
    data['redis']['category_ids'] = r.llen('ebay:category_ids')
    data['redis']['item_ids'] = r.llen('ebay:item_ids')
    data['redis']['item_ids_filter'] = r.scard('ebay:item_ids_filter')
    data['redis']['item_ids_filter_hyper'] = r.pfcount('ebay:item_ids_filter_hyper')
    data['redis']['tokens'] = r.zcard('ebay:tokens')
    data['redis']['appid'] = r.zcard('ebay:appid')
    data['redis']['shop:amount'] = r.hlen('ebay:shop:amount')
    data['redis']['shop:basic'] = r.hlen('ebay:shop:basic')
    data['redis']['shop:count'] = r.hlen('ebay:shop:count')
    data['redis']['shop:has_sold_count'] = r.hlen('ebay:shop:has_sold_count')
    data['redis']['shop:last_week_sold'] = r.hlen('ebay:shop:last_week_sold')
    data['redis']['shop:total_sold'] = r.hlen('ebay:shop:total_sold')
    data['redis']['shop:week_sold'] = r.hlen('ebay:shop:week_sold')
    data['redis_data'] = {}
    data['redis_data']['used_memory'] = r.info()['used_memory']

    # MONGODB
    collection_name = 'd_{0}'.format(datetime.now().strftime("%Y%m%d"))
    data['mongodb'] = {}
    data['mongodb']['count'] = m[collection_name].count()
    data['mongodb']['collection'] = collection_name
    # PROCESS
    for proc in psutil.process_iter(attrs=[
        'pid',
        'name',
        'status',
        'create_time',
        'cpu_percent',
        'memory_info',
        'memory_full_info',
        'memory_percent'
    ]):
        if proc.info['name'] == 'mongod':
            data['mongodb']['cpu_percent'] = proc.info['cpu_percent']
            data['mongodb']['pid'] = proc.info['pid']
            data['mongodb']['create_time'] = proc.info['create_time']
            data['mongodb']['memory_percent'] = proc.info['memory_percent']
            data['mongodb']['memory'] = proc.info['memory_info'].vms
        if proc.info['name'] == 'redis-server' or proc.info['name'] == 'redis':
            data['redis_data'] = {}
            data['redis_data']['cpu_percent'] = proc.info['cpu_percent']
            data['redis_data']['pid'] = proc.info['pid']
            data['redis_data']['create_time'] = proc.info['create_time']
            data['redis_data']['memory_percent'] = proc.info['memory_percent']
            data['redis_data']['memory'] = proc.info['memory_info'].vms
            data['redis_data']['used_memory'] = r.info()['used_memory']
        if proc.info['name'] == 'python' or proc.info['name'] == 'scrapy':
            pass
    # data['disk_partitions'] = psutil.disk_partitions()
    # data['boot_time'] = psutil.boot_time()
    # data['users'] = psutil.users()
    # data['Process'] = psutil.Process(data['pids'][0])
    return json.jsonify(data)


@app.route('/curl', methods=['post', 'get'])
def curl():
    from multiprocessing import Pool, Pipe, Queue
    url = 'https://api.ebay.com/ws/api.dll'
    data = '''
    <?xml version="1.0" encoding="utf-8"?>
        <GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
          <RequesterCredentials>
            <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**TFk/WQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6ACkoWoD5CHoQydj6x9nY+seQ**kMADAA**AAMAAA**7VtL67+uDGoPGwpzzegnSCLgL9ZwsNRQHBaZ8T6zTQuqDg8NXWGU37zosAe7c/KcRGEzb60QX3nV1ujxFDsMwI9Kw4CAPTqVOBXz72l6mhT9m2oiVX0dCAsYd0GKMTgIrO1+uhizmiIXej3Uh7NIF8L/76k/tiS/E304JsrTmKrk2r2Rr+dST1ONfj8fb5TFzeDen0hmBzgRctchyjPesIFTRd7WupOtbi6ciScQ/yYCqfH7GRGQADCIaiMnIpdQUfnwigoNoi4OyP/mH7tr03WfCDlHTAi1Ret2LsfXh0UAYi8rwuMtVSAvP52fRtwe4lom3DzBt2jB7U7rj8KZ89ea30SAIXVsag/vo3B0jkl64pSB5/zKbBPRrG5qZ+28aDKuUSuAfn9lPNCF//esp4QIF7HIPUeioLgQK5WoPT9/BCPmn0Y+tNMAPSEcUWTY42WwahoN1eYpBgqX/hZolTvupd5907NkDTxYHfij6WtcGQdHfHBWCPGHrgWcdLefochtz7pDpVzdHYCUQbv4bVzHQNbVfhNHCMp4LZ63qrkJVpWsmSeSgZi5dVECI7gp0t/Rq1y5uBsRJK6OViZS02jYw0MR7kjAyrIsK43bP4Pz8wwvpfyuaoxkgvziCaM35taQuB3qlUPeawULUSFX6olCC0kMZqdUT5HPqYD2+YTj2n0wBXvP7Lbkj3gejSbelCwS6XHdKqAXP2gY93eBtbogLic7//FGdnQvbbISceo/9hgdXKbNBcMh0zoQ0KRm</eBayAuthToken>
          </RequesterCredentials>
            <ErrorLanguage>en_US</ErrorLanguage>
            <WarningLevel>High</WarningLevel>
              <!--Enter an ItemID-->
          <ItemID>112548339313</ItemID>
        </GetItemRequest>
    '''
    headers = {
        'X-EBAY-API-SITEID': '0',
        'X-EBAY-API-COMPATIBILITY-LEVEL': '967',
        'X-EBAY-API-CALL-NAME': 'GetItem',
    }
    method = 'POST'
    requests = [
        {
            'url': url,
            'data': data,
            'headers': headers,
            'method': method,
        },
    ]
    start = datetime.now()
    pool = Pool()
    queue = Queue(16)
    for request in requests:
        print('request')
        pool.apply_async(response, args=(request, queue,))
    pool.close()
    pool.join()
    print(str(datetime.now() - start))
    return str(datetime.now() - start)
    return json.jsonify(response(url, headers, data, method))
