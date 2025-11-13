#!/usr/bin/env bash
set -euo pipefail

# Always run from the prestashop directory
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

COMPOSE="docker compose"
SERVICE=mysql
DB_NAME=prestashop
DB_USER=root
DB_PASS=prestashop
DUMP_DIR=./db/init
DUMP_FILE=${DUMP_DIR}/dump.sql

wait_for_mysql() {
  echo "Waiting for MySQL to be ready..."
  for i in {1..60}; do
    if ${COMPOSE} exec -T ${SERVICE} mysqladmin ping -u"${DB_USER}" -p"${DB_PASS}" --silent >/dev/null 2>&1; then
      echo "MySQL is ready."
      return 0
    fi
    sleep 2
  done
  echo "Timed out waiting for MySQL." >&2
  return 1
}

cmd_dump() {
  echo "Ensuring MySQL is up..."
  ${COMPOSE} up -d ${SERVICE}
  wait_for_mysql
  mkdir -p "${DUMP_DIR}"
  echo "Creating ${DUMP_FILE} (database: ${DB_NAME})..."
  ${COMPOSE} exec -T ${SERVICE} mysqldump \
    -u"${DB_USER}" -p"${DB_PASS}" \
    --single-transaction --routines --triggers --events \
    "${DB_NAME}" > "${DUMP_FILE}"
  size=$(ls -lh -- "${DUMP_FILE}" | awk '{print $5, $9}')
  echo "Done: ${size}"
}

cmd_reset_from_dump() {
  if [[ ! -f "${DUMP_FILE}" ]]; then
    echo "${DUMP_FILE} not found. Run: $0 dump" >&2
    exit 1
  fi
  echo "This will DESTROY local MySQL data in ./db/data and re-seed from ${DUMP_FILE}"
  read -r -p "Continue? [y/N] " answer
  case ${answer:-N} in
    [Yy]*) ;;
    *) echo "Aborted."; exit 1;;
  esac
  echo "Stopping containers..."
  ${COMPOSE} down
  echo "Removing data dir ./db/data ..."
  rm -rf ./db/data
  mkdir -p ./db/data
  echo "Starting MySQL (it will import ${DUMP_FILE} on first init)..."
  ${COMPOSE} up -d ${SERVICE}
  wait_for_mysql
  echo "MySQL started. If the DB was large, initial import may have taken some time."
}

cmd_up() {
  ${COMPOSE} up -d
}

cmd_down() {
  ${COMPOSE} down
}

cmd_reset_files() {
  if [[ ! -f "${DUMP_FILE}" ]]; then
    echo "${DUMP_FILE} not found. Run: $0 dump" >&2
    exit 1
  fi
  echo "This will DESTROY local MySQL data in ./db/data and prepare import from ${DUMP_FILE}"
  read -r -p "Continue? [y/N] " answer
  case ${answer:-N} in
    [Yy]*) ;;
    *) echo "Aborted."; exit 1;;
  esac
  echo "Stopping containers..."
  ${COMPOSE} down || true
  echo "Removing data dir ./db/data ..."
  rm -rf ./db/data
  mkdir -p ./db/data
  echo "Prepared. Next steps: run 'docker compose up -d' (or 'make up') when you want to start MySQL and import will occur automatically."
}

case "${1:-}" in
  dump) cmd_dump ;;
  reset-from-dump) cmd_reset_from_dump ;;
  reset-files) cmd_reset_files ;;
  up) cmd_up ;;
  down) cmd_down ;;
  *)
    echo "Usage: $0 {dump|reset-from-dump|reset-files|up|down}" >&2
    exit 2
    ;;
 esac
