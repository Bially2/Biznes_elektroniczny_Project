#!/usr/bin/env bash
set -euo pipefail

COMPOSE_BIN="docker compose"
if ! docker compose version >/dev/null 2>&1; then
  COMPOSE_BIN="docker-compose"
fi

echo "[info] Ensuring SSL cert volume..."
docker volume create prestashop_nginx-certs >/dev/null 2>&1 || true

docker run --rm -v prestashop_nginx-certs:/data alpine:3 sh -ec '
  if [ ! -f /data/localhost.crt ] || [ ! -f /data/localhost.key ]; then
    echo "Generating self-signed certificate (first run)..." >&2
    apk add --no-cache openssl >/dev/null
    openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
      -keyout /data/localhost.key \
      -out /data/localhost.crt \
      -subj "/CN=localhost" >/dev/null 2>&1
    echo "Certificate created." >&2
  else
    echo "Certificate already present; skipping generation." >&2
  fi'

echo "[info] Starting containers..."
$COMPOSE_BIN up -d

echo "[info] Containers running. Useful URLs:"
echo "  Front:  https://localhost/"
echo "  Admin:  https://localhost/admin-dev (default: demo@prestashop.com / prestashop_demo)"
echo "[note] If browser warns about certificate, accept the self-signed cert."
