#!/bin/bash


if [ -z "$1" ]; then
  echo "No argument supplied! Choose your service to restart!"
  docker ps
  exit
fi


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

start_cmds=()
containers=""
for service; do
   echo "Rebuilding service $service ..."
   containers="${containers}${service}_container "
   # get start command from start script
   cmd=$(grep "${service}_image" "$DIR/start_services.sh")
   #store in array to use later
   start_cmds+=("$cmd")
   # build image
   docker build -t "$service"_image "$service"
done

echo "Stopping containers $containers"
docker stop $containers

echo "Restarting containers ..."
for cmd in "${start_cmds[@]}"; do
  $cmd
done
