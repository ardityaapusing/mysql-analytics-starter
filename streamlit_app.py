import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")
DB_NAME = os.getenv("DB_NAME", "brm")

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

st.set_page_config(page_title="BRM Registry Dashboard", layout="wide")
st.title("📊 BRM Student Registry — Analytics")

tabs = st.tabs(["Overview", "Program Ranking", "Data Quality", "Monthly Growth", "Cohort"])

with tabs[0]:
    st.subheader("Overview")
    q = text("""
        SELECT COUNT(*) as total,
               COUNT(DISTINCT program_studi) as programs,
               MIN(created_at) as first_record,
               MAX(created_at) as last_record
        FROM tb_mahasiswa_brm
    """)
    with engine.connect() as conn:
        row = conn.execute(q).mappings().one()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Records", f"{row['total']:,}")
    c2.metric("Programs", row['programs'])
    c3.metric("First Record", str(row['first_record']))
    c4.metric("Last Record", str(row['last_record']))

with tabs[1]:
    st.subheader("Program Size & Ranking")
    q = text("""
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
    """)
    with engine.connect() as conn:
        df = pd.read_sql(q, conn)
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df.set_index("program_studi")["n"])

with tabs[2]:
    st.subheader("Data Quality Checks")
    q_invalid = text("""
        SELECT * FROM tb_mahasiswa_brm
        WHERE NOT (no_hp REGEXP '^[0-9+]{8,20}$');
    """)
    with engine.connect() as conn:
        df_inv = pd.read_sql(q_invalid, conn)
    st.write("Invalid phone numbers")
    st.dataframe(df_inv, use_container_width=True)

with tabs[3]:
    st.subheader("Monthly Growth")
    q = text("""
        SELECT DATE_FORMAT(created_at, '%Y-%m') AS ym, COUNT(*) AS n
        FROM tb_mahasiswa_brm
        GROUP BY ym
        ORDER BY ym;
    """)
    with engine.connect() as conn:
        df = pd.read_sql(q, conn)
    st.line_chart(df.set_index("ym")["n"])

with tabs[4]:
    st.subheader("Cohort by Angkatan")
    q = text("""
        SELECT angkatan, COUNT(*) AS n
        FROM tb_mahasiswa_brm
        GROUP BY angkatan
        ORDER BY angkatan DESC;
    """)
    with engine.connect() as conn:
        df = pd.read_sql(q, conn)
    st.bar_chart(df.set_index("angkatan")["n"])