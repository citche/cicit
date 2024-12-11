-- Membuat database db_gymrist
CREATE DATABASE db_gymrist;

-- Menggunakan database db_gymrist
USE db_gymrist;

-- Membuat tabel users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- Primary key
    username VARCHAR(50) NOT NULL UNIQUE,     -- Kolom username dengan nilai unik
    password VARCHAR(255) NOT NULL,           -- Kolom password yang terenkripsi
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp untuk pencatatan waktu pembuatan akun
);

CREATE TABLE gym_schedule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    day VARCHAR(20) NOT NULL,
    time_slot VARCHAR(50) NOT NULL,
    class_name VARCHAR(100) NOT NULL,
    instructor VARCHAR(100) NOT NULL
);

