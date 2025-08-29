USE brm;

-- 1) Size & share by program
WITH counts AS (
  SELECT program_studi, COUNT(*) AS n
  FROM tb_mahasiswa_brm
  GROUP BY program_studi
)
SELECT
  program_studi,
  n,
  ROUND(100.0 * n / SUM(n) OVER (), 2) AS pct
FROM counts
ORDER BY n DESC;

-- 2) Ranking programs by size (window)
WITH counts AS (
  SELECT program_studi, COUNT(*) AS n
  FROM tb_mahasiswa_brm
  GROUP BY program_studi
)
SELECT
  program_studi,
  n,
  RANK() OVER (ORDER BY n DESC) AS rnk
FROM counts
ORDER BY rnk;

-- 3) Detect invalid phone numbers (should be 8-20 chars digits or leading +)
SELECT *
FROM tb_mahasiswa_brm
WHERE NOT (no_hp REGEXP '^[0-9+]{8,20}$');

-- 4) Potential duplicates on stambuk (should be unique)
SELECT stambuk, COUNT(*) AS dup_count
FROM tb_mahasiswa_brm
GROUP BY stambuk
HAVING COUNT(*) > 1;

-- 5) Monthly growth
SELECT
  DATE_FORMAT(created_at, '%Y-%m') AS ym,
  COUNT(*) AS n
FROM tb_mahasiswa_brm
GROUP BY ym
ORDER BY ym;

-- 6) Cohort by angkatan
SELECT angkatan, COUNT(*) AS n
FROM tb_mahasiswa_brm
GROUP BY angkatan
ORDER BY angkatan DESC;

-- 7) Top 10 newest records (sanity check)
SELECT *
FROM tb_mahasiswa_brm
ORDER BY created_at DESC
LIMIT 10;

-- 8) Phone prefix distribution (simple profiling)
SELECT
  LEFT(no_hp, 4) AS prefix,
  COUNT(*) AS n
FROM tb_mahasiswa_brm
GROUP BY prefix
ORDER BY n DESC
LIMIT 10;