class Komputer:
    def __init__(self, id_komputer, nomor_pc, nama_pc, status="Tersedia"):
        self._id = id_komputer
        self._nomor_pc = nomor_pc
        self._nama_pc = nama_pc
        self._status = status

    # Getter untuk id
    @property
    def id(self):
        return self._id

    # Getter dan Setter untuk nomor_pc
    @property
    def nomor_pc(self):
        return self._nomor_pc

    @nomor_pc.setter
    def nomor_pc(self, value):
        if not value:
            raise ValueError("Nomor PC tidak boleh kosong")
        self._nomor_pc = value

    # Getter dan Setter untuk nama_pc
    @property
    def nama_pc(self):
        return self._nama_pc

    @nama_pc.setter
    def nama_pc(self, value):
        if not value:
            raise ValueError("Nama PC tidak boleh kosong")
        self._nama_pc = value

    # Getter untuk status
    @property
    def status(self):
        return self._status

    # Method untuk mengubah status komputer (Encapsulation)
    def ubah_status(self, status_baru):
        if status_baru in ["Tersedia", "Digunakan"]:
            self._status = status_baru
        else:
            raise ValueError("Status komputer harus 'Tersedia' atau 'Digunakan'")
