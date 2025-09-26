import os
import psycopg2
from dotenv import load_dotenv

# Load .env
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

MIGRATIONS_DIR = "migrations"

def ensure_migrations_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    conn.commit()

def applied_versions(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT version FROM schema_migrations")
        return {row[0] for row in cur.fetchall()}

def run_migrations():
    conn = psycopg2.connect(DB_URL)
    ensure_migrations_table(conn)
    applied = applied_versions(conn)

    for fname in sorted(os.listdir(MIGRATIONS_DIR)):
        if not fname.endswith(".sql"):
            continue
        version = fname.split("_", 1)[0]  # e.g. "001"
        if version in applied:
            continue
        print(f"Applying migration {fname}...")
        with open(os.path.join(MIGRATIONS_DIR, fname), "r", encoding="utf-8") as f:
            sql = f.read()
        with conn.cursor() as cur:
            cur.execute(sql)
            cur.execute("INSERT INTO schema_migrations(version) VALUES (%s)", (version,))
        conn.commit()
    conn.close()

if __name__ == "__main__":
    run_migrations()
