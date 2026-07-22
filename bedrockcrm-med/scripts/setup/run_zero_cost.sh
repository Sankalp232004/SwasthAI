#!/bin/bash
set -euo pipefail

# Run SwasthAI in zero-cost mode (SQLite + local host)
# Usage: bash scripts/setup/run_zero_cost.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

if [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
  PY="$ROOT_DIR/.venv/bin/python"
else
  PY="python3"
fi

export DATABASE_URL="${DATABASE_URL:-sqlite:////tmp/swasthai_free.db}"
export FLASK_ENV="${FLASK_ENV:-production}"
export PORT="${PORT:-5010}"
export APP_BASE_URL="${APP_BASE_URL:-http://127.0.0.1:${PORT}}"
export DEMO_BASE_URL="${DEMO_BASE_URL:-$APP_BASE_URL}"

if [[ -z "${SECRET_KEY:-}" ]]; then
  SECRET_KEY="$(date +%s | shasum | awk '{print $1}')"
  export SECRET_KEY
fi

echo "========================================"
echo " SwasthAI Zero-Cost Mode"
echo "========================================"
echo "DB:   $DATABASE_URL"
echo "URL:  $APP_BASE_URL"
echo "PY:   $PY"
echo ""

echo "[1/3] Initializing schema..."
"$PY" -m scripts.setup.init_db

echo "[2/3] Seeding demo users/data..."
"$PY" -m scripts.setup.create_superadmin
"$PY" -m scripts.setup.create_clinic
"$PY" -m scripts.setup.prepare_demo || true

echo "[3/3] Starting app..."
if "$PY" -c "import gunicorn" >/dev/null 2>&1; then
  exec "$PY" -m gunicorn --bind "0.0.0.0:${PORT}" --worker-class gevent --workers 2 --timeout 180 run:app
else
  exec "$PY" run.py
fi
