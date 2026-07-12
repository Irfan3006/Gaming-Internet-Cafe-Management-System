# Sistem Manajemen Warnet Gaming

Sistem Manajemen Warnet Gaming adalah aplikasi berbasis web yang dirancang untuk mengelola operasional warnet secara modular, terstruktur, dan efisien. Aplikasi ini dibangun menggunakan framework Python Flask, basis data MySQL, serta menerapkan konsep Object-Oriented Programming (OOP) untuk memenuhi tugas akhir mata kuliah Pemograman Berorientasi Objek Python Lanjutan.

## Anggota Kelompok / Pengembang

Aplikasi ini dikembangkan oleh:
1. Irfan Syarifudin (24.83.1127)
2. Sufutra Jaya Inathsalen (24.83.1147)
3. Riyan (24.84.1113)
4. Aryo Wisanggeni Abdilla (24.83.1131)
5. Eugenius Danto Tandilolo (24.83.1128)

## Fitur Utama Aplikasi

1. **Dashboard Admin**: Menyajikan metrik operasional secara real-time (total komputer, ketersediaan komputer, sesi aktif, jumlah pelanggan, total transaksi, serta tren pendapatan harian).
2. **Manajemen Komputer (CRUD)**: Mengelola data unit komputer (nomor PC, nama/spesifikasi PC, dan status penggunaan).
3. **Manajemen Pelanggan (CRUD)**: Mengelola data pelanggan dengan pembagian kategori antara Pelanggan Biasa dan Member.
4. **Transaksi Penyewaan**: Memproses sesi sewa baru dengan pemilihan pelanggan dan komputer yang tersedia, serta penentuan durasi sewa.
5. **Kalkulasi Biaya Real-Time (AJAX)**: Menghitung biaya sewa secara instan pada antarmuka pengguna sebelum transaksi disimpan ke basis data.
6. **Penyelesaian Sesi Sewa**: Menyelesaikan sesi penggunaan komputer secara dinamis yang otomatis mengubah status transaksi menjadi Selesai dan mengembalikan status komputer menjadi Tersedia.
7. **Laporan Pendapatan**: Menyediakan pencarian data berdasarkan filter tanggal serta visualisasi grafik tren pendapatan menggunakan Chart.js.

## Teknologi yang Digunakan

* **Backend**: Python Flask
* **Database**: MySQL (diakses melalui modul PyMySQL)
* **Frontend**: HTML, CSS, JavaScript (Bootstrap 5 & Bootstrap Icons)
* **Visualisasi Grafik**: Chart.js

## Panduan Instalasi dan Menjalankan Aplikasi

### Prasyarat
* Python 3 terinstal di sistem operasi Anda.
* Laragon atau server MySQL lokal dalam kondisi aktif pada port 3306.

### Langkah-Langkah Instalasi
1. Kloning atau salin folder repositori ini ke dalam direktori kerja Anda.
2. Buat basis data baru bernama `db_warnet` pada server MySQL Anda melalui phpMyAdmin atau klien SQL lainnya.
3. Impor berkas `database.sql` ke dalam basis data `db_warnet` untuk membuat skema tabel dan data awal.
4. Buka terminal pada direktori root project, kemudian instal dependensi pustaka Python yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```
5. Jalankan aplikasi Flask dengan perintah:
   ```bash
   python app.py
   ```
6. Akses aplikasi melalui web browser pada alamat:
   ```text
   http://localhost:5000/
   ```

## Penerapan Konsep Object-Oriented Programming (OOP)

Implementasi OOP diterapkan secara nyata pada alur pemrograman berikut:

### 1. Class dan Object
Semua entitas diwakili oleh kelas terdedikasi di dalam direktori `models/`:
* `Komputer`: merepresentasikan unit PC komputer.
* `Pelanggan`: merepresentasikan data pelanggan biasa.
* `Member`: merepresentasikan data pelanggan yang terdaftar sebagai member.
* `Transaksi`: mengaitkan objek pelanggan dengan objek komputer untuk satu sesi sewa.
* `Warnet`: bertindak sebagai kontrolir utama bisnis warnet.

### 2. Encapsulation (Enkapsulasi)
Setiap atribut pada objek dilindungi menggunakan tanda baris bawah (`_`) dan diakses melalui properti dekorator getter/setter. Perubahan status objek divalidasi secara internal:
* Metode `ubah_status(status_baru)` pada kelas `Komputer` membatasi pengisian status hanya pada nilai yang valid (Tersedia / Digunakan).
* Metode `selesaikan()` pada kelas `Transaksi` mengubah status transaksi dan secara terenkapsulasi langsung mengubah status objek `Komputer` terkait kembali ke Tersedia.

### 3. Inheritance (Pewarisan)
* Kelas `Member` didefinisikan sebagai subclass dari kelas `Pelanggan` (`class Member(Pelanggan):`). Melalui struktur ini, kelas `Member` secara langsung mewarisi atribut nama, nomor pelanggan, dan id dari kelas induk tanpa redundansi penulisan kode.

### 4. Polymorphism (Polimorfisme)
* Polimorfisme diimplementasikan melalui metode `hitung_biaya(durasi)`.
* Objek `Pelanggan` reguler menghitung biaya sewa dengan tarif Rp 5.000 per jam.
* Objek `Member` menghitung biaya sewa dengan tarif potongan khusus Rp 4.500 per jam.
* Saat sistem memanggil `pelanggan.hitung_biaya(durasi)` di kelas `Warnet`, hasil perhitungan otomatis menyesuaikan instans objek pelanggan terkait secara dinamis.

### 5. Abstraction (Abstraksi)
* Kelas abstrak `BaseWarnet` dibuat menggunakan kelas `ABC` dari modul standard Python `abc` untuk mendefinisikan kontrak operasi warnet (seperti `sewa_komputer`, `selesaikan_sewa`, dll.).
* Detail implementasi query basis data (SQL) dan mapping relasional ke objek disembunyikan di dalam concrete class `Warnet`.
