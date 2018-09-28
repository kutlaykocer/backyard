# Backyard

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
Initiated by the frontend script. Build backend image by hand:
```bash
docker build -t --volumes-from storage_container backend_image backend
```

### Clean up
Remove all containers and their associated volumes:
```bash
docker rm -v $(docker ps -qa)
```


# Execution
python frontend.py www.hello.com
