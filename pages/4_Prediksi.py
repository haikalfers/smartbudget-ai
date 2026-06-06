import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.data_utils import (
    init_session_state,
    load_transactions,
    get_tren_bulanan,
    format_rupiah,
)

from utils.predictor_utils import predict_future

st.set_page_config(
    page_title="Prediksi | SmartBudget AI",
    page_icon="🔮",
    layout="wide"
)

init_session_state()

st.title("🔮 Prediksi Keuangan")
st.markdown(
    "Proyeksi kondisi keuangan berdasarkan histori transaksi."
)

df = load_transactions()

if df.empty:
    st.warning("Belum ada data transaksi.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    target = st.radio(
        "Prediksi",
        ["Pengeluaran", "Pemasukan", "Saldo"],
        horizontal=True
    )

with col2:
    horizon = st.slider(
        "Jumlah bulan prediksi",
        1,
        6,
        3
    )

tren_df = get_tren_bulanan(df)

if len(tren_df) < 2:
    st.warning(
        "Minimal diperlukan data dari 2 bulan berbeda untuk melakukan prediksi."
    )
    st.stop()

predictions = predict_future(
    df=df,
    horizon=horizon,
    target=target
)


st.subheader("🏆 Financial Health Score")

latest = tren_df.iloc[-1]

saldo = latest["saldo"]
pemasukan = latest["pemasukan"]
pengeluaran = latest["pengeluaran"]

score = 100

if pemasukan > 0:

    spending_ratio = (
        pengeluaran / pemasukan
    )

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

st.metric(
    "Financial Health",
    f"{score}/100"
)


mapping = {
    "Pengeluaran": "pengeluaran",
    "Pemasukan": "pemasukan",
    "Saldo": "saldo"
}

hist_col = mapping[target]

st.subheader("📈 Grafik Historis dan Prediksi")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=tren_df["bulan"],
        y=tren_df[hist_col],
        mode="lines+markers",
        name="Historis"
    )
)

fig.add_trace(
    go.Scatter(
        x=predictions["bulan"],
        y=predictions["normal"],
        mode="lines+markers",
        name="Prediksi Normal"
    )
)

fig.add_trace(
    go.Scatter(
        x=predictions["bulan"],
        y=predictions["pesimis"],
        mode="lines",
        name="Skenario Pesimis",
        line=dict(dash="dot")
    )
)

fig.add_trace(
    go.Scatter(
        x=predictions["bulan"],
        y=predictions["optimis"],
        mode="lines",
        name="Skenario Optimis",
        line=dict(dash="dash")
    )
)

