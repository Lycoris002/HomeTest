import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL_FILE = ROOT / "init_sqlite.sql"
DB_FILE = ROOT / "fallback.db"

print(f"SQL: {SQL_FILE}")
print(f"DB: {DB_FILE}")

with sqlite3.connect(DB_FILE) as conn:
    with open(SQL_FILE, "r", encoding="utf-8") as f:
        sql = f.read()
    conn.executescript(sql)
    cur = conn.cursor()
    for tbl in ("file_metadata", "transactions"):
        cur.execute(f"SELECT COUNT(*) FROM {tbl}")
        cnt = cur.fetchone()[0]
        print(f"{tbl}: {cnt}")

print("Done")

