# Backyard


## Todo:
- Deploy on AWS or Heroku
- Migrate to Kubernetes


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

### Backend
Build backend image:
```bash
docker build -t backend_image backend
docker run -d -it --volumes-from storage_container -p 5000:5000 --rm --name backend_container backend_image
```
Check it on http://localhost:5000/


### Frontend
Build frontend:
```bash
docker build -t webapp_image frontend
docker run -d -it -p 8080:8080 --rm --name frontend_container --link backend_container:backend webapp_image
# Peek inside
docker run -it --rm  --name frontend_container --link backend_container:backend webapp_image bash
env  # see available environmental variables, amongst others the backend info
ping backend  # ping [IP_ADDRESS]
curl --data "url=www.bash.com" 172.17.0.2:5000/request/ # test backend
```
Use it on http://localhost:8080/

Check networking on docker with `docker network inspect bridge`



### Clean up
Remove all containers and their associated volumes:
```bash
docker rm -v $(docker ps -qa)
```


## Execution
Call backend directly from script:
```bash
python frontend.py www.hello.com
```
