import sys

import requests


# Validate input
_id = sys.argv[1] if len(sys.argv) > 1 else 'example'
_url = sys.argv[2] if len(sys.argv) > 2 else 'www.script.frontend.example.com'
print('Run python script to call backend for client ' + _id + ' with url ' + _url + ' ...')

# Call backend
_payload = {'id': _id, 'url': _url, 'domain': 'script.frontend.example.com'}
print('Warning: missing implementation to directly call the analysis')
_req = requests.post('http://localhost:5000/request/', data=_payload)

# Return result
print('This is the result:')
_result = _req.json()

for key in _result:
    print('{}: {}'.format(key, _result[key]))
