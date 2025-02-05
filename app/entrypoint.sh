#!/usr/bin/env bash
# start-server.sh

postgres_ready() {
python << END
import sys
import psycopg2
try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

alembic revision --autogenerate -m "create initial tables"

echo "Running Alembic migrations..."

alembic upgrade head

# Start the Uvicorn server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload