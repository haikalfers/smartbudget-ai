"""
pages/3_Analisis.py
Halaman Analisis & Visualisasi Mendalam — UI/UX didesain ulang.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_utils import (
    init_session_state,
    load_transactions,
    get_summary,
    get_pengeluaran_per_kategori,
    get_tren_bulanan,
    format_rupiah,
    filter_by_period,
)
from styles import GLOBAL_CSS, PLOTLY_THEME
from components.sidebar import render_sidebar
from utils.init_styles import apply_global_styles

# ─── Setup ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Analisis | SmartBudget AI", page_icon="📈", layout="centered")
init_session_state()
render_sidebar()
apply_global_styles()

# ─── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="sb-page-header">
    <h1>📈 Analisis & Visualisasi</h1>
    <p>Analisis mendalam pola keuanganmu berdasarkan data historis.</p>
</div>
""", unsafe_allow_html=True)

df = load_transactions()

if df.empty:
    st.markdown("""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:3rem;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
        <div style="font-size:3rem;margin-bottom:12px">📭</div>
        <div style="font-size:1rem;font-weight:600;color:#0a1628;margin-bottom:6px">Belum ada data transaksi</div>
        <div style="font-size:0.875rem;color:#64748b;margin-bottom:16px">Tambahkan data di halaman Input Transaksi terlebih dahulu.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Input_Transaksi.py", label="➕ Input Transaksi", icon="➕")
    st.stop()

# ─── Filter Bar ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:1rem 1.25rem;margin-bottom:1.25rem;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
""", unsafe_allow_html=True)

# Responsive filter columns: CSS media queries handle stacking
col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    periode = st.selectbox(
        "📅 Periode",
        ["7 Hari", "30 Hari", "3 Bulan", "6 Bulan", "Semua"],
        index=1,
    )
with col_filter2:
    tipe_filter = st.multiselect(
        "Tipe Transaksi",
        ["Pemasukan", "Pengeluaran"],
        default=["Pemasukan", "Pengeluaran"],
    )

st.markdown("</div>", unsafe_allow_html=True)

df_filtered = filter_by_period(df, periode)
if tipe_filter:
    df_filtered = df_filtered[df_filtered["tipe"].isin(tipe_filter)]

summary = get_summary(df_filtered)

# ─── Summary Strip ─────────────────────────────────────────────────────────────
# Responsive metric cards: 2x2 grid, CSS media queries handle mobile
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.metric("💳 Saldo", format_rupiah(summary["saldo"]))
with col2:
    st.metric("📥 Pemasukan", format_rupiah(summary["total_pemasukan"]))
with col3:
    st.metric("📤 Pengeluaran", format_rupiah(summary["total_pengeluaran"]))
with col4:
    st.metric("📋 Transaksi", summary["jumlah_transaksi"])

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊  Kategori", "📅  Tren Waktu", "📋  Detail Transaksi"])

