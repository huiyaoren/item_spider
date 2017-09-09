from . import app
from flask import render_template, json
import psutil
from redis import Redis
from pymongo import MongoClient

r = Redis()
m = MongoClient()['test_database']
collection_name = 'd_20170908'
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

    data['mongodb'] = {}
    data['mongodb']['count'] = m[collection_name].count()

    data['pids'] = psutil.pids()
    # for proc in psutil.process_iter(attrs=['pid', 'name']):
    #     print(proc.info)
    # data['disk_partitions'] = psutil.disk_partitions()
    # data['boot_time'] = psutil.boot_time()
    # data['users'] = psutil.users()
    # data['Process'] = psutil.Process(data['pids'][0])
    return json.jsonify(data)