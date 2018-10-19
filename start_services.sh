#!/bin/sh

echo "Starting all docker services ..."

echo "Start the tools ..."
docker run -d -it -p 5002:5002 --rm --volumes-from storage_container --name theharvester_container theharvester_image

echo "Start the analyses ..."
docker run -d -it -p 5003:5003 --rm --volumes-from storage_container --name data_statistics_container data_statistics_image
docker run -d -it -p 5004:5004 --rm --volumes-from storage_container --name dummy_analysis_container dummy_analysis_image

echo "Start the master ..."
docker run -d -it -p 5000:5000 --rm --volumes-from storage_container --link theharvester_container:theharvester --link data_statistics_container:data_statistics --link dummy_analysis_container:dummy_analysis --name master_container master_image

echo "Start the frontend ..."
docker run -d -it -p 8080:8080 --rm --link master_container:master --name frontend_container frontend_image

echo "Done!"
docker ps