fig.update_layout(
    height=550,
    hovermode="x unified",
    xaxis_title="Bulan",
    yaxis_title="Nominal (Rp)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("📋 Detail Prediksi")

display_df = predictions.copy()

display_df["pesimis"] = display_df["pesimis"].apply(format_rupiah)
display_df["normal"] = display_df["normal"].apply(format_rupiah)
display_df["optimis"] = display_df["optimis"].apply(format_rupiah)

st.dataframe(
    display_df,
    use_container_width=True
)

st.subheader("🤖 Ringkasan Prediksi")

bulan_terdekat = predictions.iloc[0]

st.info(
    f"""
Bulan: {bulan_terdekat['bulan']}

• Skenario Pesimis: {format_rupiah(bulan_terdekat['pesimis'])}

• Skenario Normal: {format_rupiah(bulan_terdekat['normal'])}

• Skenario Optimis: {format_rupiah(bulan_terdekat['optimis'])}
"""
)

st.subheader("🧠 Analisis Prediksi")

volatility = predictions["volatility"].iloc[0]

if volatility < 10:

    st.success(
        f"Kondisi keuangan sangat stabil. Perubahan rata-rata antar bulan hanya sekitar {volatility:.1f}%."
    )

elif volatility < 20:

    st.info(
        f"Kondisi keuangan cukup stabil dengan perubahan sekitar {volatility:.1f}% setiap bulan."
    )

elif volatility < 30:

    st.warning(
        f"Kondisi keuangan mulai berfluktuasi. Perubahan bulanan mencapai sekitar {volatility:.1f}%."
    )

else:

    st.error(
        f"Kondisi keuangan kurang stabil. Perubahan bulanan cukup besar, sekitar {volatility:.1f}%."
    )
    
current_value = tren_df[hist_col].iloc[-1]
future_value = predictions["normal"].iloc[0]

if current_value > 0:

    pct_change = (
        (future_value - current_value)
        / current_value
    ) * 100

    st.subheader("📊 Insight")

    if pct_change > 10:

        st.warning(
            f"{target} diperkirakan meningkat {pct_change:.1f}% dibanding periode terakhir."
        )

    elif pct_change < -10:

        st.success(
            f"{target} diperkirakan menurun {abs(pct_change):.1f}% dibanding periode terakhir."
        )

    else:

        st.info(
            f"{target} diperkirakan relatif stabil."
        )

if target == "Saldo":

    pesimis = predictions["pesimis"].iloc[0]

    st.subheader("⚠️ Analisis Risiko")

    if pesimis < 0:

        st.error(
            "Pada skenario pesimis, saldo berpotensi negatif. Disarankan mengurangi pengeluaran atau meningkatkan pemasukan."
        )

    else:

        st.success(
            "Bahkan pada skenario pesimis, kondisi saldo masih berada di zona aman."
        )

st.subheader("💡 Rekomendasi Berdasarkan Prediksi")

tips = []

if current_value > 0:
    pct_change = (
        (future_value - current_value)
        / current_value
    ) * 100
else:
    pct_change = 0

if target == "Pengeluaran":

    if pct_change > 10:

        tips.extend([
            f"Pengeluaran diperkirakan naik {pct_change:.1f}%.",
            "Tinjau kembali pengeluaran non-prioritas.",
            "Tetapkan batas anggaran mingguan.",
            "Evaluasi kategori dengan pengeluaran terbesar."
        ])

    elif pct_change < -10:

        tips.extend([
            f"Pengeluaran diperkirakan turun {abs(pct_change):.1f}%.",
            "Pertahankan kebiasaan finansial saat ini.",
            "Alokasikan dana yang dihemat ke tabungan."
        ])

    else:

        tips.extend([
            "Pengeluaran relatif stabil.",
            "Lakukan evaluasi anggaran secara berkala."
        ])

elif target == "Pemasukan":

    if pct_change > 10:

        tips.extend([
            f"Pemasukan diperkirakan naik {pct_change:.1f}%.",
            "Pertimbangkan menambah porsi tabungan.",
            "Siapkan dana darurat lebih besar."
        ])

    elif pct_change < -10:

        tips.extend([
            f"Pemasukan diperkirakan turun {abs(pct_change):.1f}%.",
            "Kurangi pengeluaran yang tidak mendesak.",
            "Cari sumber pemasukan tambahan."
        ])

    else:

        tips.extend([
            "Pemasukan relatif stabil.",
            "Fokus meningkatkan rasio tabungan."
        ])

elif target == "Saldo":

    if future_value < 0:

        tips.extend([
            "Saldo diprediksi negatif.",
            "Prioritaskan kebutuhan utama.",
            "Kurangi pengeluaran konsumtif.",
            "Perkuat dana darurat."
        ])

    elif pct_change > 10:

        tips.extend([
            f"Saldo diperkirakan meningkat {pct_change:.1f}%.",
            "Pertimbangkan investasi jangka panjang.",
            "Sisihkan sebagian surplus ke tabungan."
        ])

    elif pct_change < -10:

        tips.extend([
            f"Saldo diperkirakan turun {abs(pct_change):.1f}%.",
            "Perhatikan keseimbangan pemasukan dan pengeluaran.",
            "Kurangi biaya rutin yang tidak esensial."
        ])

    else:

        tips.extend([
            "Saldo relatif stabil.",
            "Pertahankan strategi keuangan saat ini."
        ])

for tip in tips:
    st.markdown(f"• {tip}")
