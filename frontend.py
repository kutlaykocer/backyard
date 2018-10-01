import sys

import requests


# Validate input
url = sys.argv[1] if len(sys.argv) > 1 else 'www.frontend.example.com'
print('Run python script to call backend for ' + url + ' ...')

# payload = {'url': url}
print('Warning: missing implementation to directly call the analysis')
r = requests.get('http://localhost:5000/')

# Return result
print('This is the result:')
print(r.text)
