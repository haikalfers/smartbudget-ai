"""
app.py
SmartBudget AI — Halaman Home yang didesain ulang.
"""

import streamlit as st
from utils.data_utils import init_session_state, load_transactions
from styles import GLOBAL_CSS
from components.sidebar import render_sidebar

# ─── Setup ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartBudget AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 16px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
            <div style="width:36px;height:36px;background:linear-gradient(135deg,#1e6ab3,#0f4c81);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px">💰</div>
            <div>
                <div style="font-size:1.1rem;font-weight:700;color:#fff">SmartBudget AI</div>
                <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);margin-top:1px">Kelola keuangan dengan cerdas</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    transactions = load_transactions()
    if not transactions.empty:
        total_pemasukan = transactions[transactions["tipe"] == "Pemasukan"]["jumlah"].sum()
        total_pengeluaran = transactions[transactions["tipe"] == "Pengeluaran"]["jumlah"].sum()
        saldo = total_pemasukan - total_pengeluaran
        saldo_color = "#4ade80" if saldo >= 0 else "#f87171"
        
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.08);border-radius:10px;padding:14px;margin-bottom:8px">
            <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px">Saldo Saat Ini</div>
            <div style="font-size:1.6rem;font-weight:700;color:{saldo_color}">Rp {saldo:,.0f}</div>
            <div style="display:flex;justify-content:space-between;margin-top:10px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.1)">
                <div>
                    <div style="font-size:0.68rem;color:rgba(255,255,255,0.45)">↑ Masuk</div>
                    <div style="font-size:0.8rem;color:#4ade80;font-weight:600">Rp {total_pemasukan:,.0f}</div>
                </div>
                <div>
                    <div style="font-size:0.68rem;color:rgba(255,255,255,0.45)">↓ Keluar</div>
                    <div style="font-size:0.8rem;color:#f87171;font-weight:600">Rp {total_pengeluaran:,.0f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.08);border-radius:10px;padding:14px;text-align:center">
            <div style="font-size:1.5rem;margin-bottom:6px">📭</div>
            <div style="font-size:0.8rem;color:rgba(255,255,255,0.6)">Belum ada transaksi</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top:20px">
        <div style="font-size:0.68rem;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;padding:0 4px">Menu</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.page_link("app.py", label="🏠  Beranda", use_container_width=True)
    st.page_link("pages/1_Dashboard.py", label="📊  Dashboard", use_container_width=True)
    st.page_link("pages/2_Input_Transaksi.py", label="➕  Input Transaksi", use_container_width=True)
    st.page_link("pages/3_Analisis.py", label="📈  Analisis", use_container_width=True)
    st.page_link("pages/4_Prediksi.py", label="🔮  Prediksi", use_container_width=True)
    st.page_link("pages/5_AI_Advisor.py", label="💬  AI Advisor", use_container_width=True)
    
    st.divider()
    st.markdown("""
    <div style="font-size:0.7rem;color:rgba(255,255,255,0.3);text-align:center;padding:4px 0">
        SmartBudget AI v2.0<br>Studi Independen Data Science
    </div>
    """, unsafe_allow_html=True)

# ─── Hero Section ──────────────────────────────────────────────────────────────
transactions = load_transactions()
total_pemasukan = transactions[transactions["tipe"] == "Pemasukan"]["jumlah"].sum() if not transactions.empty else 0
total_pengeluaran = transactions[transactions["tipe"] == "Pengeluaran"]["jumlah"].sum() if not transactions.empty else 0
saldo = total_pemasukan - total_pengeluaran
total_tx = len(transactions)

