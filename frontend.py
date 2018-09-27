import backend


url = 'www.tuev-sued.de'
print('Call for info on ' + url)

json_data = backend.backend_get(url)

print('This is the result:')
print(json_data)
