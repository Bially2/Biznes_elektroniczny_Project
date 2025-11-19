.PHONY: help up down restart logs status clean rebuild dump restore

help:
	@echo "Dostępne komendy:"
	@echo "  make up        - Uruchom kontenery PrestaShop"
	@echo "  make down      - Zatrzymaj kontenery"
	@echo "  make restart   - Zrestartuj kontenery"
	@echo "  make logs      - Pokaż logi kontenerów"
	@echo "  make status    - Sprawdź status kontenerów"
	@echo "  make clean     - Zatrzymaj i usuń kontenery oraz volumes"
	@echo "  make rebuild   - Przebuduj i uruchom kontenery od nowa"
	@echo "  make dump      - Zrób backup bazy danych do dump.sql"
	@echo "  make restore   - Przywróć bazę z dump.sql (usuwa obecne dane!)"


up:
    @echo "Uruchamianie PrestaShop..."
    cd prestashop && docker compose up -d
    @echo "Nadawanie uprawnień katalogom PrestaShop..."
    cd prestashop && docker exec -it prestashop bash -c "chmod -R 777 /var/www/html/var && chmod -R 777 /var/www/html/modules && chmod -R 777 /var/www/html/img && chmod -R 777 /var/www/html/translations && chmod -R 777 /var/www/html/download && chmod -R 777 /var/www/html/themes"
    cd prestashop && docker restart prestashop
    @echo "PrestaShop dostępny na: https://localhost:8443/"
    @echo "PrestaShop Admin dostępny na: https://localhost:8443/admin-dev"
    @echo "Login i hasło do admina : demo@prestashop.com / prestashop_demo"


down:
	@echo "Zatrzymywanie kontenerów..."
	cd prestashop && docker compose down


restart:
	@echo "Restartowanie kontenerów..."
	cd prestashop && docker compose restart


logs:
	cd prestashop && docker compose logs -f


status:
	cd prestashop && docker compose ps


clean:
	@echo "UWAGA: To usunie wszystkie dane!"
	@read -p "Czy na pewno chcesz kontynuować? [y/N] " confirm && [ "$$confirm" = "y" ]
	cd prestashop && docker compose down -v
	@echo "Wyczyszczono wszystkie kontenery i volumes"


rebuild:
	@echo "Przebudowywanie kontenerów..."
	cd prestashop && docker compose down -v
	cd prestashop && docker compose up -d --build
	@echo "PrestaShop dostępny na: http://localhost:8080"


dump:
	@echo "Tworzenie backupu bazy danych..."
	docker compose -f prestashop/docker-compose.yml exec -T db mysqldump -u root -proot prestashop > dump.sql
	@echo "Backup zapisany do dump.sql"


restore:
	@echo "UWAGA: To usunie obecną bazę danych!"
	@read -p "Czy na pewno chcesz kontynuować? [y/N] " confirm && [ "$$confirm" = "y" ]
	@echo "Przywracanie bazy danych..."
	cd prestashop && docker compose down -v
	cd prestashop && docker compose up -d
	@echo "Baza przywrócona z dump.sql"
