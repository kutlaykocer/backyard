#!/bin/sh

echo "Stopping all docker services ..."

docker stop \
theharvester_container \
data_statistics_container \
dummy_analysis_container \
master_container \
frontend_container

echo "Done!"
docker ps
