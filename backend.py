import json


def backend_get(url):
    with open('result.json') as f:
        json_data = json.load(f)
    return json_data
