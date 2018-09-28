import docker
import sys


# Validate input
url = sys.argv[1] if len(sys.argv) > 1 else 'www.frontend.example.com'
print('Call for info on ' + url)

# Call backend
client = docker.from_env()
json_data = client.containers.run("backend", command=url, remove=True)

# Return result
print('This is the result:')
print(json_data.decode())
