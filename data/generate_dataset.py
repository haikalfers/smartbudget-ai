# data/generate_dataset.py

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

# ==============================================
# KONFIGURASI DATA
# ==============================================

KATEGORI_DATA = {
    "Makan": {
        "deskripsi": [
            "beli nasi padang", "makan siang warteg", "beli kopi susu",
            "beli mie ayam", "jajan gorengan", "beli nasi goreng",
            "makan di kantin", "beli bubble tea", "beli indomie",
            "beli roti bakar", "sarapan nasi uduk", "beli bakso",
            "makan malam warung", "beli ayam geprek", "beli es teh",
            "beli jus buah", "makan di warteg", "beli sate",
            "beli pecel lele", "beli martabak"
        ],
        "range_harga": (8000, 45000),
        "frekuensi": 0.30  # 30% dari total transaksi
    },
    "Transport": {
        "deskripsi": [
            "naik gojek ke kampus", "grab motor ke mall",
            "bayar bensin motor", "naik bus trans",
            "isi bensin pertamax", "naik angkot",
            "gojek ke kos", "grab car ke stasiun",
            "naik kereta commuter", "bayar parkir motor",
            "grab motor ke rumah sakit", "naik ojek online",
            "beli token busway", "isi bensin pertalite"
        ],
        "range_harga": (5000, 80000),
        "frekuensi": 0.20
    },
    "Pendidikan": {
        "deskripsi": [
            "beli buku kuliah", "bayar spp semester",
            "print dan jilid laporan", "beli alat tulis",
            "beli kertas hvs", "fotokopi materi kuliah",
            "beli buku referensi", "bayar kursus online",
            "beli kuota internet belajar", "beli flashdisk",
            "print skripsi", "beli tinta printer",
            "bayar seminar", "beli jurnal ilmiah"
        ],
        "range_harga": (5000, 500000),
        "frekuensi": 0.12
    },
    "Hiburan": {
        "deskripsi": [
            "nonton bioskop", "beli game steam",
            "bayar spotify premium", "bayar netflix",
            "main bowling", "karaoke bersama teman",
            "beli komik", "bayar youtube premium",
            "main billiard", "beli tiket konser",
            "bayar disney plus", "main game arcade",
            "beli merchandise anime", "nonton film bioskop"
        ],
        "range_harga": (15000, 200000),
        "frekuensi": 0.10
    },
    "Kesehatan": {
        "deskripsi": [
            "beli obat flu di apotek", "bayar dokter umum",
            "beli vitamin c", "beli masker kesehatan",
            "bayar klinik gigi", "beli obat maag",
            "beli suplemen", "bayar puskesmas",
            "beli hand sanitizer", "beli paracetamol",
            "bayar konsultasi dokter", "beli minyak kayu putih"
        ],
        "range_harga": (10000, 200000),
        "frekuensi": 0.08
    },
    "Belanja": {
        "deskripsi": [
            "beli baju di shopee", "beli sepatu tokopedia",
            "beli celana jeans", "beli tas ransel",
            "beli aksesoris hp", "beli charger laptop",
            "beli sabun mandi", "beli shampo",
            "beli deterjen", "beli alat mandi",
            "beli baju olahraga", "beli sandal",
            "beli earphone", "beli powerbank"
        ],
        "range_harga": (20000, 400000),
        "frekuensi": 0.10
    },
    "Tagihan": {
        "deskripsi": [
            "bayar kos bulanan", "bayar listrik kos",
            "bayar wifi indihome", "bayar air pdam",
            "bayar cicilan hp", "isi pulsa telkomsel",
            "beli kuota xl", "bayar iuran kos",
            "bayar langganan aplikasi", "isi saldo e-money",
            "bayar kartu pelajar", "top up gopay"
        ],
        "range_harga": (20000, 800000),
        "frekuensi": 0.10
    }
}

PEMASUKAN_DATA = {
    "deskripsi": [
        "uang bulanan dari orang tua",
        "transfer beasiswa",
        "gaji part time",
        "uang saku tambahan",
        "bayaran freelance desain",
        "hasil jualan online",
        "transfer dari orang tua",
        "beasiswa prestasi",
        "honor mengajar les",
        "uang lembur kerja part time"
    ],
    "range_harga": (300000, 2000000)
}

