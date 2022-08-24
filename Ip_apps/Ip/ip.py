import json

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def ip():
    client_ip = request.headers.get('X-Real-IP')
    if request.data:
        body = request.get_json()
    else:
        body = dict()
    if client_ip:
        body['client_ip'] = client_ip
    return json.dumps(body)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
