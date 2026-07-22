#!/bin/bash
# Startup script for SwasthAI container
# Handles database setup and starts gunicorn

set -e  # Exit on error

echo "========================================"
echo "  SwasthAI - Starting Application"
echo "========================================"

# Railway provides postgres:// but SQLAlchemy requires postgresql://
if [[ "${DATABASE_URL:-}" == postgres://* ]]; then
  export DATABASE_URL="postgresql://${DATABASE_URL#postgres://}"
  echo "[startup] Fixed DATABASE_URL scheme: postgres:// -> postgresql://"
fi

echo ""
echo "[startup] Waiting for database..."
python3 -m scripts.setup.wait_for_db
DB_EXIT=$?
if [ $DB_EXIT -ne 0 ]; then
  echo "[startup] Database wait failed - aborting"
  exit 1
fi

echo ""
echo "[startup] Initializing database schema..."
python3 -m scripts.setup.init_db || echo "[startup] WARNING: scripts.setup.init_db failed (continuing)"

echo ""
echo "[startup] Setting up default data..."
python3 -m scripts.setup.create_clinic || echo "[startup] WARNING: scripts.setup.create_clinic failed (continuing)"
python3 -m scripts.setup.create_superadmin || echo "[startup] WARNING: scripts.setup.create_superadmin failed (continuing)"

echo ""
echo "[startup] Starting gunicorn on port ${PORT:-5000}..."
PORT=${PORT:-5000}

# Try to use gevent worker for SSE support, fallback to sync if unavailable
if python3 -c "import gevent" 2>/dev/null; then
    echo "[startup] Using gevent worker for SSE support..."
    exec gunicorn --bind "0.0.0.0:${PORT}" \
        --worker-class gevent \
        --workers 2 \
        --worker-connections 100 \
        --timeout 300 \
        --keep-alive 75 \
        --access-logfile - \
        --error-logfile - \
        "run:app"
else
    echo "[startup] WARNING: gevent not available, using sync worker (SSE may not work optimally)"
    exec gunicorn --bind "0.0.0.0:${PORT}" \
        --workers 4 \
        --worker-class sync \
        --timeout 300 \
        --keep-alive 75 \
        --access-logfile - \
        --error-logfile - \
        "run:app"
fi
