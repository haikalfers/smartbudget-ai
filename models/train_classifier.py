# models/train_classifier.py

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd

# Data training sederhana — bisa diperluas
training_data = [
    # Makan
    ("beli nasi padang", "Makan"),
    ("makan siang warteg", "Makan"),
    ("beli kopi", "Makan"),
    ("beli mie instan", "Makan"),
    ("beli snack", "Makan"),
    ("jajan gorengan", "Makan"),
    # Transport
    ("naik gojek", "Transport"),
    ("grab motor", "Transport"),
    ("bayar bensin", "Transport"),
    ("naik bus", "Transport"),
    ("isi bensin motor", "Transport"),
    # Pendidikan
    ("beli buku", "Pendidikan"),
    ("bayar spp", "Pendidikan"),
    ("beli alat tulis", "Pendidikan"),
    ("print tugas", "Pendidikan"),
    ("beli kuota belajar", "Pendidikan"),
    # Hiburan
    ("nonton bioskop", "Hiburan"),
    ("beli game", "Hiburan"),
    ("spotify", "Hiburan"),
    ("netflix", "Hiburan"),
    ("karaoke", "Hiburan"),
    # Kesehatan
    ("beli obat", "Kesehatan"),
    ("bayar dokter", "Kesehatan"),
    ("beli vitamin", "Kesehatan"),
    ("apotek", "Kesehatan"),
    # Belanja
    ("beli baju", "Belanja"),
    ("beli sepatu", "Belanja"),
    ("shopee", "Belanja"),
    ("tokopedia", "Belanja"),
    # Tagihan
    ("bayar listrik", "Tagihan"),
    ("bayar wifi", "Tagihan"),
    ("bayar kos", "Tagihan"),
    ("bayar air", "Tagihan"),
]

df = pd.DataFrame(training_data, columns=["deskripsi", "kategori"])

# Buat pipeline ML
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("clf", LogisticRegression(max_iter=1000))
])

pipeline.fit(df["deskripsi"], df["kategori"])

# Simpan model
joblib.dump(pipeline, "models/classifier.pkl")
print("✅ Model klasifikasi berhasil disimpan!")