import sys

import requests


# Validate input
url = sys.argv[1] if len(sys.argv) > 1 else 'www.frontend.script.example.com'
print('Run python script to call backend for ' + url + ' ...')


payload = {'url': url}
print('Warning: missing implementation to directly call the analysis')
r = requests.post('http://localhost:5000/request/', data=payload)

# Return result
print('This is the result:')
result = r.json()

for key in result:
    print('{}: {}'.format(key, result[key]))
