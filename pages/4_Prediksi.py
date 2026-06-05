"""
pages/4_Prediksi.py
Halaman Prediksi Keuangan menggunakan Prophet / Linear Regression.
👤 Dikerjakan oleh: Member 2

INSTRUKSI MEMBER 2:
- Isi bagian bertanda TODO di file ini
- Buat utils/predictor_utils.py untuk logika model
- Buat models/train_predictor.py untuk training
- Model tersimpan di models/predictor.pkl
- Deadline internal: 8 Juni
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.data_utils import (
    init_session_state,
    load_transactions,
    get_tren_bulanan,
    format_rupiah,
)

# ─── Setup ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Prediksi | SmartBudget AI", page_icon="🔮", layout="wide")
init_session_state()

st.title("🔮 Prediksi Keuangan")
st.markdown("Proyeksi kondisi keuanganmu ke depan berdasarkan pola historis.")

df = load_transactions()

if df.empty:
    st.warning("📭 Belum ada data transaksi. Minimal butuh data 1–2 bulan untuk prediksi akurat.")
    st.page_link("pages/2_Input_Transaksi.py", label="➕ Input Transaksi", icon="➕")
    st.stop()

# ─── Konfigurasi Prediksi ──────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    target = st.radio(
        "Prediksi apa?",
        ["Pengeluaran", "Pemasukan", "Saldo"],
        horizontal=True,
        help="Pilih variabel yang ingin diprediksi"
    )

with col2:
    horizon = st.slider(
        "Prediksi berapa bulan ke depan?",
        min_value=1, max_value=6, value=3
    )

st.divider()

# ─── Load Model & Prediksi ─────────────────────────────────────────────────────
# TODO Member 2: Import predictor_utils dan jalankan prediksi
# Contoh:
# from utils.predictor_utils import load_predictor, predict_future
# model = load_predictor()
# predictions = predict_future(df, model, horizon, target)

# ─── Placeholder (hapus setelah Member 2 selesai) ──────────────────────────────
st.info("⚙️ **Member 2:** Implementasikan model prediksi di bagian ini menggunakan `utils/predictor_utils.py`.")

# Tren historis (sudah bisa ditampilkan tanpa model)
st.subheader("📊 Data Historis")
tren_df = get_tren_bulanan(df)

if not tren_df.empty:
    col_hist = "pengeluaran" if target == "Pengeluaran" else ("pemasukan" if target == "Pemasukan" else "saldo")
    tren_df["bulan_str"] = tren_df["bulan"].astype(str)

    fig_hist = go.Figure()
    fig_hist.add_trace(go.Scatter(
        x=tren_df["bulan_str"],
        y=tren_df[col_hist],
        mode="lines+markers",
        name=f"Aktual {target}",
        line=dict(color="#6C63FF", width=2),
        marker=dict(size=8),
    ))
    fig_hist.update_layout(
        title=f"Historis {target} per Bulan",
        xaxis_title="Bulan",
        yaxis_title="Nominal (Rp)",
        hovermode="x",
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# ─── TODO Member 2: Tampilkan grafik prediksi di bawah ini ───────────────────
# Setelah model berjalan, tampilkan:
# 1. Grafik prediksi dengan confidence interval
# 2. Tabel prediksi per bulan
# 3. Insight: apakah keuangan akan surplus / defisit?
#
# Contoh struktur output yang diharapkan:
# predictions = pd.DataFrame({
#     "bulan": ["2025-04", "2025-05", "2025-06"],
#     "prediksi": [1200000, 1350000, 1100000],
#     "lower": [900000, 1000000, 800000],
#     "upper": [1500000, 1700000, 1400000],
# })

st.divider()
st.subheader("💡 Insight Prediksi")
st.markdown("""
> **TODO Member 2:** Tambahkan insight otomatis berdasarkan hasil prediksi.
> Contoh: "Pengeluaran diprediksi meningkat 15% bulan depan, pertimbangkan mengurangi belanja hiburan."
""")

# ─── Tips Keuangan (static, bisa langsung tampil) ─────────────────────────────
st.divider()
with st.expander("💡 Tips Hemat Berdasarkan Pola Umummu"):
    st.markdown("""
    - **Makanan & Minuman** biasanya kategori terbesar. Coba meal prep mingguan untuk hemat 30%
    - **Transportasi**: pertimbangkan transportasi umum atau sepeda untuk jarak dekat
    - **Hiburan**: tetapkan budget hiburan maksimal 10% dari total pengeluaran
    - **Simpan dulu, belanja sisanya** — bukan sebaliknya!
    """)
