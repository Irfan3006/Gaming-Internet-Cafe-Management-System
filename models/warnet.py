from abc import ABC, abstractmethod
import pymysql
from models.komputer import Komputer
from models.pelanggan import Pelanggan, Member
from models.transaksi import Transaksi
from datetime import datetime

# Abstraction: Mendefinisikan kontrak sistem warnet
class BaseWarnet(ABC):
    @abstractmethod
    def get_semua_komputer(self):
        pass

    @abstractmethod
    def get_komputer(self, id_komputer):
        pass

    @abstractmethod
    def tambah_komputer(self, nomor_pc, nama_pc):
        pass

    @abstractmethod
    def edit_komputer(self, id_komputer, nomor_pc, nama_pc, status):
        pass

    @abstractmethod
    def hapus_komputer(self, id_komputer):
        pass

    @abstractmethod
    def get_semua_pelanggan(self):
        pass

    @abstractmethod
    def get_pelanggan(self, id_pelanggan):
        pass

    @abstractmethod
    def tambah_pelanggan(self, nama_pelanggan, nomor_pelanggan, jenis_pelanggan):
        pass

    @abstractmethod
    def edit_pelanggan(self, id_pelanggan, nama_pelanggan, nomor_pelanggan, jenis_pelanggan):
        pass

    @abstractmethod
    def hapus_pelanggan(self, id_pelanggan):
        pass

    @abstractmethod
    def sewa_komputer(self, id_pelanggan, id_komputer, durasi):
        pass

    @abstractmethod
    def selesaikan_sewa(self, id_transaksi):
        pass

    @abstractmethod
    def get_semua_transaksi(self):
        pass

    @abstractmethod
    def get_transaksi(self, id_transaksi):
        pass


