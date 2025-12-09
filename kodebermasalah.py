from abc import ABC, abstractmethod
from dataclasses import dataclass

# Model Sederhana
@dataclass
class Order:
    customer_name: str
    total_price: float
    status: str = "open"

# === KODE BURUK (SEBELUM REFACTOR)
class OrderManager: # Melanggar SRP, OCP, DIP [cite: 47]
    def process_checkout(self, order: Order, payment_method: str):
        print(f"Memulai checkout untuk {order.customer_name}...")
        
        # LOGIKA PEMBAYARAN (Pelanggaran OCP/DIP) [cite: 84]
        if payment_method == "credit_card":
            # Logika detail implementasi hardcoded di sini [cite: 86]
            print("Processing Credit Card...")
        elif payment_method == "bank_transfer":
            # Logika detail implementasi hardcoded di sini [cite: 89]
            print("Processing Bank Transfer...")
        else:
            print("Metode tidak valid.")
            return False

        # LOGIKA NOTIFIKASI (Pelanggaran SRP) [cite: 93]
        print(f"Mengirim notifikasi ke {order.customer_name}...")
        order.status = "paid"
        return True
    

# --- ABSTRAKSI (Kontrak untuk OCP/DIP) [cite: 105]
class IPaymentProcessor(ABC):
    """Kontrak: Semua prosesor pembayaran harus punya method 'process'."""
    @abstractmethod
    def process(self, order: Order) -> bool:
        pass

class INotificationService(ABC):
    """Kontrak: Semua layanan notifikasi harus punya method 'send'."""
    @abstractmethod
    def send(self, order: Order):
        pass

# --- IMPLEMENTASI KONKRIT (Plug-in)
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        print("Payment: Memproses Kartu Kredit.")
        return True

class EmailNotifier(INotificationService):
    def send(self, order: Order):
        print(f"Notif: Mengirim email konfirmasi ke {order.customer_name}.")

# --- KELAS KOORDINATOR (SRP & DIP)
class CheckoutService: # Tanggung jawab tunggal: Mengkoordinasi Checkout [cite: 121]
    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        # Dependency Injection (DIP): Bergantung pada Abstraksi, bukan Konkrit [cite: 150]
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order):
        payment_success = self.payment_processor.process(order) # Delegasi 1 [cite: 154]
        if payment_success:
            order.status = "paid"
            self.notifier.send(order) # Delegasi 2 [cite: 157]
            print("Checkout Sukses.")
            return True
        return False
    

    # PROGRAM UTAMA [cite: 162]
andi_order = Order("Andi", 500000)
email_service = EmailNotifier()

# Setup Dependencies [cite: 166]

# 1. Inject implementasi Credit Card [cite: 188]
cc_processor = CreditCardProcessor()
checkout_cc = CheckoutService(payment_processor=cc_processor, notifier=email_service)
print("- Skenario 1: Credit Card ---")
checkout_cc.run_checkout(andi_order)

# 2. Pembuktian OCP: Menambah Metode Pembayaran QRIS (Tanpa Mengubah Checkout Service) [cite: 192]
class QrisProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        print("Payment: Memproses QRIS.")
        return True

budi_order = Order("Budi", 100000)
qris_processor = QrisProcessor()

# Inject implementasi QRIS yang baru dibuat [cite: 196]
checkout_qris = CheckoutService(payment_processor=qris_processor, notifier=email_service)
print("\n- Skenario 2: Pembuktian OCP (QRIS) ---")
checkout_qris.run_checkout(budi_order)