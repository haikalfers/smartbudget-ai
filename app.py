"""
app.py — Entry point SmartBudget AI
Halaman utama (Home/Landing) + inisialisasi global session state.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# ─── Konfigurasi Halaman ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartBudget AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Init Session State (selalu dipanggil di app.py) ─────────────────────────
from utils.data_utils import init_session_state, get_summary, format_rupiah, load_transactions
init_session_state()

# ─── Auto-train Models (Opsi 3: fallback jika .pkl tidak ada) ────────────────
# .pkl di-commit ke GitHub → startup normal cepat.
# Kode ini hanya jalan jika file .pkl tidak ditemukan (misalnya Streamlit Cloud
# restart setelah idle, atau fresh clone tanpa model files).
import os, subprocess

def auto_train_if_needed():
    """Generate dataset & train models jika file .pkl belum tersedia."""
    if not os.path.exists("data/sample_data.csv") or \
       not os.path.exists("data/training_klasifikasi.csv"):
        subprocess.run(["python", "data/generate_dataset.py"], check=True)

    if not os.path.exists("models/classifier.pkl"):
        subprocess.run(["python", "models/train_classifier.py"], check=True)

    if not os.path.exists("models/predictor.pkl"):
        subprocess.run(["python", "models/train_predictor.py"], check=True)

if "models_ready" not in st.session_state:
    _perlu_train = (
        not os.path.exists("models/classifier.pkl") or
        not os.path.exists("models/predictor.pkl")
    )
    if _perlu_train:
        with st.spinner("⚙️ Menyiapkan model AI (hanya sekali)..."):
            try:
                auto_train_if_needed()
                st.session_state.models_ready = True
            except Exception as _e:
                st.warning(f"⚠️ Model training gagal: {_e}. Beberapa fitur mungkin tidak tersedia.")
                st.session_state.models_ready = False
    else:
        st.session_state.models_ready = True

# ─── CSS Global ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #e0e0e0;
    }
    /* Sidebar branding */
    .sidebar-brand {
        text-align: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 10px;
    }
    /* Status badge */
    .badge-ok   { background: #d4edda; color: #155724; padding: 3px 10px; border-radius: 20px; font-size: 0.85em; }
    .badge-warn { background: #fff3cd; color: #856404; padding: 3px 10px; border-radius: 20px; font-size: 0.85em; }
    .badge-err  { background: #f8d7da; color: #721c24; padding: 3px 10px; border-radius: 20px; font-size: 0.85em; }
    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 40px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .hero-container h1 { font-size: 2.5rem; margin: 0; }
    .hero-container p  { font-size: 1.1rem; opacity: 0.9; margin-top: 8px; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2>💰 SmartBudget AI</h2>
        <p style="color: #666; font-size: 0.85em; margin: 0;">Manajemen Keuangan Mahasiswa</p>
    </div>
    """, unsafe_allow_html=True)

    # Status sistem
    st.markdown("#### 🔧 Status Sistem")
    _status = {}

    # Cek model klasifikasi
    try:
        from utils.classifier_utils import is_classifier_ready
        _status["Classifier"] = ("✅ Siap", "ok") if is_classifier_ready() else ("⚠️ Belum dilatih", "warn")
    except ImportError:
        _status["Classifier"] = ("❌ Error import", "err")

    # Cek model prediksi
    try:
        from utils.predictor_utils import is_predictor_ready
        _status["Predictor"] = ("✅ Siap", "ok") if is_predictor_ready() else ("⚠️ Belum dilatih", "warn")
    except ImportError:
        _status["Predictor"] = ("❌ Error import", "err")

    # Cek Groq API
    try:
        _groq_key = st.secrets.get("GROQ_API_KEY", "")
        _status["Groq API"] = ("✅ Key tersedia", "ok") if _groq_key else ("⚠️ Key belum diset", "warn")
    except Exception:
        _status["Groq API"] = ("⚠️ Secrets belum dikonfigurasi", "warn")

    for nama, (teks, level) in _status.items():
        st.markdown(f"`{nama}` {teks}")

    st.divider()

  # Quick stats
    df_sidebar = load_transactions()
    if not df_sidebar.empty:
        ring = get_summary(df_sidebar)
        st.markdown("#### 📊 Ringkasan Cepat")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Saldo", format_rupiah(ring["saldo"]))
        with col2:
            st.metric("Transaksi", ring["jumlah_transaksi"])
        st.metric("Total Pengeluaran", format_rupiah(ring["total_pengeluaran"]))

# ─── Konten Utama ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <h1>💰 SmartBudget AI</h1>
    <p>Aplikasi manajemen keuangan cerdas untuk mahasiswa — berbasis AI & Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# Cek apakah ada data
df = load_transactions()

