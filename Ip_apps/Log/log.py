import datetime
import os.path

import jsonlines
import requests
from flask import Flask, request

from .. import Base_dir

app = Flask(__name__)
log_file_path = os.path.join(Base_dir, 'Log/log.jsonl')


def save_log(body):
    with jsonlines.open(log_file_path, mode='a') as log:
        log.write(body)


@app.route('/', methods=['POST'])
def log():
    headers = request.headers
    if request.data:
        body = request.get_json()
    else:
        body = dict()
    body['time'] = str(datetime.datetime.now())
    save_log(body)
    del body['time']
    try:
        resp = requests.post(url='http://127.0.0.1:8000/', json=body, headers=headers)
        return resp.json()
    except:
        return "bad gataway", 502


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6000)
