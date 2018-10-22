#!/bin/sh


if [ -z "$1" ]; then
  echo "No argument supplied! Choose your service to restart!"
  docker ps
  exit
fi

containers=""
for service; do
   echo "Rebuilding service $service ..."
   containers="${containers}${service}_container "
   docker build -t "$service"_image "$service"
done

echo "Restarting containers $containers"
docker restart $containers
