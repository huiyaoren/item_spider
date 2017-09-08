from . import app
from flask import render_template, json
import psutil


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
    data['cpu_count_logical'] = psutil.cpu_count()
    data['cpu_count'] = psutil.cpu_count(logical=False)
    data['cpu_times'] = psutil.cpu_times()
    data['net_io_counters'] = psutil.net_io_counters()
    data['virtual_memory'] = psutil.virtual_memory()
    data['disk_partitions'] = psutil.disk_partitions()
    data['boot_time'] = psutil.boot_time()
    data['users'] = psutil.users()
    data['pids'] = psutil.pids()
    # data['Process'] = psutil.Process(data['pids'][0])
    data['cpu_percent'] = psutil.cpu_percent(interval=1)
    return json.jsonify(data)