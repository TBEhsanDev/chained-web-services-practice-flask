import json
import threading
import time

import pymongo
import requests

lock = threading.Lock()
data = {
    'student': {'age': 32, 'name': 'ali', 'grades': [14, 18]}
}
client_ip = {'client_ip': '127.0.0.1'}
resp_test_with_json = data | client_ip
resp_test_empty_json = client_ip
resp_test_empty_body = client_ip
req_num = 1


def check_logs_content(start, end):
    with open('../Log/log.jsonl', mode='r') as log:
        for i in range(start + 1, end):
            line = log.readlines()[i]
            line_dict = json.loads(line)
            del line_dict['time']
            assert line_dict == data


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
    log_lines_num_before_req = sum(1 for line in open('../Log/log.jsonl'))
    resp_200 = 0
    resp_502 = 0
    check = [resp_200, resp_502]
    th = list()

    def with_json():
        lock.acquire()
        try:
            resp = requests.post(url="http://127.0.0.1/api/", json=data)
            assert resp.status_code == 200
            assert resp.json() == resp_test_with_json
            check[0] += 1
        except:
            assert resp.status_code == 502
            check[1] += 1
        lock.release()

    for _ in range(req_num):
        t = threading.Thread(target=with_json)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    log_lines_num_after_req = sum(1 for line in open('../Log/log.jsonl'))
    if (check[0] == req_num) and (log_lines_num_after_req == log_lines_num_before_req + req_num):
        check_logs_content(log_lines_num_before_req, log_lines_num_after_req)
        time.sleep(5)
        check_mongodb(col, data, log_lines_num_in_db_before_req)


def test_empty_json():
    resp_200 = 0
    resp_502 = 0
    check = [resp_200, resp_502]
    th = list()
    log_lines_num_before_req = sum(1 for line in open('../Log/log.jsonl'))

    def empty_json():
        lock.acquire()
        try:
            resp = requests.post(url="http://127.0.0.1/api/", json=dict())
            assert resp.status_code == 200
            assert resp.json() == resp_test_empty_json
            check[0] += 1
        except:
            assert resp.status_code == 502
            check[1] += 1
        lock.release()

    for _ in range(req_num):
        t = threading.Thread(target=empty_json)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    log_lines_num_after_req = sum(1 for line in open('../Log/log.jsonl'))
    if (check[0] == req_num):
        assert log_lines_num_after_req == log_lines_num_before_req + req_num


def test_empty_body():
    resp_200 = 0
    resp_502 = 0
    check = [resp_200, resp_502]
    th = list()
    log_lines_num_before_req = sum(1 for line in open('../Log/log.jsonl'))

    def empty_body():
        lock.acquire()
        try:
            resp = requests.post(url="http://127.0.0.1/api/")
            assert resp.status_code == 200
            assert resp.json() == resp_test_empty_json
            check[0] += 1
        except:
            assert resp.status_code == 502
            check[1] += 1
        lock.release()

    for _ in range(req_num):
        t = threading.Thread(target=empty_body)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    log_lines_num_after_req = sum(1 for line in open('../Log/log.jsonl'))
    if (check[0] == req_num):
        assert log_lines_num_after_req == log_lines_num_before_req + req_num


def test_get_request():
    try:
        resp = requests.get(url="http://127.0.0.1/api/")
        assert resp.status_code == 405
    except:
        assert resp.status_code == 502
