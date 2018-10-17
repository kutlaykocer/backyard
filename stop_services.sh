#!/bin/sh

echo "Stopping all docker services ..."

docker stop \
theharvester_container \
data_statistics_container \
backend_container \
frontend_container

echo "Done!"
docker ps
