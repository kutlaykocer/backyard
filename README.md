# Backyard

## Todo
- call backend container master from frontend container via HTTP request

## Setup

### Storage
```bash
# Build image
docker build -t storage_image storage
# Create a container whose sole purpose is to persist data
docker create --name storage_container storage_image
```

Peek into the storage volume:
```bash
docker run -it --rm --volumes-from storage_container storage_image bash
```

Remove the container with
```bash
docker rm -v storage_container
```

### Master
Build backend image:
```bash
docker build -t backend_image backend
```

### Frontend
This is still experimental:
```bash
docker build -t webapp_image .
docker run --volumes-from storage_container -p 5000:5000 --rm -it webapp_image
# http://localhost:5000/
```


### Clean up
Remove all containers and their associated volumes:
```bash
docker rm -v $(docker ps -qa)
```


# Execution
Until called from web interface:
```bash
python frontend.py www.hello.com
```
