#!/bin/bash

echo "Stopping all docker services ..."

docker stop \
scan_spiderfoot_server_container \
scan_spiderfoot_sidecar_container \
scan_theharvester_container \
analysis_data_statistics_container \
analysis_dummy_container \
master_container \
frontend_container \
nats_container

echo "Done!"
docker ps
