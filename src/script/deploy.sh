#!/bin/bash

PREFIX="BE_192914"
DB_NAME="BE_192914"
DB_USER="root"
DB_PASS="student"
DB_HOST="admin-mysql_db"
PORT="19290"
COMPOSE_FILE="docker-compose.yml"

echo "Removing old stack: $PREFIX..."
docker stack rm $PREFIX
echo "Waiting 20s for network cleanup..."
sleep 20

echo "Deploying stack $PREFIX..."
docker stack deploy -c $COMPOSE_FILE $PREFIX --with-registry-auth

echo "Waiting for Prestashop service to start..."
PS_NODE=""
for i in {1..30}; do
    PS_NODE=$(docker service ps ${PREFIX}_prestashop --filter "desired-state=running" --format "{{.Node}}" 2>/dev/null | head -n 1)
    [ ! -z "$PS_NODE" ] && break
    echo "Retry $i/30..."
    sleep 5
done

if [ -z "$PS_NODE" ]; then
    echo "Prestashop service not found!"
    exit 1
fi

echo "Prestashop is running on: $PS_NODE"

echo "--------------------------------------"
if [ "$PS_NODE" == "student-swarm01" ]; then
   echo "Use tunnel: ./tunel.sh 1"
elif [ "$PS_NODE" == "student-swarm02" ]; then
   echo "Use tunnel: ./tunel.sh 2"
elif [ "$PS_NODE" == "student-swarm03" ]; then
   echo "Use tunnel: ./tunel.sh 3"
elif [ "$PS_NODE" == "student-swarm04" ]; then
   echo "Use tunnel: ./tunel.sh 4"
else
   echo "Use tunnel for node: $PS_NODE"
fi

echo "Access the shop at https://localhost:$PORT"