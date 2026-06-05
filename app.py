"""
SmartBudget AI — Aplikasi Manajemen Keuangan Mahasiswa
Entry point utama aplikasi Streamlit
"""

import streamlit as st
from utils.data_utils import init_session_state, load_transactions

# ─── Konfigurasi Halaman ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartBudget AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Inisialisasi Session State ────────────────────────────────────────────────
init_session_state()

# ─── Custom CSS Global ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Sidebar styling */
    .css-1d391kg { padding-top: 1rem; }

    /* Metric card styling */
    [data-testid="metric-container"] {
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        border-radius: 12px;
        padding: 1rem;
    }

    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Hide default Streamlit menu (opsional) */
    /* #MainMenu {visibility: hidden;} */
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Global ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💰 SmartBudget AI")
    st.markdown("*Kelola keuangan mahasiswamu dengan cerdas*")
    st.divider()

    # Info user / saldo ringkas
    transactions = load_transactions()
    if not transactions.empty:
        total_pemasukan = transactions[transactions["tipe"] == "Pemasukan"]["jumlah"].sum()
        total_pengeluaran = transactions[transactions["tipe"] == "Pengeluaran"]["jumlah"].sum()
        saldo = total_pemasukan - total_pengeluaran

        saldo_color = "green" if saldo >= 0 else "red"
        st.markdown(f"**Saldo saat ini:**")
        st.markdown(f"<h3 style='color:{saldo_color}'>Rp {saldo:,.0f}</h3>", unsafe_allow_html=True)
        st.caption(f"📥 Pemasukan: Rp {total_pemasukan:,.0f}")
        st.caption(f"📤 Pengeluaran: Rp {total_pengeluaran:,.0f}")
    else:
        st.info("Belum ada transaksi. Mulai catat di **Input Transaksi**!")

    st.divider()
    st.caption("SmartBudget AI v1.0")
    st.caption("Studi Independen Data Science — PT Celerates")

# ─── Halaman Home (Landing) ────────────────────────────────────────────────────
st.title("🏠 Selamat Datang di SmartBudget AI")
st.markdown("""
> **Aplikasi manajemen keuangan cerdas untuk mahasiswa** — powered by Machine Learning & Generative AI
""")

st.divider()

# ─── Quick Stats ───────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

transactions = load_transactions()

with col1:
    total_tx = len(transactions)
    st.metric("📋 Total Transaksi", total_tx)

with col2:
    if not transactions.empty:
        pemasukan = transactions[transactions["tipe"] == "Pemasukan"]["jumlah"].sum()
    else:
        pemasukan = 0
    st.metric("📥 Total Pemasukan", f"Rp {pemasukan:,.0f}")

with col3:
    if not transactions.empty:
        pengeluaran = transactions[transactions["tipe"] == "Pengeluaran"]["jumlah"].sum()
    else:
        pengeluaran = 0
    st.metric("📤 Total Pengeluaran", f"Rp {pengeluaran:,.0f}")

with col4:
    saldo = pemasukan - pengeluaran
    delta_color = "normal" if saldo >= 0 else "inverse"
    st.metric("💳 Saldo", f"Rp {saldo:,.0f}", delta=None)

st.divider()

# ─── Fitur Cards ───────────────────────────────────────────────────────────────
st.subheader("🚀 Fitur Utama")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 📊 Dashboard & Analisis
    Visualisasi pola pengeluaran dengan grafik interaktif.  
    Pantau tren keuanganmu secara real-time.
    """)
    st.page_link("pages/1_Dashboard.py", label="Buka Dashboard →", icon="📊")

with col2:
    st.markdown("""
    #### 🔮 Prediksi Keuangan
    Model ML memprediksi kondisi keuanganmu ke depan  
    berdasarkan pola historis transaksi.
    """)
    st.page_link("pages/4_Prediksi.py", label="Lihat Prediksi →", icon="🔮")

with col3:
    st.markdown("""
    #### 💬 AI Advisor
    Chatbot AI yang menganalisis transaksimu  
    dan memberikan rekomendasi keuangan personal.
    """)
    st.page_link("pages/5_AI_Advisor.py", label="Tanya AI →", icon="💬")

st.divider()

# ─── Getting Started ───────────────────────────────────────────────────────────
if transactions.empty:
    st.subheader("⚡ Mulai Sekarang")
    st.markdown("""
    1. **Input Transaksi** — Catat pemasukan & pengeluaranmu
    2. **Dashboard** — Lihat visualisasi pola keuanganmu
    3. **Analisis** — Breakdown kategori pengeluaran
    4. **Prediksi** — Proyeksi keuangan ke depan
    5. **AI Advisor** — Minta rekomendasi dari AI
    """)
    st.page_link("pages/2_Input_Transaksi.py", label="➕ Mulai Catat Transaksi", icon="➕")