if df.empty:
    # ── Tampilan Welcome ─────────────────────────────────────────────────────
    st.info("👋 Selamat datang! Belum ada data transaksi. Mulai dengan input transaksi atau load data sampel.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ➕ Mulai Input")
        st.markdown("Catat pemasukan dan pengeluaranmu secara manual dengan klasifikasi AI otomatis.")
        st.page_link("pages/2_Input_Transaksi.py", label="Input Transaksi →", icon="➕")

    with col2:
        st.markdown("### 📂 Load Data Sampel")
        st.markdown("Coba fitur aplikasi dengan data sampel 3 bulan yang sudah tersedia.")
        if st.button("🔄 Load Data Sampel", use_container_width=True):
            # Buat sample data jika belum ada
            try:
                from utils.data_utils import add_transaction
                # Buat beberapa transaksi sample
                sample_dates = pd.date_range(start='2024-04-01', periods=10)
                for i, date in enumerate(sample_dates):
                    add_transaction(
                        tanggal=date.date(),
                        deskripsi=f"Sample Transaksi {i+1}",
                        jumlah=50000 + (i*10000),
                        tipe="Pengeluaran" if i % 2 == 0 else "Pemasukan",
                        kategori="Makanan & Minuman" if i % 2 == 0 else "Uang Saku"
                    )
                st.success("✅ Data sampel berhasil dibuat!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")

    with col3:
        st.markdown("### 💬 Tanya AI Advisor")
        st.markdown("Chat dengan AI Advisor untuk saran keuangan personal berbasis datamu.")
        st.page_link("pages/5_AI_Advisor.py", label="Buka AI Advisor →", icon="💬")

    st.divider()

    # Fitur overview
    st.markdown("### ✨ Fitur Unggulan")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown("**🤖 Klasifikasi Otomatis**\n\nPengeluaran dikategorikan otomatis pakai ML (TF-IDF + Logistic Regression)")
    with f2:
        st.markdown("**📊 Dashboard Interaktif**\n\nVisualisasi Plotly lengkap: pie chart, tren bulanan, perbandingan")
    with f3:
        st.markdown("**🔮 Prediksi Keuangan**\n\nForecast kondisi keuangan ke depan dengan Polynomial Regression")
    with f4:
        st.markdown("**💬 AI Advisor**\n\nChatbot cerdas dengan 2 agentic tools — analisis & rekomendasi real-time")

else:
    # ── Dashboard Mini (ada data) ────────────────────────────────────────────
    ring = get_summary(df)

    st.markdown("### 📊 Ringkasan Keuangan")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("💚 Total Pemasukan", format_rupiah(ring["total_pemasukan"]))
    with m2:
        delta_color = "inverse" if ring["total_pengeluaran"] > ring["total_pemasukan"] else "normal"
        st.metric("🔴 Total Pengeluaran", format_rupiah(ring["total_pengeluaran"]))
    with m3:
        saldo_delta = "📈 Surplus" if ring["saldo"] >= 0 else "📉 Defisit"
        st.metric("💰 Saldo", format_rupiah(ring["saldo"]), saldo_delta)
    with m4:
        st.metric("📝 Total Transaksi", ring["jumlah_transaksi"])

    st.divider()

    # Tabel transaksi terbaru
    st.markdown("### 🕐 Transaksi Terbaru")
    df_sorted = df.sort_values("tanggal", ascending=False).head(5).copy()
    df_sorted["tanggal"] = df_sorted["tanggal"].dt.strftime("%d %b %Y")
    df_sorted["jumlah"] = df_sorted["jumlah"].apply(format_rupiah)
    df_sorted["tipe"] = df_sorted["tipe"].apply(
        lambda x: "🟢 " + x if x == "Pemasukan" else "🔴 " + x
    )
    st.dataframe(
        df_sorted[["tanggal", "deskripsi", "kategori", "tipe", "jumlah"]],
        use_container_width=True,
        hide_index=True,
    )

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.page_link("pages/1_Dashboard.py",          label="📊 Lihat Dashboard Lengkap →")
    with col_b:
        st.page_link("pages/4_Prediksi.py",           label="🔮 Lihat Prediksi Keuangan →")
    with col_c:
        st.page_link("pages/5_AI_Advisor.py",         label="💬 Chat dengan AI Advisor →")

    # Tombol reset
    with st.expander("⚙️ Opsi Data"):
        if st.button("🗑️ Hapus Semua Data", type="secondary"):
            from utils.data_utils import save_transactions
            empty_df = pd.DataFrame(columns=["id", "tanggal", "deskripsi", "jumlah", "tipe", "kategori"])
            save_transactions(empty_df)
            st.session_state.chat_history = []
            st.success("Data berhasil dihapus.")
            st.rerun()

# ─── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    f"""
    <div style="text-align:center; color:#999; font-size:0.82em">
    SmartBudget AI · Studi Independen Data Science & Generative AI · PT Celerates · {datetime.now().year}
    </div>
    """,
    unsafe_allow_html=True,
)
