HomeTest — Minimal README
=========================

Description
-----------------
Small Python service for file uploads and transaction processing. Entrypoint: `apps.py` (run the app from project root).

Data flow
-------------------------
Request → Router (`app/api`) → Handler (DTO, validate) → Service (business logic) → Repository (`app/models`, `utils/db_utils`) → Handler → HTTP response.

Commands (PowerShell)
---------------------
# 1. Run locally (development)
```powershell
python .\apps.py
```

# 2. Create SQLite fallback DB (optional)
```powershell
python .\scripts\create_fallback_db.py
```

# 3. Build Docker image for app
```powershell
docker build -t hometest:latest .
```

# 4. Run Postgres + app with docker-compose (recommended)
```powershell
docker-compose up -d --build
```

# 5. Run Postgres standalone (if not using compose)
```powershell
docker run --name hometest-db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=database -p 5432:5432 -v hometest_db:/var/lib/postgresql/data -d postgres:15-alpine
```

# 6. Run app container (after build)
```powershell
docker run --rm --name hometest-app -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=database -e POSTGRES_PORT=5432 -p 8000:8000 hometest:latest
```

# 7. Logs / stop
```powershell
docker-compose logs -f app

docker-compose down -v
```

Notes
-----
- Set `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_PORT` via environment or `.env` to match `settings.py`.
- `apps.py` is the required app entrypoint.
