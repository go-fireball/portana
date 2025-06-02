
# Portana

**Portana** is a portfolio analysis and transaction tracking system built with Python, SQLAlchemy, Alembic, and PostgreSQL. It supports multi-account transaction ingestion, position snapshots, and options tracking.

---

## 🔧 Developer Setup

### 1. Install Dependencies
```bash
poetry install
```

### 2. Create `.env` or configure `alembic.ini` with DB credentials

Make sure your PostgresSQL DB is running and accessible at:

```
postgresql://portana:secret@localhost:5432/portana
```

---

## 🛠 Making Model Changes

### 1. Modify your model(s) in `app/models/`

### 2. Autogenerate a migration
```bash
poetry run alembic revision --autogenerate -m "your message here"
```

### 3. Apply the migration
```bash
poetry run alembic upgrade head
```

---

## 🧪 Example CLI Usage
```bash
poetry run python -m app <command> [options]
```
### Create a new user
```bash
poetry run python -m app create-user \
  --email venkat@example.com \
  --name "Venkat Sundaram"
```

### Create an account for a user
```bash
poetry run python -m app create-account \
  --email venkat@example.com \
  --brokerage schwab \
  --account_number 123456 \
  --nickname "Rollover IRA"
```

### Import Fidelity Positions
```bash
poetry run python -m app import \
  --broker fidelity \
  --format positions \
  --email venkat@example.com \
  --account 123456 \
  --file "./data/Fidelity-Positions.csv"
```

### Import Schwab Lot Details
```bash
poetry run python -m app import \
  --broker schwab \
  --format lot_details \
  --email venkat@example.com \
  --account 123456 \
  --file "./data/Lot-Details.csv"
```

### Import Schwab Transactions
```bash
poetry run python -m app import \
  --broker schwab \
  --format transactions \
  --email venkat@example.com \
  --account 123456 \
  --file "./data/Schwab-Transactions.csv"
```

### Import Vanguard Transactions
```bash
poetry run python -m app import \
  --broker vanguard \
  --format transactions \
  --email venkat@example.com \
  --account 123456 \
  --file "./data/Vanguard-Transactions.csv"
```

### Recalculate Positions

```bash
poetry run python -m app recalculate-positions \
  --email venkat@example.com \
  --initial_load

```

```bash
poetry run python -m app recalculate-positions \
  --email venkat@gmail.com
```

### Load Prices
```bash
poetry run python -m app fetch-prices
```

---

## 📁 Project Structure

```
backend/
├── alembic/                # Migrations
├── app/
│   ├── models/             # SQLAlchemy models
│   ├── importers/          # Schwab & other data importers
│   ├── services/           # User/account creation logic
│   └── main.py             # CLI entrypoint
├── pyproject.toml          # Poetry config
└── README.md               # You're here!
```

---

## 📌 Tips

- Always commit migration files after generating them.
- Use `poetry run` to run any scripts inside the virtualenv.
- Use `psql` or any DB UI (e.g., pgAdmin, TablePlus) to inspect the PostgreSQL DB.

---

Happy analyzing!
