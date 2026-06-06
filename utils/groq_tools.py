"""
utils/groq_tools.py
Agentic AI tools untuk chatbot AI Advisor menggunakan Groq API.
👤 Dikerjakan oleh: Ketua

2 Tools wajib (agentic system):
  1. analyze_spending()         — ambil & analisis data transaksi real-time
  2. get_budget_recommendation() — hasilkan rekomendasi penghematan

Cara pakai Groq API:
- Install: pip install groq
- API key: simpan di .streamlit/secrets.toml → GROQ_API_KEY = "..."
- Model: llama-3.1-8b-instant (free tier: 14.400 req/hari)
"""

import streamlit as st
import pandas as pd
import json
from groq import Groq
from utils.data_utils import (
    load_transactions,
    get_summary,
    get_pengeluaran_per_kategori,
    get_tren_bulanan,
    get_context_for_ai,
    format_rupiah,
)

# ─── Inisialisasi Groq Client ──────────────────────────────────────────────────
def get_groq_client() -> Groq:
    """Buat Groq client menggunakan API key dari Streamlit secrets."""
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        raise ValueError("GROQ_API_KEY tidak ditemukan di .streamlit/secrets.toml")
    return Groq(api_key=api_key)


# ─── Tool 1: Analyze Spending ─────────────────────────────────────────────────
def analyze_spending(df: pd.DataFrame = None) -> str:
    """
    Tool 1 (Wajib) — Ambil dan analisis data transaksi user secara real-time.

    Fungsi ini dipanggil oleh AI ketika user bertanya tentang pola pengeluaran.
    Return string yang akan dikirim ke LLM sebagai konteks.

    Args:
        df: DataFrame transaksi (jika None, akan load dari file)

    Returns:
        String analisis yang bisa dipahami LLM
    """
    if df is None:
        df = load_transactions()

    if df.empty:
        return "Tidak ada data transaksi yang tersedia untuk dianalisis."

    summary = get_summary(df)
    kategori_df = get_pengeluaran_per_kategori(df)
    tren_df = get_tren_bulanan(df)

    # Hitung bulan dengan pengeluaran tertinggi
    pengeluaran_per_bulan = tren_df.sort_values("pengeluaran", ascending=False)

    # Kategori terboros
    top_kategori = kategori_df.head(3)["kategori"].tolist() if not kategori_df.empty else []

    # Deteksi kondisi keuangan
    saldo = summary["saldo"]
    rata_harian = summary["rata_pengeluaran_harian"]

    kondisi = "SEHAT ✅" if saldo > 0 else "DEFISIT ⚠️"

    analysis = f"""
=== HASIL ANALISIS PENGELUARAN ===

KONDISI KEUANGAN: {kondisi}

RINGKASAN:
- Total Pemasukan: {format_rupiah(summary['total_pemasukan'])}
- Total Pengeluaran: {format_rupiah(summary['total_pengeluaran'])}
- Saldo Bersih: {format_rupiah(saldo)}
- Rata-rata Pengeluaran Harian: {format_rupiah(rata_harian)}
- Total Transaksi: {summary['jumlah_transaksi']}

KATEGORI PENGELUARAN TERBESAR:
"""
    for _, row in kategori_df.iterrows():
        pct = (row["jumlah"] / summary["total_pengeluaran"] * 100) if summary["total_pengeluaran"] > 0 else 0
        analysis += f"  - {row['kategori']}: {format_rupiah(row['jumlah'])} ({pct:.1f}%)\n"

    if not tren_df.empty:
        analysis += f"\nTREN BULANAN TERAKHIR:\n"
        for _, row in tren_df.tail(3).iterrows():
            analysis += f"  - {row['bulan']}: Masuk {format_rupiah(row['pemasukan'])}, Keluar {format_rupiah(row['pengeluaran'])}, Saldo {format_rupiah(row['saldo'])}\n"

    if top_kategori:
        analysis += f"\nKATEGORI PALING BOROS: {', '.join(top_kategori)}"

    return analysis.strip()


