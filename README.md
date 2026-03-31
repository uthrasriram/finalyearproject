# Transformer-Based Device Health Monitor
## Complete Project — Frontend + Backend + Database

```
device_health/
├── backend/
│   ├── main.py          ← FastAPI app (metrics, health, alerts, WebSocket)
│   ├── database.py      ← SQLAlchemy models (SQLite / PostgreSQL)
│   └── requirements.txt
└── frontend/
    └── index.html       ← Dashboard (connects via WebSocket)
```

---

## Quick Start (SQLite — no extra setup)

### Step 1 — Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2 — Run backend
```bash
uvicorn main:app --reload --port 8000
```

### Step 3 — Open frontend
Open `frontend/index.html` in your browser.
The dashboard auto-connects to `ws://localhost:8000/ws`.

---

## PostgreSQL Setup (recommended for production)

### Install PostgreSQL
```bash
# Ubuntu
sudo apt install postgresql -y && sudo systemctl start postgresql

# macOS
brew install postgresql@15 && brew services start postgresql@15

# Windows
winget install PostgreSQL.PostgreSQL
```

### Create database
```sql
psql -U postgres
CREATE DATABASE device_health_db;
CREATE USER health_user WITH PASSWORD 'health@1234';
GRANT ALL PRIVILEGES ON DATABASE device_health_db TO health_user;
\q
```

### Install PostgreSQL driver
```bash
pip install psycopg2-binary
```

### Set environment variable and run
```bash
# Linux / macOS
export DATABASE_URL="postgresql://health_user:health@1234@localhost:5432/device_health_db"
uvicorn main:app --reload --port 8000

# Windows PowerShell
$env:DATABASE_URL="postgresql://health_user:health@1234@localhost:5432/device_health_db"
uvicorn main:app --reload --port 8000
```

---

## Phone Monitoring (Android ADB)

1. Enable Developer Options on Android phone
2. Enable USB Debugging
3. Connect via USB
4. Install ADB:
   ```bash
   # Ubuntu
   sudo apt install adb
   # macOS
   brew install android-platform-tools
   ```
5. Verify: `adb devices`
6. Switch dashboard to Phone mode — click 📱 Phone button

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/status` | Server + DB record count |
| GET | `/device` | Current device |
| POST | `/device/laptop` | Switch to laptop |
| POST | `/device/phone` | Switch to phone |
| GET | `/snapshot` | Full snapshot (saves to DB) |
| GET | `/health-score` | Health + RUL only |
| WS | `/ws` | Live stream every 1.5s |
| GET | `/db/metrics` | Stored metric records |
| GET | `/db/health` | Stored health records |
| GET | `/db/alerts` | Stored alerts |
| PATCH | `/db/alerts/{id}/acknowledge` | Ack an alert |
| GET | `/db/stats` | Aggregate stats |
| GET | `/db/sessions` | Monitoring sessions |
| DELETE | `/db/clear` | ⚠️ Clear all data |

### Query parameters
```
/db/metrics?device=laptop&limit=100&hours=24
/db/alerts?severity=critical&unacknowledged_only=true
```

---

## Database Tables

| Table | Purpose |
|-------|---------|
| `metric_records` | Raw CPU, RAM, temp, battery etc. |
| `health_records` | Health score, RUL, risk, failure probs |
| `alert_records` | All alerts with severity + ack status |
| `device_sessions` | Each server run with avg health summary |

---

## Interactive API Docs
Open `http://localhost:8000/docs` after starting the server.
