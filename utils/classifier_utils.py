# utils/classifier_utils.py

import streamlit as st

# Cache hasil klasifikasi supaya kata yang sama
# tidak memanggil API berulang kali
@st.cache_data(ttl=3600)
def classify_expense(description: str) -> str:
    """
    Klasifikasi dengan cache — deskripsi yang sama
    tidak akan memanggil API lagi selama 1 jam.
    """
    from utils.llm_utils import get_llm_response
    
    system = """Kamu adalah classifier pengeluaran mahasiswa.
Klasifikasikan ke salah satu kategori ini SAJA:
Makan, Transport, Pendidikan, Hiburan, Kesehatan, Belanja, Tagihan, Lainnya.
Jawab dengan 1 kata kategori saja, tanpa penjelasan."""
    
    result = get_llm_response(description, system_prompt=system)
    return result.strip()