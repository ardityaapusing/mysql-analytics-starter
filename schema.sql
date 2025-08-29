-- Drop & create database for clean runs
CREATE DATABASE IF NOT EXISTS brm;
USE brm;

-- Drop existing table if any
DROP TABLE IF EXISTS tb_mahasiswa_brm;

-- Main table
CREATE TABLE tb_mahasiswa_brm (
  nomor INT AUTO_INCREMENT PRIMARY KEY,
  stambuk VARCHAR(20) NOT NULL UNIQUE,
  nama VARCHAR(100) NOT NULL,
  jenis_kelamin ENUM('L','P') NOT NULL,
  program_studi ENUM('Statistika','Matematika','Fisika','Kimia','Biologi','Teknik Geofisika') NOT NULL,
  no_hp VARCHAR(20) NOT NULL,
  angkatan INT NOT NULL CHECK (angkatan BETWEEN 2000 AND 2100),
  alamat VARCHAR(255),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT chk_no_hp CHECK (no_hp REGEXP '^[0-9+]{8,20}$')
);

-- Helpful index for analytics
CREATE INDEX idx_program ON tb_mahasiswa_brm(program_studi);
CREATE INDEX idx_angkatan ON tb_mahasiswa_brm(angkatan);
CREATE INDEX idx_created_at ON tb_mahasiswa_brm(created_at);