# ─── Tool 2: Get Budget Recommendation ────────────────────────────────────────
def get_budget_recommendation(df: pd.DataFrame = None) -> str:
    """
    Tool 2 (Wajib) — Hasilkan rekomendasi penghematan berdasarkan pola pengeluaran.

    Fungsi ini dipanggil AI ketika user meminta saran atau rekomendasi keuangan.

    Args:
        df: DataFrame transaksi (jika None, akan load dari file)

    Returns:
        String rekomendasi yang akan dikirim ke LLM
    """
    if df is None:
        df = load_transactions()

    if df.empty:
        return "Belum ada data transaksi untuk dibuat rekomendasi."

    summary = get_summary(df)
    kategori_df = get_pengeluaran_per_kategori(df)

    recommendations = ["=== REKOMENDASI ANGGARAN ===\n"]

    total_pengeluaran = summary["total_pengeluaran"]
    total_pemasukan = summary["total_pemasukan"]

    # Rule-based recommendations berdasarkan pola umum
    if total_pengeluaran > 0 and total_pemasukan > 0:
        rasio = total_pengeluaran / total_pemasukan

        if rasio > 0.9:
            recommendations.append(
                "⚠️ PRIORITAS TINGGI: Pengeluaranmu melebihi 90% pemasukan. "
                "Segera kurangi pengeluaran tidak perlu!"
            )
        elif rasio > 0.7:
            recommendations.append(
                "📊 Pengeluaranmu 70-90% dari pemasukan. "
                "Targetkan menurunkan ke bawah 70% untuk tabungan lebih baik."
            )
        else:
            recommendations.append(
                "✅ Rasio pengeluaran vs pemasukan sudah baik (di bawah 70%). "
                "Pertahankan dan tingkatkan tabungan!"
            )

    # Rekomendasi per kategori
    if not kategori_df.empty:
        recommendations.append("\nREKOMENDASI PER KATEGORI:")
        for _, row in kategori_df.iterrows():
            kategori = row["kategori"]
            jumlah = row["jumlah"]
            pct = (jumlah / total_pengeluaran * 100) if total_pengeluaran > 0 else 0

            if kategori == "Makanan & Minuman" and pct > 40:
                recommendations.append(
                    f"  🍱 {kategori} ({pct:.0f}%): Terlalu tinggi. "
                    "Coba masak sendiri atau cari warung lebih terjangkau. Target: < 30%"
                )
            elif kategori == "Hiburan" and pct > 15:
                recommendations.append(
                    f"  🎮 {kategori} ({pct:.0f}%): Pertimbangkan batasi budget hiburan maks 10%. "
                    f"Potensi hemat: {format_rupiah(jumlah * 0.3)}/bulan"
                )
            elif kategori == "Transportasi" and pct > 20:
                recommendations.append(
                    f"  🚌 {kategori} ({pct:.0f}%): Coba transportasi umum atau gabung teman. "
                    f"Potensi hemat hingga 40%."
                )
            elif kategori == "Belanja" and pct > 20:
                recommendations.append(
                    f"  🛍️ {kategori} ({pct:.0f}%): Terapkan aturan 'tunggu 24 jam' sebelum beli. "
                    "Bedakan kebutuhan vs keinginan."
                )

    # Saran tabungan
    saldo = summary["saldo"]
    if saldo > 0:
        target_tabungan = total_pemasukan * 0.2
        recommendations.append(
            f"\n💰 TARGET TABUNGAN: Sisihkan minimal 20% pemasukan = {format_rupiah(target_tabungan)}/bulan. "
            f"Saldo saat ini: {format_rupiah(saldo)}"
        )
    else:
        recommendations.append(
            f"\n🚨 DEFISIT: Keuanganmu minus {format_rupiah(abs(saldo))}. "
            "Prioritas utama: kurangi pengeluaran sebelum memikirkan tabungan."
        )

    return "\n".join(recommendations)


