from abc import ABC, abstractmethod
from typing import List, Any
from dataclasses import dataclass

# Asumsi Model Data
@dataclass
class RegistrationData:
    student_name: str
    sks_count: int
    has_prerequisite: bool
    # Tambahan untuk challenge
    is_schedule_clash: bool

# --- LANGKAH 2: Implementasi DIP/OCP (Abstraksi dan Konkret) ---

# Abstraksi (IValidationRule)
class IValidationRule(ABC):
    @abstractmethod
    def validate(self, data: RegistrationData) -> bool:
        """Mengembalikan True jika valid, False jika tidak valid."""
        pass

# Implementasi Konkret 1
class SksLimitRule(IValidationRule):
    def validate(self, data: RegistrationData) -> bool:
        if data.sks_count > 24:
            print(f"Validasi SKS Gagal: {data.student_name} melebihi 24 SKS.")
            return False
        print(f"Validasi SKS Sukses: {data.student_name} SKS aman.")
        return True

# Implementasi Konkret 2
class PrerequisiteRule(IValidationRule):
    def validate(self, data: RegistrationData) -> bool:
        if not data.has_prerequisite:
            print(f"Validasi Prasyarat Gagal: {data.student_name} belum memenuhi prasyarat.")
            return False
        print(f"Validasi Prasyarat Sukses: {data.student_name} memenuhi prasyarat.")
        return True

# --- LANGKAH 3: Implementasi SRP (Kelas Koordinator) ---

class RegistrationService: # Tanggung jawab tunggal: Menjalankan validasi
    # Menerima daftar IValidationRule via Dependency Injection 
    def __init__(self, validation_rules: List[IValidationRule]):
        self.rules = validation_rules

    def register_student(self, data: RegistrationData) -> bool:
        print(f"\n--- Memulai Registrasi untuk {data.student_name} ---")
        for rule in self.rules:
            if not rule.validate(data):
                print(f"Registrasi Gagal untuk {data.student_name}.")
                return False
        
        print(f"Registrasi Sukses untuk {data.student_name}!")
        return True

# --- LANGKAH 4: Challenge Pembuktian OCP (Menambah Rule Baru) ---

# Implementasi Konkret 3 (BARU)
class JadwalBentrokRule(IValidationRule): # Dibuat tanpa mengubah RegistrationService
    def validate(self, data: RegistrationData) -> bool:
        if data.is_schedule_clash:
            print(f"Validasi Jadwal Bentrok Gagal: {data.student_name} memiliki jadwal bentrok.")
            return False
        print(f"Validasi Jadwal Bentrok Sukses: {data.student_name} jadwal aman.")
        return True

# PROGRAM UTAMA: Eksekusi dan Pembuktian OCP
# Data Mahasiswa
mahasiswa_valid = RegistrationData("Angel", 22, True, False) # Harusnya Sukses
mahasiswa_gagal_sks = RegistrationData("Jennie", 25, True, False) # Gagal SKS
mahasiswa_gagal_jadwal = RegistrationData("Cici", 20, True, True) # Gagal Jadwal

# Setup Dependencies (Aturan Validasi)
# Kita membuat daftar aturan DAN MENYUNTIKKAN JadwalBentrokRule (Pembuktian OCP)
all_rules: List[IValidationRule] = [
    SksLimitRule(),
    PrerequisiteRule(),
    JadwalBentrokRule() # Disuntikkan TANPA mengubah class RegistrationService 
]

# Inisiasi Service dengan Rules
service = RegistrationService(all_rules)

# Jalankan Skenario
service.register_student(mahasiswa_valid)
service.register_student(mahasiswa_gagal_sks)
service.register_student(mahasiswa_gagal_jadwal)