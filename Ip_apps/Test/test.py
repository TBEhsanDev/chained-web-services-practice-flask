import json
import threading
import time
from pathlib import Path

import pymongo
import redis
import requests

from ..Log.log import log_file_path

log_file = Path(log_file_path)
log_file.touch(exist_ok=True)
lock = threading.Lock()
r = redis.Redis()
data = {
    'student': {'age': 32, 'name': 'ali', 'grades': [14, 18]}
}
client_ip = {'client_ip': '127.0.0.1'}
resp_test_with_json = data | client_ip
resp_test_empty_json = client_ip
resp_test_empty_body = client_ip
req_num = 200


def check_logs_content(start, end):
    with open(log_file_path, mode='r') as log:
        lines = log.readlines()
        for line in lines[start:end]:
            line = json.loads(line)
            del line['time']
            assert line == data


def check_mongodb(col, data, log_lines_num_in_db_before_req):
    json_data = json.dumps(data)
    items = col.find()
    for item in items[log_lines_num_in_db_before_req + 1:]:
        assert col.count() == log_lines_num_in_db_before_req + req_num
        assert data["student"] == item["student"]


def test_with_json():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ip_db']
    col = db['ip_collection']
    log_lines_num_in_db_before_req = col.count()
    log_lines_num_before_req = sum(1 for line in open(log_file_path))
    resp_200 = 0
    resp_429 = 0
    resp_502 = 0
    check = [resp_200, resp_429, resp_502]
    th = list()

    def with_json():
        lock.acquire()
        try:
            resp = requests.post(url="http://127.0.0.1/api/", json=data)
            if (resp.status_code == 200):
                assert resp.json() == resp_test_with_json
                check[0] += 1
            elif (resp.status_code == 429):
                assert resp.json() == "too many requests"
                check[1] += 1
        except:
            assert resp.status_code == 502
            check[2] += 1

        lock.release()

    r.delete('127.0.0.1')
    for _ in range(req_num):
        t = threading.Thread(target=with_json)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    log_lines_num_after_req = sum(1 for line in open(log_file_path))
    if (check[0] == 100) and (log_lines_num_after_req == log_lines_num_before_req + 100):
        check_logs_content(log_lines_num_before_req, log_lines_num_after_req)
        time.sleep(5)
        check_mongodb(col, data, log_lines_num_in_db_before_req)
    r.delete('127.0.0.1')


def test_empty_json():
    resp_200 = 0
    resp_502 = 0
    check = [resp_200, resp_502]
    th = list()
    log_lines_num_before_req = sum(1 for line in open(log_file_path))

    def empty_json():
        lock.acquire()
        try:
            resp = requests.post(url="http://127.0.0.1/api/", json=dict())
            if resp.status_code == 200:
                assert resp.json() == resp_test_empty_json
                check[0] += 1
            elif (resp.status_code == 429):
                assert resp.json() == "too many requests"
                check[1] += 1
        except:
            assert resp.status_code == 502
            check[2] += 1
        lock.release()

    r.delete('127.0.0.1')
    for _ in range(req_num):
        t = threading.Thread(target=empty_json)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    log_lines_num_after_req = sum(1 for line in open(log_file_path))
    if (check[0] == 100):
        assert log_lines_num_after_req == log_lines_num_before_req + 100
    r.delete('127.0.0.1')


def test_empty_body():
    resp_200 = 0
    resp_502 = 0
    check = [resp_200, resp_502]
    th = list()
    log_lines_num_before_req = sum(1 for line in open(log_file_path))

    def empty_body():
        lock.acquire()
        try:
            resp = requests.post(url="http://127.0.0.1/api/")
            if resp.status_code == 200:
                assert resp.json() == resp_test_empty_json
                check[0] += 1
            elif (resp.status_code == 429):
                assert resp.json() == "too many requests"
                check[1] += 1
        except:
            assert resp.status_code == 502
            check[2] += 1
        lock.release()

    r.delete('127.0.0.1')
    for _ in range(req_num):
        t = threading.Thread(target=empty_body)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    log_lines_num_after_req = sum(1 for line in open(log_file_path))
    if (check[0] == req_num):
        assert log_lines_num_after_req == log_lines_num_before_req + 100
    r.delete('127.0.0.1')


def test_get_request():
    try:
        resp = requests.get(url="http://127.0.0.1/api/")
        assert resp.status_code == 405
    except:
        assert resp.status_code == 502
