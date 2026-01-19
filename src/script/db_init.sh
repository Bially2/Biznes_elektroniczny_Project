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

echo "Waiting for services to start..."
sleep 30

echo "Detecting node for Prestashop..."
PS_NODE=$(docker service ps ${PREFIX}_prestashop --filter "desired-state=running" --format "{{.Node}}" | head -n 1)

if [ -z "$PS_NODE" ]; then
    echo "Prestashop service not found!"
    exit 1
fi

echo "Prestashop is running on: $PS_NODE"

echo "Configuring Prestashop on $PS_NODE..."
ssh $PS_NODE "
    PS_CONTAINER=\$(docker ps -q -f name=${PREFIX}_prestashop 2>/dev/null || sudo docker ps -q -f name=${PREFIX}_prestashop)
    if [ ! -z \"\$PS_CONTAINER\" ]; then
        (docker exec -u 0 -i \$PS_CONTAINER bash 2>/dev/null || sudo docker exec -u 0 -i \$PS_CONTAINER bash) <<'EOFPS'
chown -R www-data:www-data /var/www/html/var
chmod -R 775 /var/www/html/var
rm -rf /var/www/html/var/cache/*
EOFPS
        echo 'Prestashop configured'
    fi
"

echo "Updating shop URLs in the database..."
DB_CONTAINER=$(docker ps -q -f name=admin-mysql_db)
docker exec -i $DB_CONTAINER mysql -u$DB_USER -p$DB_PASS $DB_NAME <<EOF
UPDATE ps_configuration SET value='localhost:$PORT' WHERE name IN ('PS_SHOP_DOMAIN', 'PS_SHOP_DOMAIN_SSL');
UPDATE ps_shop_url SET domain='localhost:$PORT', domain_ssl='localhost:$PORT';
EOF

echo "Access the shop at https://localhost:$PORT"
