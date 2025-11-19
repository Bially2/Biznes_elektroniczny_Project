# Biznes_elektroniczny_Project

# Informacje ogólne
Ten projekt jest zadaniem z przedmiotu Biznes Elektroniczny na Politechnice Gdańskiej. Zadanie polega na wykonaniu duplikatu wybranej strony internetowej. Stroną, którą wybraliśmy, jest: https://sklep.kfd.pl

# Stack technologiczny
Technologie użyte w projekcie:

-Prestashop v1.7.8

-MySQL DB v5.7

-Selenium

-Docker

# Konfiguracja i zarządzanie
Aby poprawnie uruchomić projekt, należy pobrać i załadować do bazy danych kategorie, produkty oraz zdjęcia. Dodatkowo należy zastosować politykę podatkową. Szczegóły znajdują się w folderze (tutaj folder scrappa).

Za każdym razem, gdy kontenery są uruchamiane, baza danych jest przywracana z pliku dump.sql. Stan bazy danych można zapisać, będąc w katalogu src, używając polecenia:
```bash
make dump
```

# Uruchomienie
Aby uruchomić projekt, będąc w katalogu src, wpisz:
```bash
make run
```
Następnie można uzyskać dostęp do strony pod adresem: https://localhost:8443
Aby zatrzymać i usunąć wszystkie kontenery, wpisz:
```bash
make down
```