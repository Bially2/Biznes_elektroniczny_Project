.PHONY: help up down restart logs status clean rebuild dump restore dump-backend dump-ui restore-backend restore-ui

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
	@echo "  make dump-backend - Zrób backup backendu do dump-backend.sql"
	@echo "  make dump-ui    - Zrób backup UI do dump-ui.sql"
	@echo "  make restore-backend - Przywróć backend z dump-backend.sql"
	@echo "  make restore-ui - Przywróć UI z dump-ui.sql"

up:
	@echo "Uruchamianie PrestaShop..."
	@cd prestashop && docker compose up -d
	@echo "Nadawanie uprawnień katalogom PrestaShop..."
	@chmod 777 prestashop/
	@cd prestashop && docker exec -it prestashop bash -c "chmod -R 777 /var/www/html/var && chmod -R 777 /var/www/html/modules && chmod -R 777 /var/www/html/img && chmod -R 777 /var/www/html/translations && chmod -R 777 /var/www/html/download && chmod -R 777 /var/www/html/themes"
	@cd prestashop && docker restart prestashop
	@echo "PrestaShop dostępny na: https://localhost:8443/"
	@echo "PrestaShop Admin dostępny na: https://localhost:8443/admin-dev"
	@echo "MailHog dostępny na: http://localhost:8025/"
	@echo "Login i hasło do admina : demo@prestashop.com / prestashop_demo"


down:
	@echo "Zatrzymywanie kontenerów..."
	@cd prestashop && docker compose down


restart:
	@echo "Restartowanie kontenerów..."
	@cd prestashop && docker compose restart


logs:
	@cd prestashop && docker compose logs -f


status:
	@cd prestashop && docker compose ps


clean:
	@echo "UWAGA: To usunie wszystkie dane!"
	@read -p "Czy na pewno chcesz kontynuować? [y/N] " confirm && [ "$$confirm" = "y" ]
	cd prestashop && docker compose down -v
	@echo "Wyczyszczono wszystkie kontenery i volumes"


rebuild:
	@echo "Przebudowywanie kontenerów..."
	@cd prestashop && docker compose down -v
	@cd prestashop && docker compose up -d --build
	@echo "PrestaShop dostępny na: http://localhost:8080"


dump:
	@echo "Tworzenie pełnego backupu bazy danych..."
	docker compose -f prestashop/docker-compose.yml exec -T db mysqldump -u root -proot prestashop > dump.sql
	@echo "Pełny backup zapisany do dump.sql"


dump-backend:
	@echo "Tworzenie backupu BACKEND (przewoźnicy, moduły, maile)..."
	docker compose -f prestashop/docker-compose.yml exec -T db \
	mysqldump -u root -proot prestashop \
	ps_carrier \
	ps_carrier_lang \
	ps_mail* \
	ps_order_carrier \
	ps_module \
	ps_module_shop \
	ps_module_carrier \
	ps_configuration \
	> dump-backend.sql
	@echo "Backend zapisany do dump-backend.sql"


dump-ui:
	@echo "Tworzenie backupu UI (theme, hooks, CMS, layout)..."
	docker compose -f prestashop/docker-compose.yml exec -T db \
	mysqldump -u root -proot prestashop \
	ps_theme* \
	ps_hook \
	ps_hook_module \
	ps_layout* \
	ps_cms* \
	ps_cms_lang \
	ps_meta \
	ps_translation \
	ps_smarty_last_flush \
	> dump-ui.sql
	@echo "UI zapisany do dump-ui.sql"


restore:
	@echo "UWAGA: FULL RESTORE – wszystkie dane zostaną usunięte!"
	@read -p "Kontynuować? [y/N] " confirm && [ "$$confirm" = "y" ]
	cd prestashop && docker compose down -v
	cd prestashop && docker compose up -d
	@echo "Czekam aż MySQL się uruchomi..."
	sleep 10
	@if [ ! -f dump.sql ]; then echo " Brak dump.sql!"; exit 1; fi
	@echo "Import pełnego dump.sql..."
	cat dump.sql | docker compose -f prestashop/docker-compose.yml exec -T db mysql -u root -proot prestashop
	@echo "✔ Pełna baza przywrócona."

restore-backend:
	@if [ ! -f dump-backend.sql ]; then echo " Brak dump-backend.sql!"; exit 1; fi
	@echo "Przywracanie tylko BACKEND..."
	cat dump-backend.sql | docker compose -f prestashop/docker-compose.yml exec -T db mysql -u root -proot prestashop
	@echo "✔ Backend przywrócony."

restore-ui:
	@if [ ! -f dump-ui.sql ]; then echo " Brak dump-ui.sql!"; exit 1; fi
	@echo "Przywracanie tylko UI..."
	cat dump-ui.sql | docker compose -f prestashop/docker-compose.yml exec -T db mysql -u root -proot prestashop
	@echo "✔ UI przywrócone."
