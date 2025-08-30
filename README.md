# MySQL + SQL Analytics Starter — Registry Dashboard (Streamlit)

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)

Short demo (2 min): _coming soon_

A portfolio-ready starter that goes beyond CRUD:
- Reproducible **MySQL schema + synthetic seed data** (no PII).
- **SQL analytics** with CTEs, window functions, and data-quality checks.
- A **one-page Streamlit dashboard** to present insights quickly.

> Tech: MySQL 8, Python 3.11, pandas, Streamlit, SQLAlchemy/PyMySQL, Docker (for DB).

---

## Table of Contents
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Analytics Highlights](#analytics-highlights)
- [Dashboard](#dashboard)
- [Reproducibility & Data Ethics](#reproducibility--data-ethics)
- [Key Insights (fill after running queries)](#key-insights-fill-after-running-queries)
- [Limitations & Next Steps](#limitations--next-steps)
- [License](#license)

---

## Quick Start

> **Prereqs:** Docker (for MySQL), Python 3.11  
> **Optional:** Use a virtual environment.

```bash
# Clone & setup
git clone https://github.com/ardityaapusing/mysql-analytics-starter.git
cd mysql-analytics-starter
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Start MySQL and load schema + seed (fully synthetic)
docker compose up -d
mysql -h 127.0.0.1 -P 3306 -uroot -psecret < sql/schema.sql
mysql -h 127.0.0.1 -P 3306 -uroot -psecret < sql/seed.sql

# (Optional) Run the dashboard
streamlit run app/streamlit_app.py
```

**Run all analytics queries**
```bash
mysql -h 127.0.0.1 -P 3306 -uroot -psecret < sql/analytics.sql
```

---

## Project Structure
```
mysql-analytics-starter/
  ├─ sql/
  │   ├─ schema.sql        # Tables, constraints, indexes
  │   ├─ seed.sql          # Synthetic data (no personal info)
  │   └─ analytics.sql     # 8+ business queries (CTE + window + DQ checks)
  ├─ scripts/
  │   ├─ seed_fake.py      # Deterministic generator for seed.sql
  │   └─ utils.py          # Helpers (validation, normalization)
  ├─ app/
  │   └─ streamlit_app.py  # 1-page dashboard reading from MySQL
  ├─ tests/
  │   └─ test_utils.py     # Unit tests for helpers
  ├─ .env.example          # DB connection variables
  ├─ docker-compose.yml    # MySQL 8 service
  ├─ requirements.txt
  ├─ LICENSE (MIT)
  └─ README.md
```

---

## Analytics Highlights

### 1) Program size & ranking (CTE + window)
Ranks programs by record count and shows share of total.
```sql
WITH counts AS (
  SELECT program_studi, COUNT(*) AS n
  FROM tb_mahasiswa_brm
  GROUP BY program_studi
)
SELECT program_studi, n,
       ROUND(100.0 * n / SUM(n) OVER (), 2) AS pct,
       RANK() OVER (ORDER BY n DESC) AS rnk
FROM counts
ORDER BY rnk;
```

### 2) Data-quality checks
Validate phone patterns and detect duplicate IDs.
```sql
-- Invalid phone patterns
SELECT * FROM tb_mahasiswa_brm
WHERE NOT (no_hp REGEXP '^[0-9+]{8,20}$');

-- Duplicate stambuk guardrail
SELECT stambuk, COUNT(*) AS dup_count
FROM tb_mahasiswa_brm
GROUP BY stambuk
HAVING COUNT(*) > 1;
```

### 3) Monthly growth & cohorts
Track growth by month and simple cohort by admission year.
```sql
SELECT DATE_FORMAT(created_at, '%Y-%m') AS ym, COUNT(*) AS n
FROM tb_mahasiswa_brm
GROUP BY ym
ORDER BY ym;

SELECT angkatan, COUNT(*) AS n
FROM tb_mahasiswa_brm
GROUP BY angkatan
ORDER BY angkatan DESC;
```

---

## Dashboard
A single-page Streamlit app that surfaces key metrics (overview, ranking, data quality, growth, cohort) directly from MySQL.

- Entry point: `app/streamlit_app.py`  
- Connects via SQLAlchemy → pandas → charts  
- Intended as a quick, reviewer-friendly view

_(Clickable preview can be added later after you record a demo.)_

---

## Reproducibility & Data Ethics
- **Deterministic seed:** `scripts/seed_fake.py` (fixed random seed)  
- **No PII:** all records are synthetic; do **not** commit real personal data  
- **One-click DB:** `docker-compose.yml` + `sql/schema.sql` + `sql/seed.sql`

---

## Key Insights (fill after running queries)
Replace placeholders after executing `sql/analytics.sql`.

- **Top programs:** `Program_A` (#1 with **N1** records) and `Program_B` (#2 with **N2**).  
- **Data quality:** invalid phone rate **X%**; duplicate `stambuk`: **D** records **flagged**.  
- **Growth:** highest month **YYYY-MM** with **M** new records; steady MoM trend overall.

---

## Limitations & Next Steps
- Add authentication & activity logs for CRUD.  
- Extend schema with related tables (e.g., `kegiatan`, `keanggotaan`).  
- Add CI (tests & linting) and a short Loom demo.  
- (If needed) Migrate to a cloud warehouse (e.g., BigQuery/DuckDB) for larger data.

---

## License
This project is licensed under the MIT License.