COLOR_PALETTE = ["#1e6ab3", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#ec4899", "#14b8a6", "#f97316"]

# ── Tab 1: Per Kategori ────────────────────────────────────────────────────────
with tab1:
    kategori_df = get_pengeluaran_per_kategori(df_filtered)
    
    if kategori_df.empty:
        st.info("📭 Tidak ada data pengeluaran untuk periode ini.")
    else:
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            st.markdown('<div class="sb-section-title">Proporsi Pengeluaran</div>', unsafe_allow_html=True)
            fig_donut = px.pie(
                kategori_df,
                values="jumlah",
                names="kategori",
                color_discrete_sequence=COLOR_PALETTE,
                hole=0.5,
            )
            fig_donut.update_traces(
                textposition="outside",
                textinfo="percent+label",
                textfont_size=11,
                pull=[0.04] + [0] * (len(kategori_df) - 1),
            )
            fig_donut.update_layout(
                **PLOTLY_THEME,
                showlegend=True,
                legend=dict(orientation="v", x=1.02, y=0.5),
                height=320,
                annotations=[{
                    "text": f"<b>{format_rupiah(kategori_df['jumlah'].sum())}</b>",
                    "x": 0.5, "y": 0.5,
                    "font": {"size": 11, "color": "#64748b"},
                    "showarrow": False,
                }],
            )
            st.plotly_chart(fig_donut, width='stretch', config={"displayModeBar": False})
        
        with col2:
            st.markdown('<div class="sb-section-title">Nominal per Kategori</div>', unsafe_allow_html=True)
            fig_bar = px.bar(
                kategori_df.sort_values("jumlah"),
                x="jumlah",
                y="kategori",
                orientation="h",
                color="jumlah",
                color_continuous_scale=[[0, "#dbeafe"], [1, "#0f4c81"]],
                labels={"jumlah": "Total (Rp)", "kategori": ""},
            )
            fig_bar.update_layout(
                **PLOTLY_THEME,
                showlegend=False,
                coloraxis_showscale=False,
                height=320,
                xaxis_title="",
                yaxis_title="",
            )
            fig_bar.update_traces(marker_line_width=0)
            fig_bar.update_xaxes(showgrid=True, gridcolor="#e2e8f0", gridwidth=0.5)
            fig_bar.update_yaxes(showgrid=False)
            st.plotly_chart(fig_bar, width='stretch', config={"displayModeBar": False})
        
        # ─── Tabel Kategori ────────────────────────────────────────────────────
        st.markdown('<div class="sb-section-title">📋 Tabel Ringkasan Kategori</div>', unsafe_allow_html=True)
        
        total_pengeluaran = kategori_df["jumlah"].sum()
        kategori_df = kategori_df.copy()
        kategori_df["persentase"] = (kategori_df["jumlah"] / total_pengeluaran * 100).round(1)
        kategori_df["jumlah_fmt"] = kategori_df["jumlah"].apply(format_rupiah)
        kategori_df["bar"] = kategori_df["persentase"]
        
        display_df = kategori_df[["kategori", "jumlah_fmt", "persentase"]].copy()
        display_df.columns = ["Kategori", "Total", "% dari Total"]
        display_df = display_df.sort_values("% dari Total", ascending=False)
        
        st.dataframe(
            display_df,
            width='stretch',
            hide_index=True,
            column_config={
                "% dari Total": st.column_config.ProgressColumn(
                    "% dari Total",
                    help="Persentase dari total pengeluaran",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),
            }
        )

# ── Tab 2: Tren Waktu ──────────────────────────────────────────────────────────
with tab2:
    tren_df = get_tren_bulanan(df_filtered)
    
    if tren_df.empty:
        st.info("📭 Tidak ada cukup data untuk menampilkan tren bulanan.")
    else:
        st.markdown('<div class="sb-section-title">Pemasukan vs Pengeluaran per Bulan</div>', unsafe_allow_html=True)
        
        fig_area = go.Figure()
        fig_area.add_trace(go.Scatter(
            x=tren_df["bulan"],
            y=tren_df["pemasukan"],
            fill="tozeroy",
            name="Pemasukan",
            line=dict(color="#22c55e", width=2.5),
            fillcolor="rgba(34,197,94,0.1)",
            mode="lines+markers",
            marker=dict(size=6, color="#22c55e"),
        ))
        fig_area.add_trace(go.Scatter(
            x=tren_df["bulan"],
            y=tren_df["pengeluaran"],
            fill="tozeroy",
            name="Pengeluaran",
            line=dict(color="#ef4444", width=2.5),
            fillcolor="rgba(239,68,68,0.1)",
            mode="lines+markers",
            marker=dict(size=6, color="#ef4444"),
        ))
        fig_area.update_layout(
            **PLOTLY_THEME,
            height=320,
            hovermode="x unified",
            xaxis_title="",
            yaxis_title="Nominal (Rp)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        fig_area.update_xaxes(showgrid=False)
        fig_area.update_yaxes(gridcolor="#e2e8f0", gridwidth=0.5)
        st.plotly_chart(fig_area, width='stretch', config={"displayModeBar": False})
        
        st.markdown('<div class="sb-section-title">Saldo Bersih per Bulan</div>', unsafe_allow_html=True)
        
        colors_saldo = ["#22c55e" if v >= 0 else "#ef4444" for v in tren_df["saldo"]]
        fig_saldo = go.Figure()
        fig_saldo.add_trace(go.Bar(
            x=tren_df["bulan"],
            y=tren_df["saldo"],
            marker_color=colors_saldo,
            marker_line_width=0,
            name="Saldo",
        ))
        fig_saldo.add_hline(y=0, line_dash="dot", line_color="#94a3b8", line_width=1.5)
        fig_saldo.update_layout(
            **PLOTLY_THEME,
            height=280,
            xaxis_title="",
            yaxis_title="Saldo (Rp)",
            showlegend=False,
        )
        fig_saldo.update_xaxes(showgrid=False)
        fig_saldo.update_yaxes(gridcolor="#e2e8f0", gridwidth=0.5)
        st.plotly_chart(fig_saldo, width='stretch', config={"displayModeBar": False})

# ── Tab 3: Detail Transaksi ────────────────────────────────────────────────────
with tab3:
    col_kat, col_cari = st.columns(2)
    
    with col_kat:
        kat_unik = ["Semua"] + sorted(df_filtered["kategori"].dropna().unique().tolist())
        kat_selected = st.selectbox("Filter Kategori", kat_unik)
    
    with col_cari:
        search_detail = st.text_input("Cari", placeholder="🔍 Cari deskripsi...", label_visibility="collapsed")
    
    if kat_selected != "Semua":
        df_detail = df_filtered[df_filtered["kategori"] == kat_selected]
    else:
        df_detail = df_filtered
    
    if search_detail:
        df_detail = df_detail[df_detail["deskripsi"].str.contains(search_detail, case=False, na=False)]
    
    df_display = df_detail.sort_values("tanggal", ascending=False).copy()
    df_display["jumlah_fmt"] = df_display.apply(
        lambda r: f"{'+ ' if r['tipe']=='Pemasukan' else '- '}{format_rupiah(r['jumlah'])}", axis=1
    )
    df_display["tanggal_fmt"] = pd.to_datetime(df_display["tanggal"]).dt.strftime("%d %b %Y")
    
    col_count, col_total = st.columns(2)
    with col_count:
        st.markdown(f'<div style="font-size:0.85rem;color:#64748b;padding:6px 0">{len(df_display)} transaksi ditemukan</div>', unsafe_allow_html=True)
    with col_total:
        total_val = df_display[df_display["tipe"]=="Pengeluaran"]["jumlah"].sum()
        st.markdown(f'<div style="font-size:0.85rem;color:#64748b;padding:6px 0;text-align:right">Total pengeluaran: <strong>{format_rupiah(total_val)}</strong></div>', unsafe_allow_html=True)
    
    display_final = df_display[["tanggal_fmt", "deskripsi", "kategori", "tipe", "jumlah_fmt"]].copy()
    display_final.columns = ["Tanggal", "Deskripsi", "Kategori", "Tipe", "Jumlah"]
    
    st.dataframe(display_final, width='stretch', hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    csv = df_detail.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️  Download CSV",
        data=csv,
        file_name="transaksi_smartbudget.csv",
        mime="text/csv",
    )