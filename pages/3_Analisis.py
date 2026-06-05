"""
pages/3_Analisis.py
Halaman Analisis & Visualisasi mendalam.
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
st.set_page_config(page_title="Analisis | SmartBudget AI", page_icon="📈", layout="wide")
init_session_state()

st.title("📈 Analisis & Visualisasi")
st.markdown("Analisis mendalam pola keuanganmu berdasarkan data historis.")

df = load_transactions()

if df.empty:
    st.warning("📭 Belum ada data transaksi. Tambahkan data di halaman **Input Transaksi** terlebih dahulu.")
    st.page_link("pages/2_Input_Transaksi.py", label="➕ Input Transaksi", icon="➕")
    st.stop()

# ─── Filter ────────────────────────────────────────────────────────────────────
col_filter1, col_filter2 = st.columns(2)
with col_filter1:
    periode = st.selectbox("📅 Periode", ["7 Hari", "30 Hari", "3 Bulan", "6 Bulan", "Semua"], index=1)
with col_filter2:
    tipe_filter = st.multiselect("Tipe Transaksi", ["Pemasukan", "Pengeluaran"],
                                  default=["Pemasukan", "Pengeluaran"])

df_filtered = filter_by_period(df, periode)
if tipe_filter:
    df_filtered = df_filtered[df_filtered["tipe"].isin(tipe_filter)]

st.divider()

# ─── Tab Analisis ──────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊 Kategori", "📅 Tren Waktu", "📋 Detail Transaksi"])

# ── Tab 1: Per Kategori ────────────────────────────────────────────────────────
with tab1:
    st.subheader("Breakdown Pengeluaran per Kategori")

    kategori_df = get_pengeluaran_per_kategori(df_filtered)

    if kategori_df.empty:
        st.info("Tidak ada data pengeluaran untuk periode ini.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            # Donut chart
            fig_donut = px.pie(
                kategori_df, values="jumlah", names="kategori",
                title="Proporsi Pengeluaran",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.5,
            )
            fig_donut.update_traces(textposition="outside", textinfo="percent+label")
            fig_donut.update_layout(showlegend=False)
            st.plotly_chart(fig_donut, use_container_width=True)

        with col2:
            # Bar chart horizontal
            fig_bar = px.bar(
                kategori_df,
                x="jumlah", y="kategori",
                orientation="h",
                title="Nominal per Kategori",
                color="jumlah",
                color_continuous_scale="Purples",
                labels={"jumlah": "Total (Rp)", "kategori": "Kategori"},
            )
            fig_bar.update_layout(showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        # Tabel ringkasan
        st.subheader("Tabel Kategori")
        total_pengeluaran = kategori_df["jumlah"].sum()
        kategori_df["persentase"] = (kategori_df["jumlah"] / total_pengeluaran * 100).round(1)
        kategori_df["jumlah_fmt"] = kategori_df["jumlah"].apply(format_rupiah)
        display_df = kategori_df[["kategori", "jumlah_fmt", "persentase"]].rename(
            columns={"kategori": "Kategori", "jumlah_fmt": "Total", "persentase": "% dari Total"}
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)

# ── Tab 2: Tren Waktu ──────────────────────────────────────────────────────────
with tab2:
    st.subheader("Tren Keuangan per Bulan")

    tren_df = get_tren_bulanan(df_filtered)

    if tren_df.empty:
        st.info("Tidak ada cukup data untuk menampilkan tren.")
    else:
        # Area chart tren
        fig_area = go.Figure()
        fig_area.add_trace(go.Scatter(
            x=tren_df["bulan"], y=tren_df["pemasukan"],
            fill="tonexty", name="Pemasukan",
            line=dict(color="#2ECC71", width=2),
            fillcolor="rgba(46,204,113,0.1)"
        ))
        fig_area.add_trace(go.Scatter(
            x=tren_df["bulan"], y=tren_df["pengeluaran"],
            fill="tozeroy", name="Pengeluaran",
            line=dict(color="#E74C3C", width=2),
            fillcolor="rgba(231,76,60,0.1)"
        ))
        fig_area.update_layout(
            title="Pemasukan vs Pengeluaran per Bulan",
            xaxis_title="Bulan",
            yaxis_title="Nominal (Rp)",
            hovermode="x unified",
        )
        st.plotly_chart(fig_area, use_container_width=True)

        # Saldo bulanan
        fig_saldo = px.bar(
            tren_df, x="bulan", y="saldo",
            title="Saldo Bersih per Bulan",
            color="saldo",
            color_continuous_scale=["#E74C3C", "#F39C12", "#2ECC71"],
            labels={"saldo": "Saldo (Rp)", "bulan": "Bulan"},
        )
        fig_saldo.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_saldo, use_container_width=True)

# ── Tab 3: Detail Transaksi ────────────────────────────────────────────────────
with tab3:
    st.subheader("Semua Transaksi")

    # Filter tambahan
    kat_unik = ["Semua"] + sorted(df_filtered["kategori"].dropna().unique().tolist())
    kat_selected = st.selectbox("Filter Kategori", kat_unik)

    if kat_selected != "Semua":
        df_detail = df_filtered[df_filtered["kategori"] == kat_selected]
    else:
        df_detail = df_filtered

    df_display = df_detail.sort_values("tanggal", ascending=False).copy()
    df_display["jumlah"] = df_display["jumlah"].apply(format_rupiah)
    df_display["tanggal"] = df_display["tanggal"].dt.strftime("%d %b %Y")
    df_display = df_display[["tanggal", "deskripsi", "kategori", "tipe", "jumlah"]]
    df_display.columns = ["Tanggal", "Deskripsi", "Kategori", "Tipe", "Jumlah"]

    st.dataframe(df_display, use_container_width=True, hide_index=True)

    # Export CSV
    csv = df_detail.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download CSV",
        data=csv,
        file_name="transaksi_smartbudget.csv",
        mime="text/csv",
    )
