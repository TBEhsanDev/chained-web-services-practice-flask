import requests

json_data = {
    'student': {'age': 32, 'name': 'ali', 'grades': [14, 16]}
}
client_ip = {'client_ip': '127.0.0.1'}
resp_test_with_json = json_data | client_ip
resp_test_empty_json = client_ip
resp_test_empty_body = client_ip


def test_with_json():
    try:
        resp = requests.post(url="http://127.0.0.1/api/", json=json_data)
        assert resp.status_code == 200
        assert resp.json() == resp_test_with_json
    except:
        assert resp.status_code == 502


def test_empty_json():
    try:
        resp = requests.post(url="http://127.0.0.1/api/", json=dict())
        assert resp.status_code == 200
        assert resp.json() == resp_test_empty_json
    except:
        assert resp.status_code == 502


def test_empty_body():
    try:
        resp = requests.post(url="http://127.0.0.1/api/")
        assert resp.status_code == 200
        assert resp.json() == resp_test_empty_body
    except:
        assert resp.status_code == 502


def test_get_request():
    try:
        resp = requests.get(url="http://127.0.0.1/api/")
        assert resp.status_code == 405
    except:
        assert resp.status_code == 502
