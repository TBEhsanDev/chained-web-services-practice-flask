from flask import Flask, request, json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def ip():
    if hasattr(request.headers, 'X-Real-IP'):
        client_ip = request.headers['X-Real-IP']
    else:
        client_ip = dict()
    if request.data:
        body = request.get_json()
    else:
        body = dict()
    body['client_ip'] = client_ip
    return json.dumps(body)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
