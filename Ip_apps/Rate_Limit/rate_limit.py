import json
import threading

import redis
import requests
from flask import Flask, request

app = Flask(__name__)
req_num = 100
lock = threading.Lock()
r = redis.Redis()


@app.route('/', methods=['POST'])
def rate_limit():
    client_ip = request.headers.get('X-Real-IP')
    ip = str(client_ip)
    lock.acquire()
    if not r.exists(ip):
        r.set(ip, req_num)
    print(r.get(ip))
    if r.get(ip) == b'0':
        lock.release()
        return json.dumps('too many requests'), 429
    r.decrby(ip,1)
    lock.release()
    headers = request.headers
    if request.data:
        body = request.get_json()
    else:
        body = dict()
    try:
        resp = requests.post(url='http://127.0.0.1:6000/', json=body, headers=headers)
        return resp.json()
    except:
        return json.dumps("bad gateway"), 502


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
