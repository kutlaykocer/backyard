#!/bin/sh

echo "Stopping all docker services ..."

docker stop \
scan_theharvester_container \
analysis_data_statistics_container \
analysis_dummy_container \
master_container \
frontend_container

echo "Done!"
docker ps
