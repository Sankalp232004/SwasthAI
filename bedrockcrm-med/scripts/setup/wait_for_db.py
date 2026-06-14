import time, os, sys

try:
    import psycopg2
    from urllib.parse import urlparse
except ImportError as e:
    print(f"[startup] Import error: {e}")
    sys.exit(1)

db_url = os.environ.get("DATABASE_URL", "")
if db_url.startswith("postgres://"):
    db_url = "postgresql://" + db_url[len("postgres://"):]

if not db_url.startswith("postgresql://"):
    print("[startup] No DATABASE_URL set - skipping wait")
    sys.exit(0)

r = urlparse(db_url)
for i in range(60):
    try:
        c = psycopg2.connect(
            database=r.path[1:],
            user=r.username,
            password=r.password,
            host=r.hostname,
            port=r.port or 5432
        )
        c.close()
        print(f"[startup] Database ready after {i+1} attempt(s)")
        sys.exit(0)
    except Exception as e:
        print(f"[startup] Attempt {i+1}/60: {e}")
        time.sleep(2)

print("[startup] ERROR: Database never became ready after 120s")
sys.exit(1)
