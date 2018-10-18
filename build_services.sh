#!/bin/sh

echo "Building all docker services ..."

echo "Build the storage ..."
docker build -t storage_image storage
docker create --name storage_container storage_image

echo "Build the tools ..."
docker build -t theharvester_image tools/theharvester

echo "Build the analyses ..."
docker build -t data_statistics_image analyses/data_statistics
docker build -t dummy_analysis_image analyses/dummy_analysis

echo "Build the backend ..."
docker build -t backend_image backend

echo "Build the frontend ..."
docker build -t webapp_image frontend
