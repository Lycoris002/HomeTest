-- init_sqlite.sql
-- Creates SQLite schema compatible with app/models/data_models.py

PRAGMA foreign_keys = OFF;

CREATE TABLE IF NOT EXISTS file_metadata (
  id TEXT PRIMARY KEY,
  filename TEXT NOT NULL,
  size_bytes INTEGER NOT NULL,
  upload_time TEXT NOT NULL,
  row_count INTEGER NOT NULL,
  path TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  file_id TEXT NOT NULL,
  transaction_id TEXT NOT NULL,
  date TEXT NOT NULL,
  category TEXT NOT NULL,
  amount NUMERIC(12,2) NOT NULL,
  currency TEXT(3) NOT NULL,
  UNIQUE(file_id, transaction_id)
);

-- Example seed data: replace or extend as needed
INSERT OR IGNORE INTO file_metadata (id, filename, size_bytes, upload_time, row_count, path) VALUES
('11111111-1111-1111-1111-111111111111','test.csv',1024,'2025-12-14T12:00:00',10,'uploads/test.csv');

INSERT OR IGNORE INTO transactions (file_id, transaction_id, date, category, amount, currency) VALUES
('11111111-1111-1111-1111-111111111111','tx-0001','2025-12-14T12:01:00','groceries',12.34,'USD'),
('11111111-1111-1111-1111-111111111111','tx-0002','2025-12-14T12:02:00','entertainment',45.00,'USD');

