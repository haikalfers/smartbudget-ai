"""
pages/1_Insights_Keuangan.py
Dashboard & Analisis Keuangan Terpadu — Kombinasi fitur terbaik dari kedua halaman.
Menggunakan tabs untuk pengalaman pengguna yang lebih terstruktur.
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
from utils.init_styles import apply_global_styles

# ─── Setup ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Insights Keuangan | SmartBudget AI",
    page_icon="📈",
    layout="wide"
)
init_session_state()
render_sidebar()
apply_global_styles()

# ─── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="sb-page-header">
    <h1>📈 Insights Keuangan</h1>
    <p>Dashboard & analisis mendalam pola keuanganmu dalam satu tempat.</p>
</div>
""", unsafe_allow_html=True)

# ─── Data Loading & Filtering ──────────────────────────────────────────────────
df = load_transactions()

# Filter Controls (Sidebar friendly layout)
col_filter1, col_filter2, col_filter3 = st.columns(3)

with col_filter1:
    periode = st.selectbox(
        "📅 Filter Periode",
        ["Bulan Ini", "7 Hari", "30 Hari", "3 Bulan", "6 Bulan", "Semua"],
        index=1,
    )

with col_filter2:
    tipe_filter = st.multiselect(
        "Tipe Transaksi",
        ["Pemasukan", "Pengeluaran"],
        default=["Pemasukan", "Pengeluaran"],
    )

with col_filter3:
    kat_unik_all = sorted(df["kategori"].dropna().unique().tolist())
    kat_filter = st.multiselect(
        "Kategori",
        kat_unik_all,
        default=kat_unik_all,
    )

# ─── Apply Filters ────────────────────────────────────────────────────────────
df_filtered = filter_by_period(df, periode)
if tipe_filter:
    df_filtered = df_filtered[df_filtered["tipe"].isin(tipe_filter)]
if kat_filter:
    df_filtered = df_filtered[df_filtered["kategori"].isin(kat_filter)]

summary = get_summary(df_filtered)

