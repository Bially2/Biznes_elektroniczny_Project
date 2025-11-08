# Jak uruchomić PrestaShop (Docker)

## Start
```bash
cd prestashop
docker compose up -d
```
Aplikacja (front):  
http://localhost:8001

Panel administracyjny:  
http://localhost:8001/admin-dev

Domyślne dane logowania (jeśli nie zmienione podczas instalacji):
- E-mail: demo@prestashop.com
- Hasło: prestashop_demo

Jeżeli instalator nie uruchomił się automatycznie, wejdź na front i wykonaj instalację w przeglądarce.

## Zatrzymywanie / usuwanie kontenerów
- Zatrzymaj:
```bash
docker compose stop
```
- Usuń kontenery (dane bazy zostają dzięki wolumenowi db-data):
```bash
docker compose down
```
- Usuń kontenery i dane bazy (reset środowiska):
```bash
docker compose down -v
```

## Dostęp do kontenerów i logów
- Lista usług:
```bash
docker compose ps
```
- Logi aplikacji:
```bash
docker logs -f prestashop
```
- Shell w kontenerze aplikacji:
```bash
docker exec -it prestashop bash
```

## MySQL (wejście do bazy z kontenera)
- Klient MySQL:
```bash
docker exec -it prestashop-mysql mysql -u root -p
USE prestashop;
```
haslo - prestashop

- Przykład zapytania:
```bash
SELECT * FROM ps_product;
```
- Backup:
```bash
docker exec -it prestashop-mysql mysqldump -uroot -pprestashop prestashop > backup.sql
```
- Restore:
```bash
docker exec -i prestashop-mysql mysql -uroot -pprestashop prestashop < backup.sql
```

(Przypomnienie: wolumen db-data utrzymuje dane po stop/down; kasuje je tylko `docker compose down -v`.)

## Najczęstsze problemy
- Przekierowania na inny port/domenę: zaktualizuj domenę w DB
```bash
docker exec -it prestashop-mysql mysql -uroot -pprestashop -e "USE prestashop; UPDATE ps_shop_url SET domain='localhost:8001', domain_ssl='localhost:8001' WHERE id_shop_url=1; DELETE FROM ps_configuration WHERE name IN ('PS_SHOP_DOMAIN','PS_SHOP_DOMAIN_SSL');"
```
- Błędy cache: wyczyść cache w kontenerze
```bash
docker exec -it prestashop bash -lc "rm -rf var/cache/*"
```
- Ponowna instalacja (reset):
  1) `docker compose down -v`  
  2) Upewnij się, że katalog `install-dev` istnieje  
  3) Usuń pliki konfiguracyjne jeśli są:  
     `rm -f config/settings.inc.php app/config/parameters.php`  
  4) `docker compose up -d` i przejdź instalator w przeglądarce