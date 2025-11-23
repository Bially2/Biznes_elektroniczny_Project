.PHONY: dump-settings restore-settings

# Katalog backupu
BACKUP_DIR=prestashop-backup
SQL_DIR=$(BACKUP_DIR)/sql
CONFIG_DIR=$(BACKUP_DIR)/config
THEMES_DIR=$(BACKUP_DIR)/themes
MODULES_DIR=$(BACKUP_DIR)/modules

DOCKER_COMPOSE_FILE=../src/prestashop/docker-compose.yml


dump-settings:
	@echo "Tworzenie katalogów backupu..."
	mkdir -p $(SQL_DIR) $(CONFIG_DIR) $(THEMES_DIR) $(MODULES_DIR)
	@echo "Tworzenie pełnego backupu bazy danych..."
	docker compose -f $(DOCKER_COMPOSE_FILE) exec -T db \
	mysqldump -u root -proot prestashop > $(SQL_DIR)/backup-full.sql
	@echo "Backup bazy zapisany w $(SQL_DIR)/backup-full.sql"
	@echo "Kopiowanie plików konfiguracyjnych..."
	cp ../src/prestashop/app/config/parameters.php $(CONFIG_DIR)/
	@echo "Kopiowanie motywów..."
	cp -r ../src/prestashop/themes/* $(THEMES_DIR)/
	@echo "Kopiowanie modułów..."
	cp -r ../src/prestashop/modules/* $(MODULES_DIR)/
	@echo "Backup ustawień sklepu zapisany w $(BACKUP_DIR)"

restore-settings:
	@echo "Przywracanie dumpa ustawień..."
	cat $(SQL_DIR)/backup-full.sql | docker compose -f $(DOCKER_COMPOSE_FILE) exec -T db \
	mysql -u root -proot prestashop
	@echo "Przywracanie plików konfiguracyjnych..."
	cp $(CONFIG_DIR)/parameters.php ../src/prestashop/app/config/
	@echo "Przywracanie motywów..."
	cp -r $(THEMES_DIR)/* ../src/prestashop/themes/
	@echo "Przywracanie modułów..."
	cp -r $(MODULES_DIR)/* ../src/prestashop/modules/
	@echo "Czyszczenie cache PrestaShop..."
	docker compose -f $(DOCKER_COMPOSE_FILE) exec prestashop bash -c "rm -rf var/cache/*"
	@echo "Restart kontenera PrestaShop..."
	docker compose -f $(DOCKER_COMPOSE_FILE) restart prestashop
	@echo "Przywracanie ustawień zakończone"
