"""
pages/1_Dashboard.py
Halaman Dashboard & Visualisasi — UI/UX didesain ulang.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_utils import (
    init_session_state,
    load_transactions,
    get_summary,
    get_pengeluaran_per_kategori,
    get_tren_bulanan,
    format_rupiah,
    filter_by_period,
)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, PLOTLY_THEME
from components.sidebar import render_sidebar

# ─── Setup ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Dashboard | SmartBudget AI", page_icon="📊", layout="wide")
init_session_state()
render_sidebar()
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ─── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="sb-page-header">
    <h1>📊 Dashboard Keuangan</h1>
    <p>Pantau kondisi keuanganmu secara real-time.</p>
</div>
""", unsafe_allow_html=True)

# ─── Filter Periode (styled) ───────────────────────────────────────────────────
col_filter, col_spacer = st.columns([2, 5])
with col_filter:
    periode = st.selectbox(
        "Filter Periode",
        ["7 Hari", "30 Hari", "3 Bulan", "6 Bulan", "Semua"],
        index=1,
        label_visibility="collapsed",
    )

df = load_transactions()
df_filtered = filter_by_period(df, periode)
summary = get_summary(df_filtered)

# ─── Metric Cards ──────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

saldo = summary["saldo"]
saldo_delta = "✅ Positif" if saldo >= 0 else "⚠️ Negatif"

with col1:
    st.metric(
        label="💳 Saldo",
        value=format_rupiah(saldo),
        delta=saldo_delta,
    )
with col2:
    st.metric(
        label="📥 Pemasukan",
        value=format_rupiah(summary["total_pemasukan"]),
    )
with col3:
    st.metric(
        label="📤 Pengeluaran",
        value=format_rupiah(summary["total_pengeluaran"]),
    )
with col4:
    st.metric(
        label="📋 Transaksi",
        value=summary["jumlah_transaksi"],
    )

st.markdown("<br>", unsafe_allow_html=True)

if df_filtered.empty:
    st.markdown("""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:3rem;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
        <div style="font-size:3rem;margin-bottom:12px">📭</div>
        <div style="font-size:1rem;font-weight:600;color:#0a1628;margin-bottom:6px">Belum ada data transaksi</div>
        <div style="font-size:0.875rem;color:#64748b">Tambahkan transaksi di halaman Input Transaksi.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Charts Row ────────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2, gap="medium")

with col_left:
    st.markdown('<div class="sb-section-title">🥧 Pengeluaran per Kategori</div>', unsafe_allow_html=True)
    kategori_df = get_pengeluaran_per_kategori(df_filtered)
    
    if not kategori_df.empty:
        fig_pie = px.pie(
            kategori_df,
            values="jumlah",
            names="kategori",
            color_discrete_sequence=["#1e6ab3", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#ec4899", "#14b8a6"],
            hole=0.45,
        )
        fig_pie.update_traces(
            textposition="outside",
            textinfo="percent+label",
            textfont_size=12,
            pull=[0.03] * len(kategori_df),
        )
        fig_pie.update_layout(
            **PLOTLY_THEME,
            showlegend=False,
            height=300,
            annotations=[{
                "text": f"<b>{len(kategori_df)}</b><br>kategori",
                "x": 0.5, "y": 0.5,
                "font_size": 14,
                "showarrow": False,
            }],
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Belum ada data pengeluaran.")

with col_right:
    st.markdown('<div class="sb-section-title">📈 Tren Bulanan</div>', unsafe_allow_html=True)
    tren_df = get_tren_bulanan(df_filtered)
    
    if not tren_df.empty:
        fig_tren = go.Figure()
        fig_tren.add_trace(go.Bar(
            x=tren_df["bulan"], y=tren_df["pemasukan"],
            name="Pemasukan",
            marker_color="#22c55e",
            marker_line_width=0,
        ))
        fig_tren.add_trace(go.Bar(
            x=tren_df["bulan"], y=tren_df["pengeluaran"],
            name="Pengeluaran",
            marker_color="#ef4444",
            marker_line_width=0,
        ))
        fig_tren.update_layout(
            **PLOTLY_THEME,
            barmode="group",
            xaxis_title="",
            yaxis_title="Nominal (Rp)",
            height=300,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            bargap=0.3,
            bargroupgap=0.08,
        )
        fig_tren.update_xaxes(showgrid=False)
        fig_tren.update_yaxes(gridcolor="#e2e8f0", gridwidth=0.5)
        st.plotly_chart(fig_tren, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Belum ada data tren bulanan.")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Spending Health Bar ───────────────────────────────────────────────────────
if summary["total_pemasukan"] > 0:
    spending_ratio = summary["total_pengeluaran"] / summary["total_pemasukan"] * 100
    bar_color = "#22c55e" if spending_ratio < 70 else ("#f59e0b" if spending_ratio < 90 else "#ef4444")
    health_text = "Sangat Sehat 🟢" if spending_ratio < 70 else ("Perlu Perhatian 🟡" if spending_ratio < 90 else "Berbahaya 🔴")
    
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.2rem;margin-bottom:1rem;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
            <div style="font-size:0.9rem;font-weight:600;color:#0a1628">💡 Rasio Pengeluaran</div>
            <div style="font-size:0.8rem;font-weight:600;color:#64748b">{health_text}</div>
        </div>
        <div style="background:#f1f5f9;border-radius:6px;height:10px;overflow:hidden;margin-bottom:8px">
            <div style="width:{min(spending_ratio,100):.1f}%;height:100%;background:{bar_color};border-radius:6px;transition:width 0.4s ease"></div>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:0.75rem;color:#94a3b8">
            <span>Pengeluaran: {spending_ratio:.1f}% dari pemasukan</span>
            <span>Target: &lt; 70%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Tabel Transaksi Terbaru ───────────────────────────────────────────────────
st.markdown('<div class="sb-section-title">🕒 Transaksi Terbaru</div>', unsafe_allow_html=True)

recent = df_filtered.sort_values("tanggal", ascending=False).head(10)
if not recent.empty:
    recent_display = recent[["tanggal", "deskripsi", "kategori", "tipe", "jumlah"]].copy()
    recent_display["jumlah_fmt"] = recent_display.apply(
        lambda r: f"{'📥 +' if r['tipe'] == 'Pemasukan' else '📤 -'}{format_rupiah(r['jumlah'])}", axis=1
    )
    recent_display["tanggal"] = pd.to_datetime(recent_display["tanggal"]).dt.strftime("%d %b %Y")
    
    display_cols = recent_display[["tanggal", "deskripsi", "kategori", "tipe", "jumlah_fmt"]].copy()
    display_cols.columns = ["Tanggal", "Deskripsi", "Kategori", "Tipe", "Jumlah"]
    
    st.dataframe(
        display_cols,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Tipe": st.column_config.TextColumn(width="small"),
            "Jumlah": st.column_config.TextColumn(width="medium"),
        }
    )