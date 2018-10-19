#!/bin/sh

echo "Starting all docker services ..."

echo "Start the scans ..."
docker run -d -it -p 5002:5002 --rm --volumes-from storage_container --name scan_theharvester_container scan_theharvester_image

echo "Start the analyses ..."
docker run -d -it -p 5003:5003 --rm --volumes-from storage_container --name analysis_data_statistics_container analysis_data_statistics_image
docker run -d -it -p 5004:5004 --rm --volumes-from storage_container --name analysis_dummy_container analysis_dummy_image

echo "Start the master ..."
docker run -d -it -p 5000:5000 --rm --volumes-from storage_container --link scan_theharvester_container:scan_theharvester --link analysis_data_statistics_container:analysis_data_statistics --link analysis_dummy_container:analysis_dummy --name master_container master_image

echo "Start the frontend ..."
docker run -d -it -p 8080:8080 --rm --link master_container:master --name frontend_container frontend_image

echo "Done!"
docker ps
