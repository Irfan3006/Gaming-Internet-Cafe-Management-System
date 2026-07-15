CREATE DATABASE IF NOT EXISTS db_warnet;
USE db_warnet;

DROP TABLE IF EXISTS transaksi;
DROP TABLE IF EXISTS pelanggan;
DROP TABLE IF EXISTS komputer;
DROP TABLE IF EXISTS kontak;

CREATE TABLE komputer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomor_pc VARCHAR(50) UNIQUE NOT NULL,
    nama_pc VARCHAR(100) NOT NULL,
    spesifikasi VARCHAR(255) NOT NULL DEFAULT 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz',
    status ENUM('Tersedia', 'Digunakan') DEFAULT 'Tersedia'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pelanggan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pelanggan VARCHAR(100) NOT NULL,
    nomor_pelanggan VARCHAR(50) UNIQUE NOT NULL,
    jenis_pelanggan ENUM('Biasa', 'Member') DEFAULT 'Biasa'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE transaksi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pelanggan INT NOT NULL,
    id_komputer INT NOT NULL,
    durasi INT NOT NULL,
    tarif_per_jam DECIMAL(10, 2) NOT NULL,
    total_biaya DECIMAL(10, 2) NOT NULL,
    waktu_transaksi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Aktif', 'Selesai') DEFAULT 'Aktif',
    FOREIGN KEY (id_pelanggan) REFERENCES pelanggan(id) ON DELETE CASCADE,
    FOREIGN KEY (id_komputer) REFERENCES komputer(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO komputer (nomor_pc, nama_pc, status) VALUES
('PC-01', 'Gaming PC Elite 1', 'Tersedia'),
('PC-02', 'Gaming PC Elite 2', 'Tersedia'),
('PC-03', 'Gaming PC Pro 1', 'Tersedia'),
('PC-04', 'Gaming PC Pro 2', 'Tersedia'),
('PC-05', 'Streaming PC 1', 'Tersedia');

INSERT INTO pelanggan (nama_pelanggan, nomor_pelanggan, jenis_pelanggan) VALUES
('Irfan Syarifudin', 'PLG-001', 'Biasa'),
('Kevin Sufutra Jaya', 'PLG-002', 'Member'),
('Riyan Antony', 'PLG-003', 'Biasa'),
('Michael Aryo Wisanggeni', 'PLG-004', 'Member'),
('Bagas Tegar Pratama', 'PLG-005', 'Biasa');

INSERT INTO transaksi (id, id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi, status) VALUES
(1, 1, 1, 2, 5000.00, 10000.00, DATE_SUB(NOW(), INTERVAL 5 HOUR), 'Selesai');

INSERT INTO transaksi (id, id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi, status) VALUES
(2, 2, 2, 3, 4500.00, 13500.00, DATE_SUB(NOW(), INTERVAL 2 HOUR), 'Selesai');

INSERT INTO transaksi (id, id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi, status) VALUES
(3, 3, 3, 2, 5000.00, 10000.00, NOW(), 'Aktif');

UPDATE komputer SET status = 'Digunakan' WHERE id = 3;

CREATE TABLE kontak (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    subjek VARCHAR(150) NOT NULL,
    pesan TEXT NOT NULL,
    waktu_kirim TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