# ─── System Prompt AI Advisor ─────────────────────────────────────────────────
SYSTEM_PROMPT = """Kamu adalah SmartBudget AI Advisor, asisten keuangan pribadi untuk mahasiswa Indonesia.

PERANMU:
- Bantu mahasiswa memahami pola keuangan mereka
- Berikan rekomendasi penghematan yang praktis dan realistis
- Motivasi user untuk membangun kebiasaan keuangan yang sehat
- Jawab dalam Bahasa Indonesia yang ramah dan mudah dipahami

PANDUAN MENJAWAB:
- Gunakan data keuangan user yang diberikan sebagai konteks
- Berikan saran spesifik berdasarkan data, bukan saran generik
- Gunakan emoji secukupnya agar respons lebih engaging
- Jika ada pertanyaan non-keuangan, arahkan kembali ke topik keuangan
- Respons maksimal 200-300 kata, ringkas dan actionable

INGAT:
- Kamu bukan penasihat keuangan profesional, disclaimer jika diperlukan
- Saran disesuaikan dengan konteks mahasiswa (budget terbatas, uang saku/beasiswa)
"""


# ─── Main Chat Function ────────────────────────────────────────────────────────
def chat_with_advisor(
    user_input: str,
    chat_history: list,
    df: pd.DataFrame,
) -> str:
    """
    Fungsi utama chatbot AI Advisor.

    Alur agentic:
    1. Cek apakah perlu memanggil tool (analyze_spending / get_budget_recommendation)
    2. Jalankan tool jika perlu, tambahkan hasilnya ke konteks
    3. Kirim ke Groq API untuk generate respons final

    Args:
        user_input: Pertanyaan user
        chat_history: Riwayat chat sebelumnya (list of dict {role, content})
        df: DataFrame transaksi user

    Returns:
        String respons dari AI
    """
    client = get_groq_client()

    # ─── Tentukan tool yang perlu dipanggil ─────────────────────────────────
    # Keyword matching sederhana untuk trigger tools
    lower_input = user_input.lower()

    tool_results = []

    # Tool 1: analyze_spending
    keywords_analyze = [
        "analisis", "pola", "pengeluaran", "kondisi", "sehat",
        "boros", "terbesar", "kategori", "berapa", "statistik",
        "summary", "ringkasan", "overview"
    ]
    if any(kw in lower_input for kw in keywords_analyze):
        analysis_result = analyze_spending(df)
        tool_results.append(f"[HASIL TOOL: analyze_spending]\n{analysis_result}")

    # Tool 2: get_budget_recommendation
    keywords_recommend = [
        "rekomendasi", "saran", "hemat", "kurangi", "tips",
        "cara", "strategi", "bagaimana", "solusi", "perbaiki",
        "tabungan", "budget", "anggaran"
    ]
    if any(kw in lower_input for kw in keywords_recommend):
        recommendation_result = get_budget_recommendation(df)
        tool_results.append(f"[HASIL TOOL: get_budget_recommendation]\n{recommendation_result}")

    # Jika tidak ada tool terpanggil, tetap kirim konteks dasar
    if not tool_results:
        basic_context = get_context_for_ai(df)
        tool_results.append(f"[DATA KEUANGAN USER]\n{basic_context}")

    # ─── Bangun messages untuk Groq API ────────────────────────────────────
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Tambah riwayat chat (maksimal 10 pesan terakhir untuk efisiensi token)
    for msg in chat_history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Gabungkan tool results ke user message
    tool_context = "\n\n".join(tool_results)
    full_user_message = f"{user_input}\n\n---\n{tool_context}"

    messages.append({"role": "user", "content": full_user_message})

    # ─── Panggil Groq API ───────────────────────────────────────────────────
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )

    return response.choices[0].message.content
