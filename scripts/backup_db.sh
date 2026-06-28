#!/usr/bin/env bash
# Dumps the Postgres database to backups/ with a timestamped filename.
# Intended to be run on a schedule (e.g. cron/systemd timer) against the
# running docker-compose stack (Engineering Rules §20: Automatic backups).
set -euo pipefail

BACKUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/backups"
mkdir -p "$BACKUP_DIR"

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
OUTPUT_FILE="${BACKUP_DIR}/real_estate_ai-${TIMESTAMP}.sql.gz"

docker compose exec -T postgres pg_dump -U "${POSTGRES_USER:-real_estate_ai}" "${POSTGRES_DB:-real_estate_ai}" \
  | gzip > "$OUTPUT_FILE"

echo "Backup written to ${OUTPUT_FILE}"
