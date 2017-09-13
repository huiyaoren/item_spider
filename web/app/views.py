from datetime import datetime

from . import app
from flask import render_template, json
import psutil
from redis import Redis
from pymongo import MongoClient

r = Redis(host='192.168.1.200', password='root')
m = MongoClient()['test_database']
cpu_count_logical = psutil.cpu_count()
cpu_count = psutil.cpu_count(logical=False)


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
    data['Process'] = psutil.Process(data['pids'][0])
    data['cpu_percent'] = psutil.cpu_percent(interval=1)
    return render_template('index.html', data=data)
    # return 'hello world'


@app.route('/data', methods=['post', 'get'])
def data():
    data = {}
    data['cpu_percent'] = psutil.cpu_percent(interval=1)
    data['virtual_memory'] = psutil.virtual_memory()
    data['cpu_count_logical'] = cpu_count_logical
    data['cpu_count'] = cpu_count

    data['redis'] = {}
    data['redis']['category_ids'] = r.llen('ebay:category_ids')
    data['redis']['category_urls'] = r.llen('ebay:category_urls')
    data['redis']['item_ids'] = r.llen('ebay:item_ids')
    data['redis']['item_ids_filter'] = r.scard('ebay:item_ids_filter')
    data['redis']['tokens'] = r.zcard('ebay:tokens')

    collection_name = 'd_{0}'.format(datetime.now().strftime("%Y%m%d"))
    data['mongodb'] = {}
    data['mongodb']['count'] = m[collection_name].count()
    data['mongodb']['collection'] = collection_name

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
        if proc.info['name'] == 'redis-server':
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
