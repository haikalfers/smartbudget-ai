# models/train_classifier.py

import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

print("⏳ Memuat dataset training...")
df = pd.read_csv("data/training_klasifikasi.csv")

X = df["deskripsi"]
y = df["kategori"]

# Split data training & testing (80:20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Pipeline: TF-IDF → Logistic Regression
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),   # unigram + bigram
        max_features=5000,
        sublinear_tf=True
    )),
    ("clf", LogisticRegression(
        max_iter=1000,
        C=1.0,
        random_state=42
    ))
])

print("⏳ Training model klasifikasi...")
pipeline.fit(X_train, y_train)

# Evaluasi
y_pred = pipeline.predict(X_test)
akurasi = accuracy_score(y_test, y_pred)

print(f"\n✅ Training selesai!")
print(f"📊 Akurasi model : {akurasi:.2%}")
print(f"\nDetail per kategori:")
print(classification_report(y_test, y_pred))

# Simpan model
joblib.dump(pipeline, "models/classifier.pkl")
print("✅ Model disimpan ke models/classifier.pkl")

# Test prediksi manual
print("\n🧪 Test prediksi manual:")
test_cases = [
    "beli nasi goreng",
    "naik grab ke kampus",
    "bayar kos bulan ini",
    "beli obat batuk",
    "nonton netflix",
    "beli buku statistika"
]
for teks in test_cases:
    prediksi = pipeline.predict([teks])[0]
    print(f"  '{teks}' → {prediksi}")