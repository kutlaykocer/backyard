# Webapp

## Setup
```bash
docker build -t webapp_image .
docker run --volumes-from storage_container -p 5000:5000 --rm -it webapp_image
# http://localhost:5000/
```

## Todo
- call backend container master from this container via HTTP request