# Concrete Class yang mengimplementasikan BaseWarnet
class Warnet(BaseWarnet):
    def __init__(self, db_config):
        self._db_config = db_config

    # Helper untuk mendapatkan koneksi database
    def _get_connection(self):
        return pymysql.connect(
            host=self._db_config.MYSQL_HOST,
            port=self._db_config.MYSQL_PORT,
            user=self._db_config.MYSQL_USER,
            password=self._db_config.MYSQL_PASSWORD,
            database=self._db_config.MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor
        )

    # === MANAJEMEN KOMPUTER ===
    def get_semua_komputer(self):
        connection = self._get_connection()
        komputer_list = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nomor_pc, nama_pc, status FROM komputer ORDER BY nomor_pc ASC")
                results = cursor.fetchall()
                for row in results:
                    komputer = Komputer(row['id'], row['nomor_pc'], row['nama_pc'], row['status'])
                    komputer_list.append(komputer)
        finally:
            connection.close()
        return komputer_list

    def get_komputer(self, id_komputer):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nomor_pc, nama_pc, status FROM komputer WHERE id = %s", (id_komputer,))
                row = cursor.fetchone()
                if row:
                    return Komputer(row['id'], row['nomor_pc'], row['nama_pc'], row['status'])
        finally:
            connection.close()
        return None

    def tambah_komputer(self, nomor_pc, nama_pc):
        connection = self._get_connection()
        try:
            # Validasi input melalui pembuatan object dummy temporer
            temp_pc = Komputer(None, nomor_pc, nama_pc)
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO komputer (nomor_pc, nama_pc, status) VALUES (%s, %s, 'Tersedia')",
                    (temp_pc.nomor_pc, temp_pc.nama_pc)
                )
                connection.commit()
        finally:
            connection.close()

    def edit_komputer(self, id_komputer, nomor_pc, nama_pc, status):
        connection = self._get_connection()
        try:
            # OOP validation
            pc = self.get_komputer(id_komputer)
            if not pc:
                raise ValueError("Komputer tidak ditemukan")
            
            pc.nomor_pc = nomor_pc
            pc.nama_pc = nama_pc
            pc.ubah_status(status)

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE komputer SET nomor_pc = %s, nama_pc = %s, status = %s WHERE id = %s",
                    (pc.nomor_pc, pc.nama_pc, pc.status, pc.id)
                )
                connection.commit()
        finally:
            connection.close()

    def hapus_komputer(self, id_komputer):
        connection = self._get_connection()
        try:
            pc = self.get_komputer(id_komputer)
            if not pc:
                raise ValueError("Komputer tidak ditemukan")
            if pc.status == "Digunakan":
                raise ValueError("Komputer sedang aktif digunakan, tidak dapat dihapus")

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM komputer WHERE id = %s", (id_komputer,))
                connection.commit()
        finally:
            connection.close()

    # === MANAJEMEN PELANGGAN ===
    def get_semua_pelanggan(self):
        connection = self._get_connection()
        pelanggan_list = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nama_pelanggan, nomor_pelanggan, jenis_pelanggan FROM pelanggan ORDER BY nama_pelanggan ASC")
                results = cursor.fetchall()
                for row in results:
                    if row['jenis_pelanggan'] == 'Member':
                        plg = Member(row['id'], row['nama_pelanggan'], row['nomor_pelanggan'])
                    else:
                        plg = Pelanggan(row['id'], row['nama_pelanggan'], row['nomor_pelanggan'])
                    pelanggan_list.append(plg)
        finally:
            connection.close()
        return pelanggan_list

    def get_pelanggan(self, id_pelanggan):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nama_pelanggan, nomor_pelanggan, jenis_pelanggan FROM pelanggan WHERE id = %s", (id_pelanggan,))
                row = cursor.fetchone()
                if row:
                    if row['jenis_pelanggan'] == 'Member':
                        return Member(row['id'], row['nama_pelanggan'], row['nomor_pelanggan'])
                    else:
                        return Pelanggan(row['id'], row['nama_pelanggan'], row['nomor_pelanggan'])
        finally:
            connection.close()
        return None

    def tambah_pelanggan(self, nama_pelanggan, nomor_pelanggan, jenis_pelanggan):
        connection = self._get_connection()
        try:
            # OOP validation (Polymorphism & Class creation test)
            if jenis_pelanggan == 'Member':
                temp_plg = Member(None, nama_pelanggan, nomor_pelanggan)
            else:
                temp_plg = Pelanggan(None, nama_pelanggan, nomor_pelanggan)

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO pelanggan (nama_pelanggan, nomor_pelanggan, jenis_pelanggan) VALUES (%s, %s, %s)",
                    (temp_plg.nama_pelanggan, temp_plg.nomor_pelanggan, temp_plg.jenis_pelanggan)
                )
                connection.commit()
        finally:
            connection.close()

    def edit_pelanggan(self, id_pelanggan, nama_pelanggan, nomor_pelanggan, jenis_pelanggan):
        connection = self._get_connection()
        try:
            plg = self.get_pelanggan(id_pelanggan)
            if not plg:
                raise ValueError("Pelanggan tidak ditemukan")
            
            plg.nama_pelanggan = nama_pelanggan
            plg.nomor_pelanggan = nomor_pelanggan

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE pelanggan SET nama_pelanggan = %s, nomor_pelanggan = %s, jenis_pelanggan = %s WHERE id = %s",
                    (plg.nama_pelanggan, plg.nomor_pelanggan, jenis_pelanggan, id_pelanggan)
                )
                connection.commit()
        finally:
            connection.close()

    def hapus_pelanggan(self, id_pelanggan):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                # Periksa apakah ada transaksi aktif untuk pelanggan ini
                cursor.execute("SELECT id FROM transaksi WHERE id_pelanggan = %s AND status = 'Aktif'", (id_pelanggan,))
                if cursor.fetchone():
                    raise ValueError("Pelanggan sedang memiliki sesi sewa aktif, tidak dapat dihapus")

                cursor.execute("DELETE FROM pelanggan WHERE id = %s", (id_pelanggan,))
                connection.commit()
        finally:
            connection.close()

    # === MANAJEMEN PENYEWAAN & TRANSAKSI ===
    def sewa_komputer(self, id_pelanggan, id_komputer, durasi):
        connection = self._get_connection()
        try:
            # 1. Ambil objek pelanggan dan komputer
            pelanggan = self.get_pelanggan(id_pelanggan)
            if not pelanggan:
                raise ValueError("Pelanggan tidak ditemukan")

            komputer = self.get_komputer(id_komputer)
            if not komputer:
                raise ValueError("Komputer tidak ditemukan")

            # 2. Periksa ketersediaan komputer
            if komputer.status == "Digunakan":
                raise ValueError("Komputer sedang digunakan oleh pelanggan lain")

            # 3. Hitung biaya menggunakan Polymorphism
            total_biaya = pelanggan.hitung_biaya(durasi)
            tarif_per_jam = pelanggan.tarif_per_jam

            # 4. Ubah status komputer (OOP)
            komputer.ubah_status("Digunakan")

            # 5. Jalankan transaksi database
            with connection.cursor() as cursor:
                connection.begin()

                # Simpan transaksi baru
                cursor.execute(
                    """INSERT INTO transaksi (id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, status)
                       VALUES (%s, %s, %s, %s, %s, 'Aktif')""",
                    (pelanggan.id, komputer.id, durasi, tarif_per_jam, total_biaya)
                )

                # Update status komputer di database
                cursor.execute(
                    "UPDATE komputer SET status = 'Digunakan' WHERE id = %s",
                    (komputer.id,)
                )

                connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

    def selesaikan_sewa(self, id_transaksi):
        # 1. Ambil objek transaksi
        transaksi = self.get_transaksi(id_transaksi)
        if not transaksi:
            raise ValueError("Transaksi tidak ditemukan")

        # 2. Selesaikan sewa secara OOP (ini mengubah status transaksi & komputer asosiasi)
        transaksi.selesaikan()

        # 3. Update status ke database
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                connection.begin()

                cursor.execute(
                    "UPDATE transaksi SET status = 'Selesai' WHERE id = %s",
                    (transaksi.id,)
                )

                cursor.execute(
                    "UPDATE komputer SET status = 'Tersedia' WHERE id = %s",
                    (transaksi.komputer.id,)
                )

                connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

    def get_semua_transaksi(self):
        connection = self._get_connection()
        transaksi_list = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi, status 
                    FROM transaksi ORDER BY waktu_transaksi DESC
                """)
                results = cursor.fetchall()
                for row in results:
                    pelanggan = self.get_pelanggan(row['id_pelanggan'])
                    komputer = self.get_komputer(row['id_komputer'])
                    trx = Transaksi(
                        row['id'],
                        pelanggan,
                        komputer,
                        row['durasi'],
                        row['tarif_per_jam'],
                        row['total_biaya'],
                        row['waktu_transaksi'],
                        row['status']
                    )
                    transaksi_list.append(trx)
        finally:
            connection.close()
        return transaksi_list

    def get_transaksi(self, id_transaksi):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi, status 
                    FROM transaksi WHERE id = %s
                """, (id_transaksi,))
                row = cursor.fetchone()
                if row:
                    pelanggan = self.get_pelanggan(row['id_pelanggan'])
                    komputer = self.get_komputer(row['id_komputer'])
                    return Transaksi(
                        row['id'],
                        pelanggan,
                        komputer,
                        row['durasi'],
                        row['tarif_per_jam'],
                        row['total_biaya'],
                        row['waktu_transaksi'],
                        row['status']
                    )
        finally:
            connection.close()
        return None

    def get_transaksi_terbaru(self, limit=5):
        connection = self._get_connection()
        transaksi_list = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi, status 
                    FROM transaksi ORDER BY waktu_transaksi DESC LIMIT %s
                """, (limit,))
                results = cursor.fetchall()
                for row in results:
                    pelanggan = self.get_pelanggan(row['id_pelanggan'])
                    komputer = self.get_komputer(row['id_komputer'])
                    trx = Transaksi(
                        row['id'],
                        pelanggan,
                        komputer,
                        row['durasi'],
                        row['tarif_per_jam'],
                        row['total_biaya'],
                        row['waktu_transaksi'],
                        row['status']
                    )
                    transaksi_list.append(trx)
        finally:
            connection.close()
        return transaksi_list

    # === STATISTIK & LAPORAN ===
    def get_statistik(self):
        connection = self._get_connection()
        stats = {}
        try:
            with connection.cursor() as cursor:
                # 1. Total Komputer
                cursor.execute("SELECT COUNT(*) as total FROM komputer")
                stats['total_komputer'] = cursor.fetchone()['total']

                # 2. Komputer Tersedia
                cursor.execute("SELECT COUNT(*) as total FROM komputer WHERE status = 'Tersedia'")
                stats['komputer_tersedia'] = cursor.fetchone()['total']

                # 3. Komputer Sedang Digunakan
                cursor.execute("SELECT COUNT(*) as total FROM komputer WHERE status = 'Digunakan'")
                stats['komputer_digunakan'] = cursor.fetchone()['total']

                # 4. Total Pelanggan
                cursor.execute("SELECT COUNT(*) as total FROM pelanggan")
                stats['total_pelanggan'] = cursor.fetchone()['total']

                # 5. Total Transaksi
                cursor.execute("SELECT COUNT(*) as total FROM transaksi")
                stats['total_transaksi'] = cursor.fetchone()['total']

                # 6. Pendapatan Hari Ini
                cursor.execute("""
                    SELECT COALESCE(SUM(total_biaya), 0) as total 
                    FROM transaksi 
                    WHERE DATE(waktu_transaksi) = CURDATE()
                """)
                stats['pendapatan_hari_ini'] = float(cursor.fetchone()['total'])

                # 7. Pendapatan Keseluruhan
                cursor.execute("SELECT COALESCE(SUM(total_biaya), 0) as total FROM transaksi")
                stats['pendapatan_keseluruhan'] = float(cursor.fetchone()['total'])
        finally:
            connection.close()
        return stats

    def get_laporan_pendapatan(self, start_date=None, end_date=None):
        connection = self._get_connection()
        laporan = {
            'total_pendapatan': 0.0,
            'jumlah_transaksi': 0,
            'riwayat': []
        }
        try:
            with connection.cursor() as cursor:
                # Query filter tanggal
                where_clause = ""
                params = []
                if start_date and end_date:
                    where_clause = "WHERE DATE(waktu_transaksi) BETWEEN %s AND %s"
                    params = [start_date, end_date]
                elif start_date:
                    where_clause = "WHERE DATE(waktu_transaksi) >= %s"
                    params = [start_date]
                elif end_date:
                    where_clause = "WHERE DATE(waktu_transaksi) <= %s"
                    params = [end_date]

                # Hitung summary
                sql_summary = f"""
                    SELECT COALESCE(SUM(total_biaya), 0) as total_biaya, COUNT(*) as jumlah_transaksi 
                    FROM transaksi {where_clause}
                """
                cursor.execute(sql_summary, params)
                summary = cursor.fetchone()
                laporan['total_pendapatan'] = float(summary['total_biaya'])
                laporan['jumlah_transaksi'] = summary['jumlah_transaksi']

                # Riwayat per hari untuk Chart.js
                sql_riwayat = f"""
                    SELECT DATE(waktu_transaksi) as tanggal, COALESCE(SUM(total_biaya), 0) as pendapatan
                    FROM transaksi
                    {where_clause}
                    GROUP BY DATE(waktu_transaksi)
                    ORDER BY DATE(waktu_transaksi) ASC
                """
                cursor.execute(sql_riwayat, params)
                results = cursor.fetchall()
                for row in results:
                    laporan['riwayat'].append({
                        'tanggal': row['tanggal'].strftime('%Y-%m-%d') if isinstance(row['tanggal'], datetime) or hasattr(row['tanggal'], 'strftime') else str(row['tanggal']),
                        'pendapatan': float(row['pendapatan'])
                    })
        finally:
            connection.close()
        return laporan
