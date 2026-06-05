"""
pages/1_Dashboard.py
Halaman Dashboard & Visualisasi utama.
👤 Dikerjakan oleh: Member 3
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

# ─── Setup ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Dashboard | SmartBudget AI", page_icon="📊", layout="wide")
init_session_state()

st.title("📊 Dashboard Keuangan")
st.markdown("Pantau kondisi keuanganmu secara real-time.")

# ─── Filter Periode ────────────────────────────────────────────────────────────
periode = st.selectbox(
    "📅 Filter Periode",
    ["7 Hari", "30 Hari", "3 Bulan", "6 Bulan", "Semua"],
    index=1,
)

df = load_transactions()
df_filtered = filter_by_period(df, periode)

# ─── Summary Metrics ───────────────────────────────────────────────────────────
summary = get_summary(df_filtered)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💳 Saldo", format_rupiah(summary["saldo"]))
with col2:
    st.metric("📥 Pemasukan", format_rupiah(summary["total_pemasukan"]))
with col3:
    st.metric("📤 Pengeluaran", format_rupiah(summary["total_pengeluaran"]))
with col4:
    st.metric("📋 Transaksi", summary["jumlah_transaksi"])

st.divider()

# ─── TODO: Member 3 mengisi bagian visualisasi di bawah ini ────────────────────
# Gunakan Plotly Express untuk semua chart.
# Referensi warna tema: primaryColor = "#6C63FF"

if df_filtered.empty:
    st.info("📭 Belum ada data transaksi. Tambahkan transaksi di halaman **Input Transaksi**.")
    st.stop()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🥧 Pengeluaran per Kategori")
    # TODO Member 3: Pie chart pengeluaran per kategori
    # Gunakan get_pengeluaran_per_kategori(df_filtered)
    kategori_df = get_pengeluaran_per_kategori(df_filtered)
    if not kategori_df.empty:
        fig_pie = px.pie(
            kategori_df,
            values="jumlah",
            names="kategori",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4,
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Belum ada data pengeluaran.")

with col_right:
    st.subheader("📈 Tren Bulanan")
    # TODO Member 3: Line/bar chart tren pemasukan vs pengeluaran per bulan
    # Gunakan get_tren_bulanan(df_filtered)
    tren_df = get_tren_bulanan(df_filtered)
    if not tren_df.empty:
        fig_tren = go.Figure()
        fig_tren.add_trace(go.Bar(
            x=tren_df["bulan"], y=tren_df["pemasukan"],
            name="Pemasukan", marker_color="#2ECC71"
        ))
        fig_tren.add_trace(go.Bar(
            x=tren_df["bulan"], y=tren_df["pengeluaran"],
            name="Pengeluaran", marker_color="#E74C3C"
        ))
        fig_tren.update_layout(barmode="group", xaxis_title="Bulan", yaxis_title="Nominal (Rp)")
        st.plotly_chart(fig_tren, use_container_width=True)
    else:
        st.info("Belum ada data tren bulanan.")

# ─── Tabel Transaksi Terbaru ───────────────────────────────────────────────────
st.subheader("🕒 Transaksi Terbaru")
recent = df_filtered.sort_values("tanggal", ascending=False).head(10)
if not recent.empty:
    recent_display = recent[["tanggal", "deskripsi", "kategori", "tipe", "jumlah"]].copy()
    recent_display["jumlah"] = recent_display["jumlah"].apply(format_rupiah)
    recent_display.columns = ["Tanggal", "Deskripsi", "Kategori", "Tipe", "Jumlah"]
    st.dataframe(recent_display, use_container_width=True, hide_index=True)
