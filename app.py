import streamlit as st

st.set_page_config(
    page_title="SmartBudget AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💰 SmartBudget AI")
st.subheader("Asisten Keuangan Cerdas untuk Mahasiswa")

st.markdown("""
Selamat datang di **SmartBudget AI**! Gunakan menu di sidebar untuk:

- 📊 Melihat **Dashboard** keuanganmu
- ➕ **Input Transaksi** harian
- 📈 Melihat **Analisis** pola pengeluaran
- 🔮 Cek **Prediksi** keuangan ke depan
- 💬 Tanya **AI Advisor** untuk rekomendasi
""")