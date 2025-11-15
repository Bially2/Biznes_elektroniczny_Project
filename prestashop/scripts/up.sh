#!/usr/bin/env bash
set -euo pipefail

COMPOSE_BIN="docker compose"
if ! docker compose version >/dev/null 2>&1; then
  COMPOSE_BIN="docker-compose"
fi

<<<<<<< HEAD
# Generate self-signed certs into apache-conf/ssl (host directory mounted into container)
SSL_DIR="apache-conf/ssl"
mkdir -p "$SSL_DIR"
if [ ! -f "$SSL_DIR/localhost.crt" ] || [ ! -f "$SSL_DIR/localhost.key" ]; then
  echo "[info] Generating self-signed certificate into $SSL_DIR ..."
  docker run --rm -v "$PWD/$SSL_DIR":/data alpine:3 sh -ec '
=======
echo "[info] Ensuring SSL cert volume..."
docker volume create prestashop_nginx-certs >/dev/null 2>&1 || true

docker run --rm -v prestashop_nginx-certs:/data alpine:3 sh -ec '
  if [ ! -f /data/localhost.crt ] || [ ! -f /data/localhost.key ]; then
    echo "Generating self-signed certificate (first run)..." >&2
>>>>>>> fdba62e4347ae382c8190f7f402d1ade3542b675
    apk add --no-cache openssl >/dev/null
    openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
      -keyout /data/localhost.key \
      -out /data/localhost.crt \
      -subj "/CN=localhost" >/dev/null 2>&1
<<<<<<< HEAD
  '
  echo "[info] Certificate created."
else
  echo "[info] Certificate already exists; skipping generation."
fi
=======
    echo "Certificate created." >&2
  else
    echo "Certificate already present; skipping generation." >&2
  fi'
>>>>>>> fdba62e4347ae382c8190f7f402d1ade3542b675

echo "[info] Starting containers..."
$COMPOSE_BIN up -d

echo "[info] Containers running. Useful URLs:"
<<<<<<< HEAD
echo "  Front HTTP:  http://localhost:8080/"
echo "  Front HTTPS: https://localhost:8443/"
echo "  Admin:       https://localhost:8443/admin-dev (demo@prestashop.com / prestashop_demo)"
=======
echo "  Front:  https://localhost/"
echo "  Admin:  https://localhost/admin-dev (default: demo@prestashop.com / prestashop_demo)"
>>>>>>> fdba62e4347ae382c8190f7f402d1ade3542b675
echo "[note] If browser warns about certificate, accept the self-signed cert."
