#!/bin/bash


echo "Building all docker services ..."

echo "Build the storage ..."
docker build -t storage_image storage
docker create --name storage_container storage_image

echo "Build the scans ..."
docker build -t scan_spiderfoot_server_image scans/spiderfoot/download
docker build -t scan_spiderfoot_sidecar_image scans/spiderfoot
docker build -t scan_theharvester_image scans/theharvester

echo "Build the analyses ..."
docker build -t analysis_data_statistics_image analyses/data_statistics
docker build -t analysis_dummy_image analyses/dummy

echo "Build the master ..."
docker build -t master_image master

echo "Build the frontend ..."
docker build -t frontend_image frontend
