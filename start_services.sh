#!/bin/sh

echo "Starting all docker services ..."

echo "Start the tools ..."
docker run -d -it -p 5002:5002 --rm --volumes-from storage_container --name theharvester_container theharvester_image

echo "Start the analyses ..."
docker run -d -it -p 5003:5003 --rm --volumes-from storage_container --name data_statistics_container data_statistics_image

echo "Start the backend ..."
docker run -d -it -p 5000:5000 --rm --volumes-from storage_container --link theharvester_container:theharvester --link data_statistics_container:data_statistics --name backend_container backend_image

echo "Start the frontend ..."
docker run -d -it -p 8080:8080 --rm --link backend_container:backend --name frontend_container webapp_image

echo "Done!"
docker ps
