# BRM Student Registry — Analytics-Ready (MySQL + Python + Streamlit)

A portfolio-grade remake of a student/member registry. It goes beyond CRUD:
- Reproducible **MySQL schema + synthetic seed data** (no PII).
- **Analytics queries** (CTE, window functions, data validation).
- Optional **Streamlit dashboard** to present insights.

> Tech: MySQL 8, Python 3.11, Streamlit, SQLAlchemy/PyMySQL, pandas, Docker (for DB).

---

## 1) Quick Start

### A. Clone repo & install Python deps
```bash
git clone <your-repo-url>
cd brm-student-registry
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### B. Start MySQL via Docker Compose
```bash
docker compose up -d
# Wait ~10s for MySQL to be ready, then:
mysql -h 127.0.0.1 -P 3306 -uroot -psecret < sql/schema.sql
mysql -h 127.0.0.1 -P 3306 -uroot -psecret < sql/seed.sql
```

### C. (Optional) Run the dashboard
```bash
streamlit run app/streamlit_app.py
```

---

## 2) Project Structure

```
brm-student-registry/
  ├─ sql/
  │   ├─ schema.sql        # Tables, constraints, indexes
  │   ├─ seed.sql          # Synthetic data (no personal info)
  │   └─ analytics.sql     # 8+ business queries
  ├─ scripts/
  │   ├─ seed_fake.py      # Generator for seed.sql
  │   └─ utils.py          # Helpers (validation, etc.)
  ├─ app/
  │   └─ streamlit_app.py  # 1-page dashboard
  ├─ tests/
  │   └─ test_utils.py     # Unit tests for helpers
  ├─ .env.example          # DB connection variables
  ├─ docker-compose.yml    # MySQL 8 service
  ├─ requirements.txt
  ├─ LICENSE (MIT)
  └─ README.md
```

---

## 3) Analytics Showcases (what recruiters look for)

- **Program size & share** by `program_studi` (+ ranking via window functions).
- **Data quality** checks: invalid phone formats, duplicate `stambuk`.
- **Monthly growth** using `created_at` timestamps.
- **Cohort** by `angkatan` (admission year).

Run samples:
```bash
mysql -h 127.0.0.1 -uroot -psecret brm < sql/analytics.sql
```

---

## 4) How to Present (Portfolio Tips)

- Keep README crisp: Problem → Data → Methods → Results → Recommendations → Limitations.
- Add a 90–120s Loom walkthrough (link at top).
- Include 3–5 metrics/charts max; focus on the “so what”.

---

## 5) Safety & Ethics

- All data is **synthetic**. Do not upload real personal data.
- `seed_fake.py` can regenerate `sql/seed.sql` deterministically (fixed seed).

---

## 6) Next Steps

- Add authentication & activity logs for CRUD.
- Extend schema with related tables (e.g., `kegiatan`, `keanggotaan`).
- Add GitHub Actions (lint, tests).