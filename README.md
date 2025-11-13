# Jak uruchomić PrestaShop (Docker)

Wersja sklepu: 1.7.8.11

## Szybki start (z katalogu repozytorium)
```bash
make up
```
Po starcie:
- Front (HTTPS): https://localhost/
- Panel admina: https://localhost/admin-dev
- Domyślne loginy (jeśli nie zmieniono podczas instalacji):
	- E-mail: demo@prestashop.com
	- Hasło: prestashop_demo

Uwaga: pierwszy start instaluje sklep automatycznie. Jeśli w `prestashop/db/init/` jest plik `dump.sql`, MySQL zaimportuje go przy pierwszym uruchomieniu pustej bazy.

## Przydatne komendy (z katalogu repozytorium)
- `make up`: uruchamia kontenery (z generacją certyfikatu dla HTTPS).
- `make down`: zatrzymuje i usuwa kontenery (dane DB zostają).
- `make dump`: eksportuje aktualną bazę do `prestashop/db/init/dump.sql`.
- `make reset`: czyści lokalne dane i przygotowuje import; wykonaj potem make up.
- `make install`: `composer install` + budowa assetów.
- `make composer`: same zależności PHP.
- `make assets`: budowa assetów (frontend).

## Kontenery, logi i shell
Uwaga: poniższe komendy `docker compose ...` uruchamiaj z katalogu `prestashop/`.
- Lista usług: `docker compose ps`
- Logi aplikacji (Nginx): `docker compose logs -f nginx`
- Logi PHP (kontener `prestashop`): `docker logs -f prestashop`
- Shell w kontenerze www: `docker exec -it prestashop bash`

## MySQL: dostęp, backup i restore
- Wejście do MySQL:
```bash
docker exec -it prestashop-mysql mysql -uroot -pprestashop
USE prestashop;
```
- Backup ręczny: `docker exec -it prestashop-mysql mysqldump -uroot -pprestashop prestashop > backup.sql`
- Restore ręczny: `docker exec -i prestashop-mysql mysql -uroot -pprestashop prestashop < backup.sql`


## Czyszczenie cache aplikacji
```bash
docker exec -it prestashop bash -lc "rm -rf var/cache/*"
```

## Instalacja bez danych demo (zaawansowane, opcjonalne)
```bash
docker exec -it prestashop-mysql mysql -uroot -pprestashop -e "DROP DATABASE IF EXISTS prestashop; CREATE DATABASE prestashop CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
docker exec -it prestashop bash -lc "rm -f config/settings.inc.php app/config/parameters.php"
docker compose -f prestashop/docker-compose.yml restart prestashop

docker exec -it prestashop bash -lc "php install-dev/index_cli.php --domain=localhost --db_server=mysql --db_name=prestashop --db_user=root --db_password=prestashop --language=pl --country=pl --fixtures=0 --firstname=Admin --lastname=Admin --password=prestashop_demo --email=demo@prestashop.com"
docker exec -it prestashop bash -lc "rm -rf install-dev && rm -rf var/cache/*"
```
