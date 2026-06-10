"""
pages/4_Prediksi.py
Halaman Prediksi Keuangan — UI/UX didesain ulang.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_utils import (
    init_session_state,
    load_transactions,
    get_tren_bulanan,
    format_rupiah,
)
from utils.predictor_utils import predict_future
from styles import GLOBAL_CSS, PLOTLY_THEME
from components.sidebar import render_sidebar
from utils.init_styles import apply_global_styles

# ─── Setup ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Prediksi | SmartBudget AI", page_icon="🔮", layout="centered")
init_session_state()
render_sidebar()
apply_global_styles()

# ─── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="sb-page-header">
    <h1>🔮 Prediksi Keuangan</h1>
    <p>Proyeksi kondisi keuangan berdasarkan histori transaksi.</p>
</div>
""", unsafe_allow_html=True)

df = load_transactions()

if df.empty:
    st.markdown("""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:3rem;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
        <div style="font-size:3rem;margin-bottom:12px">📭</div>
        <div style="font-size:1rem;font-weight:600;color:#0a1628">Belum ada data transaksi</div>
        <div style="font-size:0.875rem;color:#64748b">Tambahkan data terlebih dahulu untuk melihat prediksi.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Controls ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:1rem 1.25rem;margin-bottom:1.25rem;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    target = st.radio(
        "Prediksi Target",
        ["Pengeluaran", "Pemasukan", "Saldo"],
        horizontal=True,
    )
with col2:
    horizon = st.slider("Jumlah Bulan Prediksi", 1, 6, 3)

st.markdown("</div>", unsafe_allow_html=True)

tren_df = get_tren_bulanan(df)

if len(tren_df) < 2:
    st.warning("⚠️ Minimal diperlukan data dari 2 bulan berbeda untuk melakukan prediksi.")
    st.stop()

predictions = predict_future(df=df, horizon=horizon, target=target)

# ─── Financial Health Score ────────────────────────────────────────────────────
latest = tren_df.iloc[-1]
saldo = latest["saldo"]
pemasukan = latest["pemasukan"]
pengeluaran = latest["pengeluaran"]

score = 100
if pemasukan > 0:
    spending_ratio = pengeluaran / pemasukan
    if spending_ratio > 1:
        score -= 40
    elif spending_ratio > 0.8:
        score -= 20
if saldo < 0:
    score -= 30
volatility = predictions["volatility"].iloc[0]
if volatility > 30:
    score -= 15
elif volatility > 20:
    score -= 10
score = max(score, 0)

score_color = "#22c55e" if score >= 70 else ("#f59e0b" if score >= 40 else "#ef4444")
score_label = "Sangat Sehat 🟢" if score >= 80 else ("Sehat 🟡" if score >= 60 else ("Perlu Perhatian 🟠" if score >= 40 else "Berbahaya 🔴"))
score_pct = score / 100

st.markdown(f"""
<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1.25rem;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
    <div style="display:flex;align-items:center;gap:1.5rem">
        <div style="position:relative;width:80px;height:80px;flex-shrink:0">
            <svg viewBox="0 0 80 80" width="80" height="80">
                <circle cx="40" cy="40" r="32" fill="none" stroke="#f1f5f9" stroke-width="10"/>
                <circle cx="40" cy="40" r="32" fill="none" stroke="{score_color}" stroke-width="10"
                    stroke-dasharray="{201.06}" stroke-dashoffset="{201.06 * (1 - score_pct)}"
                    stroke-linecap="round" transform="rotate(-90 40 40)"/>
                <text x="40" y="44" text-anchor="middle" font-size="16" font-weight="700" fill="#0a1628">{score}</text>
            </svg>
        </div>
        <div style="flex:1">
            <div style="font-size:0.72rem;color:#94a3b8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px">Financial Health Score</div>
            <div style="font-size:1.2rem;font-weight:700;color:#0a1628;margin-bottom:6px">{score_label}</div>
            <div style="background:#f1f5f9;border-radius:6px;height:8px;overflow:hidden">
                <div style="width:{score}%;height:100%;background:{score_color};border-radius:6px;transition:width 0.4s ease"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:0.7rem;color:#94a3b8;margin-top:4px"><span>0</span><span>50</span><span>100</span></div>
        </div>
        <div style="text-align:right">
            <div style="font-size:0.72rem;color:#94a3b8;margin-bottom:3px">Volatilitas</div>
            <div style="font-size:1.1rem;font-weight:700;color:{'#22c55e' if volatility < 15 else '#f59e0b'}">{volatility:.1f}%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Scenario Cards ────────────────────────────────────────────────────────────
bulan_terdekat = predictions.iloc[0]

col_pes, col_nor, col_opt = st.columns(3, gap="medium")

with col_pes:
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #fca5a5;border-radius:12px;padding:1.2rem;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,0.04)">
        <div style="font-size:0.7rem;color:#94a3b8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px">📉 Skenario Pesimis</div>
        <div style="font-size:1.3rem;font-weight:700;color:#dc2626;margin-bottom:4px">{format_rupiah(bulan_terdekat['pesimis'])}</div>
        <div style="font-size:0.75rem;color:#94a3b8">{bulan_terdekat['bulan']}</div>
    </div>
    """, unsafe_allow_html=True)

with col_nor:
    st.markdown(f"""
    <div style="background:#eff6ff;border:2px solid #93c5fd;border-radius:12px;padding:1.2rem;text-align:center;box-shadow:0 2px 8px rgba(30,106,179,0.1)">
        <div style="font-size:0.7rem;color:#1e6ab3;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px">📊 Skenario Normal</div>
        <div style="font-size:1.3rem;font-weight:700;color:#0f4c81;margin-bottom:4px">{format_rupiah(bulan_terdekat['normal'])}</div>
        <div style="font-size:0.75rem;color:#1e6ab3;font-weight:500">{bulan_terdekat['bulan']}</div>
    </div>
    """, unsafe_allow_html=True)

with col_opt:
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #86efac;border-radius:12px;padding:1.2rem;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,0.04)">
        <div style="font-size:0.7rem;color:#94a3b8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px">📈 Skenario Optimis</div>
        <div style="font-size:1.3rem;font-weight:700;color:#16a34a;margin-bottom:4px">{format_rupiah(bulan_terdekat['optimis'])}</div>
        <div style="font-size:0.75rem;color:#94a3b8">{bulan_terdekat['bulan']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Grafik Historis & Prediksi ────────────────────────────────────────────────
st.markdown('<div class="sb-section-title">📈 Grafik Historis & Prediksi</div>', unsafe_allow_html=True)

mapping = {"Pengeluaran": "pengeluaran", "Pemasukan": "pemasukan", "Saldo": "saldo"}
hist_col = mapping[target]

fig = go.Figure()

# Historis
fig.add_trace(go.Scatter(
    x=tren_df["bulan"],
    y=tren_df[hist_col],
    mode="lines+markers",
    name="Historis",
    line=dict(color="#1e6ab3", width=2.5),
    marker=dict(size=7, color="#1e6ab3"),
))

# Prediksi Normal
fig.add_trace(go.Scatter(
    x=predictions["bulan"],
    y=predictions["normal"],
    mode="lines+markers",
    name="Prediksi Normal",
    line=dict(color="#0f4c81", width=2, dash="dash"),
    marker=dict(size=6, color="#0f4c81", symbol="diamond"),
))

# Confidence Band (area antara pesimis dan optimis)
fig.add_trace(go.Scatter(
    x=list(predictions["bulan"]) + list(predictions["bulan"])[::-1],
    y=list(predictions["optimis"]) + list(predictions["pesimis"])[::-1],
    fill="toself",
    fillcolor="rgba(30,106,179,0.08)",
    line=dict(color="rgba(0,0,0,0)"),
    name="Rentang Skenario",
    hoverinfo="skip",
))

# Pesimis & Optimis lines
fig.add_trace(go.Scatter(
    x=predictions["bulan"],
    y=predictions["pesimis"],
    mode="lines",
    name="Pesimis",
    line=dict(color="#ef4444", width=1.5, dash="dot"),
))

fig.add_trace(go.Scatter(
    x=predictions["bulan"],
    y=predictions["optimis"],
    mode="lines",
    name="Optimis",
    line=dict(color="#22c55e", width=1.5, dash="dot"),
))

# Vertical line separator
# if len(tren_df) > 0 and len(predictions) > 0:
#     fig.add_vline(
#         x=tren_df["bulan"].iloc[-1],
#         line_dash="dot",
#         line_color="#94a3b8",
#         line_width=1,
#         annotation_text="  Mulai Prediksi",
#         annotation_font_size=11,
#         annotation_font_color="#64748b",
#     )
# Vertical line separator
if len(tren_df) > 0 and len(predictions) > 0:

    last_month = tren_df["bulan"].iloc[-1]

    fig.add_shape(
        type="line",
        x0=last_month,
        x1=last_month,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(
            color="#94a3b8",
            dash="dot",
            width=1,
        ),
    )

    fig.add_annotation(
        x=last_month,
        y=1,
        yref="paper",
        text="Mulai Prediksi",
        showarrow=False,
        yshift=10,
        font=dict(
            size=11,
            color="#64748b",
        ),
    )

# fig.update_layout(
#     **PLOTLY_THEME,
#     height=380,
#     hovermode="x unified",
#     xaxis_title="",
#     yaxis_title=f"{target} (Rp)",
#     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
# )
fig.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    height=380,
    hovermode="x unified",
    xaxis_title="",
    yaxis_title=f"{target} (Rp)",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ),
)
fig.update_xaxes(showgrid=False)
fig.update_yaxes(gridcolor="#e2e8f0", gridwidth=0.5)

st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

# ─── Analisis & Insight ────────────────────────────────────────────────────────
col_analisis, col_tips = st.columns(2, gap="medium")

with col_analisis:
    st.markdown('<div class="sb-section-title">🧠 Analisis</div>', unsafe_allow_html=True)
    
    if volatility < 10:
        st.success(f"✅ Kondisi keuangan **sangat stabil**. Perubahan rata-rata antar bulan hanya ~{volatility:.1f}%.")
    elif volatility < 20:
        st.info(f"ℹ️ Kondisi keuangan **cukup stabil** dengan perubahan sekitar {volatility:.1f}% setiap bulan.")
    elif volatility < 30:
        st.warning(f"⚠️ Kondisi mulai **berfluktuasi**. Perubahan bulanan mencapai ~{volatility:.1f}%.")
    else:
        st.error(f"🚨 Kondisi keuangan **kurang stabil**. Perubahan bulanan cukup besar: ~{volatility:.1f}%.")
    
    current_value = tren_df[hist_col].iloc[-1]
    future_value = predictions["normal"].iloc[0]
    
    if current_value > 0:
        pct_change = ((future_value - current_value) / current_value) * 100
        if pct_change > 10:
            st.warning(f"📈 {target} diperkirakan **meningkat {pct_change:.1f}%** dibanding periode terakhir.")
        elif pct_change < -10:
            st.success(f"📉 {target} diperkirakan **menurun {abs(pct_change):.1f}%** dibanding periode terakhir.")
        else:
            st.info(f"↔️ {target} diperkirakan **relatif stabil** (±{abs(pct_change):.1f}%).")
    
    if target == "Saldo":
        pesimis = predictions["pesimis"].iloc[0]
        if pesimis < 0:
            st.error("⚠️ Pada skenario pesimis, saldo **berpotensi negatif**. Kurangi pengeluaran!")
        else:
            st.success("✅ Bahkan skenario pesimis, saldo masih di **zona aman**.")

with col_tips:
    st.markdown('<div class="sb-section-title">💡 Rekomendasi</div>', unsafe_allow_html=True)
    
    current_value = tren_df[hist_col].iloc[-1]
    future_value = predictions["normal"].iloc[0]
    pct_change = ((future_value - current_value) / current_value * 100) if current_value > 0 else 0
    
    tips = []
    if target == "Pengeluaran":
        if pct_change > 10:
            tips = [
                f"Pengeluaran diperkirakan naik {pct_change:.1f}% — perlu perhatian!",
                "Tinjau pengeluaran non-prioritas minggu ini.",
                "Tetapkan batas anggaran harian/mingguan.",
                "Evaluasi kategori dengan pengeluaran terbesar.",
            ]
        elif pct_change < -10:
            tips = [
                f"Pengeluaran diperkirakan turun {abs(pct_change):.1f}% — kabar baik!",
                "Pertahankan kebiasaan finansial saat ini.",
                "Alokasikan dana yang dihemat ke tabungan.",
            ]
        else:
            tips = ["Pengeluaran relatif stabil.", "Lakukan evaluasi anggaran secara berkala."]
    elif target == "Pemasukan":
        if pct_change > 10:
            tips = [f"Pemasukan diperkirakan naik {pct_change:.1f}%!", "Tambah porsi tabungan atau investasi.", "Siapkan dana darurat lebih besar."]
        elif pct_change < -10:
            tips = [f"Pemasukan diperkirakan turun {abs(pct_change):.1f}%.", "Kurangi pengeluaran tidak mendesak.", "Cari sumber pemasukan tambahan."]
        else:
            tips = ["Pemasukan relatif stabil.", "Fokus meningkatkan rasio tabungan."]
    elif target == "Saldo":
        if future_value < 0:
            tips = ["Saldo diprediksi negatif — prioritas utama!", "Kurangi pengeluaran konsumtif segera.", "Cari sumber penghasilan tambahan."]
        elif pct_change > 10:
            tips = [f"Saldo diperkirakan meningkat {pct_change:.1f}%!", "Pertimbangkan investasi jangka panjang.", "Sisihkan surplus ke rekening tabungan."]
        else:
            tips = ["Saldo relatif stabil.", "Pertahankan strategi keuangan saat ini."]
    
    for tip in tips:
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:8px;padding:8px 0;border-bottom:1px solid #f1f5f9">
            <span style="color:#1e6ab3;flex-shrink:0;margin-top:1px">→</span>
            <span style="font-size:0.875rem;color:#334155">{tip}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabel Detail Prediksi ─────────────────────────────────────────────────────
with st.expander("📋 Tabel Detail Prediksi", expanded=False):
    display_df = predictions.copy()
    display_df["pesimis"] = display_df["pesimis"].apply(format_rupiah)
    display_df["normal"] = display_df["normal"].apply(format_rupiah)
    display_df["optimis"] = display_df["optimis"].apply(format_rupiah)
    display_df = display_df.rename(columns={
        "bulan": "Bulan",
        "pesimis": "Skenario Pesimis",
        "normal": "Skenario Normal",
        "optimis": "Skenario Optimis",
    })
    st.dataframe(display_df[["Bulan", "Skenario Pesimis", "Skenario Normal", "Skenario Optimis"]], width='stretch', hide_index=True)