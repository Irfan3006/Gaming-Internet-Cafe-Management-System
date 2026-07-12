class Pelanggan:
    def __init__(self, id_pelanggan, nama_pelanggan, nomor_pelanggan):
        self._id = id_pelanggan
        self._nama_pelanggan = nama_pelanggan
        self._nomor_pelanggan = nomor_pelanggan

    # Getter untuk id
    @property
    def id(self):
        return self._id

    # Getter dan Setter untuk nama_pelanggan
    @property
    def nama_pelanggan(self):
        return self._nama_pelanggan

    @nama_pelanggan.setter
    def nama_pelanggan(self, value):
        if not value:
            raise ValueError("Nama pelanggan tidak boleh kosong")
        self._nama_pelanggan = value

    # Getter dan Setter untuk nomor_pelanggan
    @property
    def nomor_pelanggan(self):
        return self._nomor_pelanggan

    @nomor_pelanggan.setter
    def nomor_pelanggan(self, value):
        if not value:
            raise ValueError("Nomor pelanggan tidak boleh kosong")
        self._nomor_pelanggan = value

    # Getter untuk jenis_pelanggan (Biasa)
    @property
    def jenis_pelanggan(self):
        return "Biasa"

    # Getter untuk tarif per jam
    @property
    def tarif_per_jam(self):
        return 5000.0

    # Method Polymorphism untuk menghitung biaya sewa (biasa: 5000/jam)
    def hitung_biaya(self, durasi):
        if durasi <= 0:
            raise ValueError("Durasi harus lebih dari 0 jam")
        return durasi * self.tarif_per_jam


# Inheritance: Member mewarisi Pelanggan
class Member(Pelanggan):
    
    # Getter Override untuk jenis_pelanggan (Member)
    @property
    def jenis_pelanggan(self):
        return "Member"

    # Getter Override untuk tarif per jam
    @property
    def tarif_per_jam(self):
        return 4500.0

    # Polymorphism: Meng-override method hitung_biaya (member: 4500/jam)
    def hitung_biaya(self, durasi):
        if durasi <= 0:
            raise ValueError("Durasi harus lebih dari 0 jam")
        return durasi * self.tarif_per_jam