st.markdown(f"""
<div style="background:linear-gradient(135deg,#0a1628 0%,#0f4c81 60%,#1e6ab3 100%);border-radius:16px;padding:2rem 2.5rem;margin-bottom:1.5rem;position:relative;overflow:hidden">
    <div style="position:absolute;top:-40px;right:-40px;width:200px;height:200px;background:rgba(255,255,255,0.04);border-radius:50%"></div>
    <div style="position:absolute;bottom:-60px;right:80px;width:150px;height:150px;background:rgba(255,255,255,0.04);border-radius:50%"></div>
    <div style="position:relative;z-index:1">
        <div style="font-size:0.75rem;color:rgba(255,255,255,0.55);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px">Selamat datang kembali 👋</div>
        <h1 style="font-size:1.8rem;font-weight:800;color:#fff;margin:0 0 6px">SmartBudget AI</h1>
        <p style="color:rgba(255,255,255,0.65);font-size:0.9rem;margin:0 0 1.5rem">Aplikasi manajemen keuangan cerdas — powered by Machine Learning & Generative AI</p>
        <div style="display:flex;gap:2rem;flex-wrap:wrap">
            <div>
                <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.05em">Total Transaksi</div>
                <div style="font-size:1.4rem;font-weight:700;color:#fff">{total_tx}</div>
            </div>
            <div style="width:1px;background:rgba(255,255,255,0.15)"></div>
            <div>
                <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.05em">Pemasukan</div>
                <div style="font-size:1.4rem;font-weight:700;color:#4ade80">Rp {total_pemasukan:,.0f}</div>
            </div>
            <div style="width:1px;background:rgba(255,255,255,0.15)"></div>
            <div>
                <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.05em">Pengeluaran</div>
                <div style="font-size:1.4rem;font-weight:700;color:#f87171">Rp {total_pengeluaran:,.0f}</div>
            </div>
            <div style="width:1px;background:rgba(255,255,255,0.15)"></div>
            <div>
                <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.05em">Saldo</div>
                <div style="font-size:1.4rem;font-weight:700;color:{'#4ade80' if saldo >= 0 else '#f87171'}">Rp {saldo:,.0f}</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Feature Cards ─────────────────────────────────────────────────────────────
st.markdown("""<div style="font-size:1rem;font-weight:700;color:#0a1628;margin-bottom:1rem">🚀 Fitur Utama</div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# with col1:
#     st.markdown("""
#     <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;height:100%;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
#         <div style="width:40px;height:40px;background:#dbeafe;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:12px">📊</div>
#         <div style="font-size:1rem;font-weight:700;color:#0a1628;margin-bottom:6px">Dashboard & Analisis</div>
#         <div style="font-size:0.85rem;color:#64748b;line-height:1.6">Visualisasi pola pengeluaran dengan grafik interaktif. Pantau tren keuanganmu secara real-time.</div>
#     </div>
#     """, unsafe_allow_html=True)
#     st.page_link("pages/1_Dashboard.py", label="Buka Dashboard →", icon="📊")
with col1:
    with st.container(border=True):

        st.markdown("""
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;height:100%;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
            <div style="width:40px;height:40px;background:#dbeafe;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:12px">📊</div>
            <div style="font-size:1rem;font-weight:700;color:#0a1628;margin-bottom:6px">Dashboard & Analisis</div>
            <div style="font-size:0.85rem;color:#64748b;line-height:1.6">Visualisasi pola pengeluaran dengan grafik interaktif. Pantau tren keuanganmu secara real-time.</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "📊 Buka Dashboard",
            key="go_dashboard",
            use_container_width=True
        ):
            st.switch_page("pages/1_Dashboard.py")

with col2:
    with st.container(border=True):

        st.markdown("""
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;height:100%;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
            <div style="width:40px;height:40px;background:#fef3c7;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:12px">🔮</div>
            <div style="font-size:1rem;font-weight:700;color:#0a1628;margin-bottom:6px">Prediksi Keuangan</div>
            <div style="font-size:0.85rem;color:#64748b;line-height:1.6">Model ML memprediksi kondisi keuanganmu ke depan berdasarkan pola historis transaksi.</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "🔮 Lihat Prediksi",
            key="go_prediksi",
            use_container_width=True
        ):
            st.switch_page("pages/4_Prediksi.py")

with col3:
    with st.container(border=True):

        st.markdown("""
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;height:100%;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
            <div style="width:40px;height:40px;background:#dcfce7;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:12px">💬</div>
            <div style="font-size:1rem;font-weight:700;color:#0a1628;margin-bottom:6px">AI Advisor</div>
            <div style="font-size:0.85rem;color:#64748b;line-height:1.6">Chatbot AI yang menganalisis transaksimu dan memberikan rekomendasi keuangan personal.</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "💬 Tanya AI",
            key="go_ai_advisor",
            use_container_width=True
        ):
            st.switch_page("pages/5_AI_Advisor.py")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Getting Started ───────────────────────────────────────────────────────────
if transactions.empty:
    st.markdown("""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.5rem;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
        <div style="font-size:1rem;font-weight:700;color:#0a1628;margin-bottom:1rem">⚡ Mulai Sekarang</div>
        <div style="display:flex;flex-direction:column;gap:12px">
            <div style="display:flex;align-items:center;gap:12px">
                <div style="min-width:28px;height:28px;background:#dbeafe;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:#0f4c81">1</div>
                <div style="font-size:0.875rem;color:#334155">Catat pemasukan & pengeluaranmu di <strong>Input Transaksi</strong></div>
            </div>
            <div style="display:flex;align-items:center;gap:12px">
                <div style="min-width:28px;height:28px;background:#dbeafe;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:#0f4c81">2</div>
                <div style="font-size:0.875rem;color:#334155">Lihat visualisasi pola keuanganmu di <strong>Dashboard</strong></div>
            </div>
            <div style="display:flex;align-items:center;gap:12px">
                <div style="min-width:28px;height:28px;background:#dbeafe;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:#0f4c81">3</div>
                <div style="font-size:0.875rem;color:#334155">Analisis breakdown kategori di halaman <strong>Analisis</strong></div>
            </div>
            <div style="display:flex;align-items:center;gap:12px">
                <div style="min-width:28px;height:28px;background:#dbeafe;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:#0f4c81">4</div>
                <div style="font-size:0.875rem;color:#334155">Proyeksikan masa depan keuanganmu di <strong>Prediksi</strong></div>
            </div>
            <div style="display:flex;align-items:center;gap:12px">
                <div style="min-width:28px;height:28px;background:#dbeafe;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:#0f4c81">5</div>
                <div style="font-size:0.875rem;color:#334155">Minta saran personal dari <strong>AI Advisor</strong></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link("pages/2_Input_Transaksi.py", label="➕ Mulai Catat Transaksi Pertamamu", icon="➕")