# ==============================================
# FUNGSI GENERATE DATA
# ==============================================

def generate_tanggal(n_bulan=3):
    """Generate tanggal acak untuk n bulan terakhir"""
    tanggal_sekarang = datetime(2025, 5, 31)
    tanggal_mulai = tanggal_sekarang - timedelta(days=30 * n_bulan)
    selisih = (tanggal_sekarang - tanggal_mulai).days
    tanggal_acak = tanggal_mulai + timedelta(days=random.randint(0, selisih))
    return tanggal_acak.strftime("%Y-%m-%d")

def generate_transaksi_pengeluaran(n=600):
    """Generate data pengeluaran sintetik"""
    data = []
    
    # Hitung jumlah per kategori berdasarkan frekuensi
    kategori_list = list(KATEGORI_DATA.keys())
    frekuensi_list = [KATEGORI_DATA[k]["frekuensi"] for k in kategori_list]
    
    for _ in range(n):
        # Pilih kategori berdasarkan frekuensi
        kategori = random.choices(kategori_list, weights=frekuensi_list, k=1)[0]
        info = KATEGORI_DATA[kategori]
        
        deskripsi = random.choice(info["deskripsi"])
        jumlah = random.randint(*info["range_harga"])
        # Bulatkan ke ribuan
        jumlah = round(jumlah / 1000) * 1000
        tanggal = generate_tanggal(3)
        
        data.append({
            "tanggal": tanggal,
            "deskripsi": deskripsi,
            "jumlah": jumlah,
            "tipe": "Pengeluaran",
            "kategori": kategori
        })
    
    return data

def generate_pemasukan(n=15):
    """Generate data pemasukan sintetik"""
    data = []
    
    for _ in range(n):
        deskripsi = random.choice(PEMASUKAN_DATA["deskripsi"])
        jumlah = random.randint(*PEMASUKAN_DATA["range_harga"])
        jumlah = round(jumlah / 50000) * 50000
        tanggal = generate_tanggal(3)
        
        data.append({
            "tanggal": tanggal,
            "deskripsi": deskripsi,
            "jumlah": jumlah,
            "tipe": "Pemasukan",
            "kategori": "Pemasukan"
        })
    
    return data

# ==============================================
# GENERATE & SIMPAN
# ==============================================

print("⏳ Generating dataset...")

pengeluaran = generate_transaksi_pengeluaran(600)
pemasukan = generate_pemasukan(15)
semua_data = pengeluaran + pemasukan

df = pd.DataFrame(semua_data)
df["tanggal"] = pd.to_datetime(df["tanggal"])
df = df.sort_values("tanggal").reset_index(drop=True)

# Simpan dataset lengkap (untuk training model)
df.to_csv("data/dataset_transaksi.csv", index=False)
print(f"✅ dataset_transaksi.csv — {len(df)} baris")

# Simpan sample data (untuk demo aplikasi)
sample = df.sample(n=50, random_state=42).sort_values("tanggal")
sample.to_csv("data/sample_data.csv", index=False)
print(f"✅ sample_data.csv — {len(sample)} baris")

# Simpan khusus data training klasifikasi (pengeluaran saja)
df_training = df[df["tipe"] == "Pengeluaran"][["deskripsi", "kategori"]]
df_training.to_csv("data/training_klasifikasi.csv", index=False)
print(f"✅ training_klasifikasi.csv — {len(df_training)} baris")

# ==============================================
# PREVIEW & STATISTIK
# ==============================================

print("\n📊 Statistik Dataset:")
print(f"Total transaksi  : {len(df)}")
print(f"Total pengeluaran: {len(pengeluaran)}")
print(f"Total pemasukan  : {len(pemasukan)}")
print(f"\nDistribusi kategori pengeluaran:")
print(df[df["tipe"]=="Pengeluaran"]["kategori"].value_counts())
print(f"\nSample 5 baris pertama:")
print(df.head())