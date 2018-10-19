import sys

import requests


# Validate input
_id = sys.argv[1] if len(sys.argv) > 1 else 'example'
_url = sys.argv[2] if len(sys.argv) > 2 else 'www.microsoft.com'
_domain = _url.split('www.')[-1]
print('Run python script to call scans for client ' + _id +
      ' with url ' + _url + ' and domain ' + _domain + ' ...')

# Call master
_payload = {'id': _id, 'url': _url, 'domain': _domain}
_req = requests.post('http://localhost:5002/', data=_payload)

# Return result
print('This is the result: ')
print(_req)
