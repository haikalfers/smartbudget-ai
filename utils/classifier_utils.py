# utils/classifier_utils.py

import joblib
import os
import streamlit as st

@st.cache_resource
def load_classifier():
    """Load model classifier — di-cache supaya tidak reload tiap interaksi"""
    model_path = "models/classifier.pkl"
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            "Model classifier belum ada. "
            "Jalankan dulu: python models/train_classifier.py"
        )
    return joblib.load(model_path)

def predict_category(deskripsi: str) -> str:
    """Prediksi kategori dari deskripsi transaksi"""
    model = load_classifier()
    return model.predict([deskripsi.lower()])[0]

def predict_category_batch(deskripsi_list: list) -> list:
    """Prediksi kategori untuk banyak transaksi sekaligus"""
    model = load_classifier()
    return model.predict([d.lower() for d in deskripsi_list]).tolist()


# ─── Alias dan helper untuk backward compatibility ────────────────────────────
klasifikasi_teks = predict_category  # Alias untuk nama fungsi lama


def is_classifier_ready() -> bool:
    """Cek apakah model classifier sudah siap digunakan."""
    model_path = "models/classifier.pkl"
    if not os.path.exists(model_path):
        return False
    try:
        load_classifier()
        return True
    except Exception:
        return False