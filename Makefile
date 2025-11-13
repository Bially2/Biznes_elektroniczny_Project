.PHONY: up down dump reset reset-start reset-from-dump install composer assets

PS_DIR := prestashop
SCRIPT := $(PS_DIR)/scripts/db-tools.sh
COMPOSE := docker compose


up:
	cd $(PS_DIR) && ./scripts/up.sh

down:
	cd $(PS_DIR) && $(COMPOSE) down

dump:
	cd $(PS_DIR) && ./scripts/db-tools.sh dump

reset:
	cd $(PS_DIR) && ./scripts/db-tools.sh reset-files

install: composer assets

composer:
	cd $(PS_DIR) && composer install

assets:
	cd $(PS_DIR) && ./tools/assets/build.sh
