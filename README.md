# Jak uruchomić PrestaShop (Docker)

## Start
```bash
cd prestashop
./up.sh   
```

Front (HTTPS tylko):
- https://localhost/

Panel administracyjny:
- https://localhost/admin-dev

Domyślne loginy (jeśli nie zmieniono podczas instalacji):
- E-mail: demo@prestashop.com
- Hasło: prestashop_demo


## USUWANIE COOCKIES 
```bash
docker exec -it prestashop bash -lc "rm -rf var/cache/*"
```
## Zatrzymywanie / usuwanie
- Zatrzymaj: `docker compose stop`
- Usuń kontenery (DB zostaje): `docker compose down`
- Usuń kontenery i DB (reset): `docker compose down -v`


## Dostęp do kontenerów i logów
- Lista usług: `docker compose ps`
- Logi aplikacji: `docker logs -f prestashop`
- Shell www: `docker exec -it prestashop bash`

## MySQL
- Wejście do MySQL:
```bash
docker exec -it prestashop-mysql mysql -uroot -pprestashop
USE prestashop;
```
- Backup: `docker exec -it prestashop-mysql mysqldump -uroot -pprestashop prestashop > backup.sql`
- Restore: `docker exec -i prestashop-mysql mysql -uroot -pprestashop prestashop < backup.sql`


## Instalacja bez danych demo
- Jeśli masz już DB, zrób reset:
```bash
docker exec -it prestashop-mysql mysql -uroot -pprestashop -e "DROP DATABASE IF EXISTS prestashop; CREATE DATABASE prestashop CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
docker exec -it prestashop bash -lc "rm -f config/settings.inc.php app/config/parameters.php"
docker compose restart prestashop

docker exec -it prestashop bash -lc "php install-dev/index_cli.php --domain=localhost --db_server=mysql --db_name=prestashop --db_user=root --db_password=prestashop --language=pl --country=pl --fixtures=0 --firstname=Admin --lastname=Admin --password=prestashop_demo --email=demo@prestashop.com"
docker exec -it prestashop bash -lc "rm -rf install-dev && rm -rf var/cache/*"
```

## Import produktów (1000+)
- BO: Międzynarodowy > Import > Produkty. Załaduj CSV ze sklepu źródłowego (nazwy, opisy, ceny, VAT, zdjęcia URL/plik).
- Ustaw magazyn: maks. 10 szt./wariant (Import: Kolumna Quantity ≤ 10). Część produktów: Quantity = 0 (niedostępne).
- Kategorie: utwórz min. 4 kategorie i ≥ 2 podkategorie każda (żadna niepusta). CSV Category i Category tree lub przez BO.


## Płatności (PL)
- Włącz: Przelew bankowy (ps_wirepayment), Płatność przy odbiorze (COD).
- Wyłącz: Czeki, metody spoza PL.
- Konfiguracja przelewu: dane rachunku, tytuł płatności. 

## Przewoźnicy
- Dodaj 2 przewoźników.
- Darmowa dostawa > 2000 zł: Koszty wysyłki > Reguły przewozów lub w ustawieniach przewoźników (Reguła ceny: od 2000 zł = 0).
- Produkty > 50 kg: dla wag > 50 kg brak zakresu wagi u przewoźnika (lub reguła wykluczenia).
- Różne opłaty: zdefiniuj różne ceny w zależności od wagi/kwoty.



## PL interfejs i brak domyślnych treści
- Międzynarodowy > Lokalizacja: zaimportuj “Poland”, ustaw Domyślny język: Polski, “Set language from browser”: Nie.
- Usuń/wyłącz demo moduły/banery (np. ps_imageslider) i treści demo (pscleaner lub ręcznie).