# ─── Check Empty Data ─────────────────────────────────────────────────────────
if df_filtered.empty:
    st.markdown("""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:3rem;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
        <div style="font-size:3rem;margin-bottom:12px">📭</div>
        <div style="font-size:1rem;font-weight:600;color:#0a1628;margin-bottom:6px">Belum ada data transaksi</div>
        <div style="font-size:0.875rem;color:#64748b">Tambahkan transaksi di halaman Input Transaksi.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Overview Section: Metric Cards ────────────────────────────────────────────
st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
st.markdown('<div class="sb-section-title">📊 Ringkasan Periode</div>', unsafe_allow_html=True)

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

# ─── Spending Health Bar ───────────────────────────────────────────────────────
if summary["total_pemasukan"] > 0:
    spending_ratio = summary["total_pengeluaran"] / summary["total_pemasukan"] * 100
    bar_color = "#22c55e" if spending_ratio < 70 else ("#f59e0b" if spending_ratio < 90 else "#ef4444")
    health_text = "Sangat Sehat 🟢" if spending_ratio < 70 else ("Perlu Perhatian 🟡" if spending_ratio < 90 else "Berbahaya 🔴")
    
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.2rem;margin-bottom:1.5rem;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
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

st.markdown("<br>", unsafe_allow_html=True)

# ─── Main Tabs Section ────────────────────────────────────────────────────────
st.markdown('<div class="sb-section-title">🔍 Analisis Mendalam</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Kategori", "📅 Tren Waktu", "📋 Detail Transaksi", "📥 Export"])

COLOR_PALETTE = ["#1e6ab3", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#ec4899", "#14b8a6", "#f97316"]

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: KATEGORI
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    kategori_df = get_pengeluaran_per_kategori(df_filtered)
    
    if kategori_df.empty:
        st.info("📭 Tidak ada data pengeluaran untuk filter yang dipilih.")
    else:
        col1, col2 = st.columns(2, gap="medium")
        
        # ─── Pie Chart ─────────────────────────────────────────────────────────
        with col1:
            st.markdown('<div class="sb-section-title">Proporsi Pengeluaran</div>', unsafe_allow_html=True)
            fig_pie = px.pie(
                kategori_df,
                values="jumlah",
                names="kategori",
                color_discrete_sequence=COLOR_PALETTE,
                hole=0.45,
            )
            fig_pie.update_traces(
                textposition="outside",
                textinfo="percent+label",
                textfont_size=11,
                pull=[0.03] * len(kategori_df),
            )
            fig_pie.update_layout(
                **PLOTLY_THEME,
                showlegend=False,
                height=350,
                annotations=[{
                    "text": f"<b>{format_rupiah(kategori_df['jumlah'].sum())}</b><br><span style='font-size:0.8em'>Total</span>",
                    "x": 0.5, "y": 0.5,
                    "font_size": 12,
                    "showarrow": False,
                }],
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        
        # ─── Bar Chart ─────────────────────────────────────────────────────────
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
                height=350,
                xaxis_title="",
                yaxis_title="",
            )
            fig_bar.update_traces(marker_line_width=0)
            fig_bar.update_xaxes(showgrid=True, gridcolor="#e2e8f0", gridwidth=0.5)
            fig_bar.update_yaxes(showgrid=False)
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        
        # ─── Category Summary Table ────────────────────────────────────────────
        st.markdown('<div class="sb-section-title">📋 Tabel Ringkasan Kategori</div>', unsafe_allow_html=True)
        
        total_pengeluaran = kategori_df["jumlah"].sum()
        kategori_summary = kategori_df.copy()
        kategori_summary["persentase"] = (kategori_summary["jumlah"] / total_pengeluaran * 100).round(1)
        kategori_summary["jumlah_fmt"] = kategori_summary["jumlah"].apply(format_rupiah)
        
        display_df = kategori_summary[["kategori", "jumlah_fmt", "persentase"]].copy()
        display_df.columns = ["Kategori", "Total", "% dari Total"]
        display_df = display_df.sort_values("% dari Total", ascending=False)
        
        st.dataframe(
            display_df,
            use_container_width=True,
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

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: TREN WAKTU
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    tren_df = get_tren_bulanan(df_filtered)
    
    if tren_df.empty:
        st.info("📭 Tidak ada cukup data untuk menampilkan tren bulanan.")
    else:
        # ─── Area Chart: Pemasukan vs Pengeluaran ───────────────────────────
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
            height=350,
            hovermode="x unified",
            xaxis_title="",
            yaxis_title="Nominal (Rp)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        fig_area.update_xaxes(showgrid=False)
        fig_area.update_yaxes(gridcolor="#e2e8f0", gridwidth=0.5)
        st.plotly_chart(fig_area, use_container_width=True, config={"displayModeBar": False})
        
        # ─── Bar Chart: Saldo Bersih per Bulan ──────────────────────────────
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
            height=300,
            xaxis_title="",
            yaxis_title="Saldo (Rp)",
            showlegend=False,
        )
        fig_saldo.update_xaxes(showgrid=False)
        fig_saldo.update_yaxes(gridcolor="#e2e8f0", gridwidth=0.5)
        st.plotly_chart(fig_saldo, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: DETAIL TRANSAKSI
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    col_kat, col_cari = st.columns([2, 2])
    
    with col_kat:
        kat_detail_unik = ["Semua"] + sorted(df_filtered["kategori"].dropna().unique().tolist())
        kat_selected = st.selectbox("Filter Kategori Tambahan", kat_detail_unik, label_visibility="collapsed")
    
    with col_cari:
        search_detail = st.text_input("🔍 Cari deskripsi...", label_visibility="collapsed", placeholder="Cari transaksi...")
    
    # ─── Apply Detail Filters ──────────────────────────────────────────────
    df_detail = df_filtered.copy()
    
    if kat_selected != "Semua":
        df_detail = df_detail[df_detail["kategori"] == kat_selected]
    
    if search_detail:
        df_detail = df_detail[df_detail["deskripsi"].str.contains(search_detail, case=False, na=False)]
    
    df_display = df_detail.sort_values("tanggal", ascending=False).copy()
    
    # ─── Display Metrics ───────────────────────────────────────────────────
    col_count, col_income, col_expense, col_net = st.columns(4)
    
    with col_count:
        st.metric("Transaksi", len(df_display))
    
    with col_income:
        income_total = df_display[df_display["tipe"]=="Pemasukan"]["jumlah"].sum()
        st.metric("Total Pemasukan", format_rupiah(income_total))
    
    with col_expense:
        expense_total = df_display[df_display["tipe"]=="Pengeluaran"]["jumlah"].sum()
        st.metric("Total Pengeluaran", format_rupiah(expense_total))
    
    with col_net:
        net = income_total - expense_total
        st.metric("Saldo Bersih", format_rupiah(net))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ─── Transaction Table ────────────────────────────────────────────────
    if not df_display.empty:
        df_display["jumlah_fmt"] = df_display.apply(
            lambda r: f"{'+ ' if r['tipe']=='Pemasukan' else '- '}{format_rupiah(r['jumlah'])}", axis=1
        )
        df_display["tanggal_fmt"] = pd.to_datetime(df_display["tanggal"]).dt.strftime("%d %b %Y")
        
        display_final = df_display[["tanggal_fmt", "deskripsi", "kategori", "tipe", "jumlah_fmt"]].copy()
        display_final.columns = ["Tanggal", "Deskripsi", "Kategori", "Tipe", "Jumlah"]
        
        st.dataframe(
            display_final,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Tipe": st.column_config.TextColumn(width="small"),
                "Jumlah": st.column_config.TextColumn(width="medium"),
            }
        )
    else:
        st.info("Tidak ada transaksi yang sesuai dengan filter.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: EXPORT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sb-section-title">📥 Download & Export</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📊 Data Transaksi")
        csv = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️  Download CSV",
            data=csv,
            file_name="transaksi_smartbudget.csv",
            mime="text/csv",
        )
    
    with col2:
        st.subheader("📈 Ringkasan Kategori")
        kategori_export = get_pengeluaran_per_kategori(df_filtered)
        if not kategori_export.empty:
            csv_kat = kategori_export.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️  Download CSV",
                data=csv_kat,
                file_name="kategori_summary.csv",
                mime="text/csv",
            )
    
    with col3:
        st.subheader("📅 Tren Bulanan")
        tren_export = get_tren_bulanan(df_filtered)
        if not tren_export.empty:
            csv_tren = tren_export.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️  Download CSV",
                data=csv_tren,
                file_name="tren_bulanan.csv",
                mime="text/csv",
            )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 Gunakan CSV untuk analisis lebih lanjut di Excel, Google Sheets, atau tools lainnya.")
