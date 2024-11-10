#!/bin/bash

SUDO=""

if [ $(test -r /var/run/docker.sock; echo "$?") -ne 0 ]; then
    SUDO="sudo"
fi

$SUDO docker rm $($SUDO docker ps -aq) 2>/dev/null
$SUDO docker network rm $($SUDO docker network ls -q) 2>/dev/null
$SUDO docker volume rm $($SUDO docker volume ls -q) 2>/dev/null

PROJECT_NAME=$(basename "$PWD" | tr '[:upper:]' '[:lower:]')

$SUDO docker rmi $($SUDO docker images --format "{{.Repository}}:{{.Tag}}" | grep "^${PROJECT_NAME}-") 2>/dev/null

sudo rm -rf ./data

echo "Project cleared"