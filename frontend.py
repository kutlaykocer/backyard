import docker
import sys


# Validate input
url = sys.argv[1] if len(sys.argv) > 1 else 'www.frontent.example.com'
print('Call for info on ' + url)

# Call backend
client = docker.from_env()
json_data = client.containers.run("backend", url)

# Return result
print('This is the result:')
print(json_data)
