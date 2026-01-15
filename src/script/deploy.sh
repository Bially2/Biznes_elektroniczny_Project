#!/bin/bash


PREFIX="BE_192914"
DB_NAME="BE_192914"
DB_USER="root"
DB_PASS="student"
DB_HOST="admin-mysql_db" 
PORT="19290"
COMPOSE_FILE="docker-compose.yml"

echo "Usuwanie starego stacka: $PREFIX..."
docker stack rm $PREFIX
echo "Czekam 20s na zwolnienie zasobów sieciowych..."
sleep 20

echo "Wdrażanie stacka $PREFIX..."
docker stack deploy -c $COMPOSE_FILE $PREFIX --with-registry-auth

echo "Szukanie kontenera Prestashop..."
PS_CONTAINER=""

for i in {1..204}; do
    
    PS_CONTAINER=$(docker ps -q -f name=${PREFIX}_prestashop)
    [ ! -z "$PS_CONTAINER" ] && break
    echo "Próba $i/204: Kontener jeszcze nie wstał..."
    sleep 5
done

if [ -z "$PS_CONTAINER" ]; then
    echo "BŁĄD: Kontener Prestashop nie uruchomił się w wyznaczonym czasie."
    exit 1
fi

echo "Konfiguracja plików wewnątrz kontenera ($PS_CONTAINER)..."
docker exec -u 0 -i $PS_CONTAINER bash <<EOF
# Naprawa uprawnień do folderów cache i logów
chown -R www-data:www-data /var/www/html/var
chmod -R 775 /var/www/html/var

# Automatyczna podmiana danych bazy w pliku parameters.php
FILE="/var/www/html/app/config/parameters.php"
if [ -f "\$FILE" ]; then
    echo "Aktualizacja pliku parameters.php..."
    sed -i "s/'database_host' => '.*'/'database_host' => '$DB_HOST'/" \$FILE
    sed -i "s/'database_name' => '.*'/'database_name' => '$DB_NAME'/" \$FILE
    sed -i "s/'database_user' => '.*'/'database_user' => '$DB_USER'/" \$FILE
    sed -i "s/'database_password' => '.*'/'database_password' => '$DB_PASS'/" \$FILE
    sed -i "s/'database_port' => '.*'/'database_port' => '3306'/" \$FILE
fi
# Czyszczenie cache, żeby Presta zauważyła zmiany
rm -rf /var/www/html/var/cache/*
EOF

echo "Aktualizacja adresów URL sklepu w bazie danych..."

DB_CONTAINER=$(docker ps -q -f name=admin-mysql_db)

if [ ! -z "$DB_CONTAINER" ]; then
    docker exec -i $DB_CONTAINER mysql -u$DB_USER -p$DB_PASS $DB_NAME <<EOF
UPDATE ps_configuration SET value='localhost:$PORT' WHERE name IN ('PS_SHOP_DOMAIN', 'PS_SHOP_DOMAIN_SSL');
UPDATE ps_shop_url SET domain='localhost:$PORT', domain_ssl='localhost:$PORT';
EOF
    echo "Adresy URL w bazie zaktualizowane na localhost:$PORT"
else
    echo "OSTRZEŻENIE: Nie znaleziono kontenera admin-mysql_db na tym węźle. Skrypt nie mógł zaktualizować tabeli ps_shop_url."
fi

echo "-------------------------------------------------------"
echo "GOTOWE! Sklep powinien być dostępny pod adresem:"
echo "http://localhost:$PORT"
echo "Pamiętaj o aktywnym tunelu SSH!"
