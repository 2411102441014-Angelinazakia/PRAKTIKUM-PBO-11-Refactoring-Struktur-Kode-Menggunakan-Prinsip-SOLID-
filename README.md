# PRAKTIKUM-PBO-11-Refactoring-Struktur-Kode-Menggunakan-Prinsip-SOLID-
1. Pelanggaran Single Responsibility Principle (SRP)
Identifikasi: Kelas memiliki tanggung jawab gabungan. Contohnya, sebuah OrderManager menangani pengaturan item, memproses pembayaran, dan mengirim notifikasi sekaligus.
Penjelasan Pelanggaran: SRP menyatakan bahwa sebuah kelas harus memiliki satu, dan hanya satu, alasan untuk berubah. Kelas yang bermasalah harus dimodifikasi jika ada perubahan pada sistem pembayaran atau jika ada perubahan pada logika notifikasi. Memiliki lebih dari satu alasan untuk diubah secara otomatis melanggar prinsip ini.

2. Pelanggaran Open/Closed Principle (OCP)
IdentifIkasi: Logika fungsional diatur menggunakan struktur kondisional if/elif hardcoded untuk memilih implementasi (misalnya, pembayaran kredit atau transfer bank).
Penjelasan Pelanggaran: OCP menuntut kelas harus terbuka untuk ekstensi (penambahan fitur baru) tetapi tertutup untuk modifikasi (tidak perlu mengubah kode yang sudah ada). Ketika metode pembayaran baru ditambahkan, programmer dipaksa untuk mengubah kode sumber kelas inti tersebut, menambahkan branch elif baru. Ini membuat kelas tidak "tertutup untuk modifikasi," melanggar OCP.


3. Pelanggaran Dependency Inversion Principle (DIP)
Identifikasi: Modul tingkat tinggi (logika bisnis utama) bergantung pada implementasi detail tingkat rendah yang konkret.
Penjelasan Pelanggaran: DIP menyatakan bahwa modul high-level harus bergantung pada Abstraksi (Kontrak), bukan pada Implementasi Konkret (detail low-level). Kelas yang bermasalah secara langsung memanggil dan mengandung detail implementasi pembayaran tertentu. Ini membuat kelas terikat erat (tightly coupled) pada detail tersebut. Jika detail implementasi berubah, kelas inti harus diubah, menunjukkan adanya ketergantungan pada konkret, bukan pada Abstraksi.
