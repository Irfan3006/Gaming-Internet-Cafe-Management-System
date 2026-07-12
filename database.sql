-- Database Warnet Gaming
CREATE DATABASE IF NOT EXISTS db_warnet;
USE db_warnet;

-- Hapus tabel jika ada untuk reset data
DROP TABLE IF EXISTS transaksi;
DROP TABLE IF EXISTS pelanggan;
DROP TABLE IF EXISTS komputer;

-- 1. Tabel Komputer
CREATE TABLE komputer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomor_pc VARCHAR(50) UNIQUE NOT NULL,
    nama_pc VARCHAR(100) NOT NULL,
    status ENUM('Tersedia', 'Digunakan') DEFAULT 'Tersedia'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Tabel Pelanggan
CREATE TABLE pelanggan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pelanggan VARCHAR(100) NOT NULL,
    nomor_pelanggan VARCHAR(50) UNIQUE NOT NULL,
    jenis_pelanggan ENUM('Biasa', 'Member') DEFAULT 'Biasa'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Tabel Transaksi
CREATE TABLE transaksi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pelanggan INT NOT NULL,
    id_komputer INT NOT NULL,
    durasi INT NOT NULL, -- dalam jam
    tarif_per_jam DECIMAL(10, 2) NOT NULL,
    total_biaya DECIMAL(10, 2) NOT NULL,
    waktu_transaksi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Aktif', 'Selesai') DEFAULT 'Aktif',
    FOREIGN KEY (id_pelanggan) REFERENCES pelanggan(id) ON DELETE CASCADE,
    FOREIGN KEY (id_komputer) REFERENCES komputer(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Memasukkan Data Dummy PC
INSERT INTO komputer (nomor_pc, nama_pc, status) VALUES
('PC-01', 'Gaming PC Elite 1', 'Tersedia'),
('PC-02', 'Gaming PC Elite 2', 'Tersedia'),
('PC-03', 'Gaming PC Pro 1', 'Tersedia'),
('PC-04', 'Gaming PC Pro 2', 'Tersedia'),
('PC-05', 'Streaming PC 1', 'Tersedia');

-- Memasukkan Data Dummy Pelanggan
INSERT INTO pelanggan (nama_pelanggan, nomor_pelanggan, jenis_pelanggan) VALUES
('Irfan Syarifudin', 'PLG-001', 'Biasa'),
('Sufutra Jaya Inathsalen', 'PLG-002', 'Member'),
('Riyan', 'PLG-003', 'Biasa'),
('Aryo Wisanggeni Abdilla', 'PLG-004', 'Member'),
('Eugenius Danto Tandilolo', 'PLG-005', 'Biasa');

-- Memasukkan Data Dummy Transaksi
-- Irfan Syarifudin (PLG-001) menyewa PC-01 selama 2 jam (Selesai)
-- Tarif Biasa = 5000, Total = 10000
INSERT INTO transaksi (id, id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi, status) VALUES
(1, 1, 1, 2, 5000.00, 10000.00, DATE_SUB(NOW(), INTERVAL 5 HOUR), 'Selesai');

-- Sufutra Jaya Inathsalen (PLG-002) menyewa PC-02 selama 3 jam (Selesai)
-- Tarif Member = 4500, Total = 13500
INSERT INTO transaksi (id, id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi, status) VALUES
(2, 2, 2, 3, 4500.00, 13500.00, DATE_SUB(NOW(), INTERVAL 2 HOUR), 'Selesai');

-- Riyan (PLG-003) sedang menyewa PC-03 selama 2 jam (Aktif)
-- Tarif Biasa = 5000, Total = 10000
INSERT INTO transaksi (id, id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi, status) VALUES
(3, 3, 3, 2, 5000.00, 10000.00, NOW(), 'Aktif');

-- Ubah status PC-03 menjadi Digunakan karena transaksi 3 masih aktif
UPDATE komputer SET status = 'Digunakan' WHERE id = 3;

