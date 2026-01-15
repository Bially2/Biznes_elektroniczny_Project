# Skrypty (`src/script`)

Ten folder zawiera pomocnicze skrypty do pracy z klastrem (logowanie, tunel, wdrożenie) oraz do wysyłki plików na klaster.

Jeśli skrypt nie ma praw do uruchomienia:

```sh
chmod +x *.sh
```

---

## `transfer.sh` — wysyłka pliku na klaster przez bastion (ProxyJump)

Skrypt przesyła wskazany plik na klaster (`student-swarm01.maas`) wykorzystując skok przez serwer bastion (`ProxyJump`). W środku ma na stałe ustawione:

- bastion: `172.20.83.101` (użytkownik: `rsww`)
- klaster: `student-swarm01.maas` (użytkownik: `hdoop`)
- docelowy katalog na klastrze: `/opt/storage/actina15-20/block-storage/students/projects/students-swarm-services/BE_192914`

### Użycie

```sh
bash transfer.sh <plik_zrodlowy> <nazwa_docelowa>
```

### Przykłady

Wysyłka `docker-compose.yml` do katalogu projektu na klastrze:

```sh
bash transfer.sh ../docker-compose.yml docker-compose.yml
```

Wysyłka `deploy.sh`:

```sh
bash transfer.sh ./deploy.sh deploy.sh
```

---

## `login.sh` — logowanie na klaster (opcjonalnie start VPN)

Skrypt loguje na klaster przez bastion i przechodzi do katalogu projektu.

### Użycie

```sh
bash login.sh
```

Opcjonalnie uruchomienie VPN przed logowaniem:

```sh
bash login.sh --vpn
```

### Uwagi

- Opcja `--vpn` zakłada istnienie katalogu `/vpn-eti/vpn2023/` oraz plików konfiguracyjnych OpenVPN na Twojej maszynie.
- Skrypt uruchamia `openvpn` z `sudo`.

CERTYFIKAT ETI NALEZY WYPAKOWAC W /vpn-eti/vpn2023/

---

## `tunel.sh` — tunel SSH do wystawionego portu na klastrze (opcjonalnie start VPN)

Skrypt zestawia tunel SSH (port-forward) przez bastion. Jest przydatny, gdy usługa na klastrze jest wystawiona na porcie, a chcesz wejść na nią lokalnie.

W obecnej konfiguracji forwarduje port `19290`.

### Użycie

```sh
bash tunel.sh
```

Opcjonalnie uruchomienie VPN przed zestawieniem tunelu:

```sh
bash tunel.sh --vpn
```

### Jak sprawdzić czy działa

Po uruchomieniu tunelu możesz wchodzić lokalnie na:

- `http://localhost:19290`

---

## `deploy.sh` — wdrożenie stacka Docker Swarm (uruchamiać na klastrze)

Skrypt wdraża stack Dockera na klastrze (Docker Swarm): usuwa poprzedni stack, wdraża nowy z `docker-compose.yml`, a następnie wykonuje konfigurację w kontenerach (m.in. aktualizuje parametry bazy w PrestaShop i aktualizuje domenę w bazie danych na `localhost:<PORT>`).

### Najważniejsze

- `deploy.sh` uruchamiaj na klastrze (po zalogowaniu), na węźle, gdzie masz dostęp do `docker` i uprawnienia do `docker stack`.
- Skrypt zakłada, że w bieżącym katalogu na klastrze znajduje się `docker-compose.yml`.

### Użycie (na klastrze)

```sh
cd /opt/storage/actina15-20/block-storage/students/projects/students-swarm-services/BE_192914
bash deploy.sh
```

### Dostęp do aplikacji

Skrypt wypisuje adres w postaci `http://localhost:19290`. Żeby wejść na ten adres z Twojej maszyny, uruchom tunel:

```sh
bash tunel.sh
```