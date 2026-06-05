"""
utils/data_utils.py
Shared utility functions untuk manajemen data transaksi.
Digunakan oleh semua halaman Streamlit.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime, date

# ─── Konstanta ─────────────────────────────────────────────────────────────────
DATA_PATH = "data/dataset_transaksi.csv"

KATEGORI_PENGELUARAN = [
    "Makanan & Minuman",
    "Transportasi",
    "Pendidikan",
    "Hiburan",
    "Kesehatan",
    "Belanja",
    "Tagihan & Utilitas",
    "Lainnya",
]

KATEGORI_PEMASUKAN = [
    "Uang Saku",
    "Beasiswa",
    "Freelance / Part-time",
    "Hadiah",
    "Lainnya",
]

KOLOM_WAJIB = ["id", "tanggal", "deskripsi", "jumlah", "tipe", "kategori"]


# ─── Session State ─────────────────────────────────────────────────────────────
def init_session_state():
    """Inisialisasi semua session state yang dibutuhkan aplikasi."""
    if "transactions" not in st.session_state:
        st.session_state.transactions = load_transactions()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = datetime.now()


# ─── Load & Save Data ──────────────────────────────────────────────────────────
def load_transactions() -> pd.DataFrame:
    """
    Load data transaksi dari CSV.
    Jika file tidak ada, kembalikan DataFrame kosong dengan kolom yang benar.
    """
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_csv(DATA_PATH, parse_dates=["tanggal"])
            # Pastikan semua kolom wajib ada
            for col in KOLOM_WAJIB:
                if col not in df.columns:
                    df[col] = None
            return df
        except Exception as e:
            st.error(f"Error membaca data: {e}")
            return _empty_dataframe()
    return _empty_dataframe()


def save_transactions(df: pd.DataFrame) -> bool:
    """
    Simpan DataFrame transaksi ke CSV.
    Return True jika berhasil, False jika gagal.
    """
    try:
        os.makedirs("data", exist_ok=True)
        df.to_csv(DATA_PATH, index=False)
        # Update session state
        st.session_state.transactions = df
        return True
    except Exception as e:
        st.error(f"Error menyimpan data: {e}")
        return False


def _empty_dataframe() -> pd.DataFrame:
    """Kembalikan DataFrame kosong dengan struktur kolom yang benar."""
    return pd.DataFrame(columns=KOLOM_WAJIB)


# ─── CRUD Transaksi ────────────────────────────────────────────────────────────
def add_transaction(
    tanggal: date,
    deskripsi: str,
    jumlah: float,
    tipe: str,
    kategori: str,
) -> bool:
    """
    Tambah transaksi baru ke dataset.

    Args:
        tanggal: Tanggal transaksi
        deskripsi: Deskripsi / keterangan transaksi
        jumlah: Nominal (selalu positif)
        tipe: 'Pemasukan' atau 'Pengeluaran'
        kategori: Kategori transaksi

    Returns:
        True jika berhasil disimpan
    """
    df = load_transactions()

    new_id = int(df["id"].max()) + 1 if not df.empty and df["id"].notna().any() else 1

    new_row = pd.DataFrame([{
        "id": new_id,
        "tanggal": pd.Timestamp(tanggal),
        "deskripsi": deskripsi.strip(),
        "jumlah": abs(jumlah),
        "tipe": tipe,
        "kategori": kategori,
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    return save_transactions(df)


def delete_transaction(transaction_id: int) -> bool:
    """Hapus transaksi berdasarkan ID."""
    df = load_transactions()
    df = df[df["id"] != transaction_id]
    return save_transactions(df)


def update_transaction(
    transaction_id: int,
    tanggal: date,
    deskripsi: str,
    jumlah: float,
    tipe: str,
    kategori: str,
) -> bool:
    """Update transaksi yang sudah ada berdasarkan ID."""
    df = load_transactions()
    mask = df["id"] == transaction_id
    if not mask.any():
        return False

    df.loc[mask, "tanggal"] = pd.Timestamp(tanggal)
    df.loc[mask, "deskripsi"] = deskripsi.strip()
    df.loc[mask, "jumlah"] = abs(jumlah)
    df.loc[mask, "tipe"] = tipe
    df.loc[mask, "kategori"] = kategori

    return save_transactions(df)


# ─── Analisis & Agregasi ───────────────────────────────────────────────────────
def get_summary(df: pd.DataFrame) -> dict:
    """
    Hitung ringkasan keuangan dari DataFrame transaksi.

    Returns:
        dict dengan keys: total_pemasukan, total_pengeluaran, saldo,
        jumlah_transaksi, rata_pengeluaran_harian
    """
    if df.empty:
        return {
            "total_pemasukan": 0,
            "total_pengeluaran": 0,
            "saldo": 0,
            "jumlah_transaksi": 0,
            "rata_pengeluaran_harian": 0,
        }

    pemasukan = df[df["tipe"] == "Pemasukan"]["jumlah"].sum()
    pengeluaran = df[df["tipe"] == "Pengeluaran"]["jumlah"].sum()

    # Rata pengeluaran harian (hanya hari yang ada transaksi)
    pengeluaran_df = df[df["tipe"] == "Pengeluaran"]
    if not pengeluaran_df.empty:
        hari_unik = pengeluaran_df["tanggal"].dt.date.nunique()
        rata_harian = pengeluaran / max(hari_unik, 1)
    else:
        rata_harian = 0

    return {
        "total_pemasukan": pemasukan,
        "total_pengeluaran": pengeluaran,
        "saldo": pemasukan - pengeluaran,
        "jumlah_transaksi": len(df),
        "rata_pengeluaran_harian": rata_harian,
    }


def get_pengeluaran_per_kategori(df: pd.DataFrame) -> pd.DataFrame:
    """Agregasi pengeluaran per kategori, diurutkan descending."""
    pengeluaran = df[df["tipe"] == "Pengeluaran"]
    if pengeluaran.empty:
        return pd.DataFrame(columns=["kategori", "jumlah"])
    return (
        pengeluaran.groupby("kategori")["jumlah"]
        .sum()
        .reset_index()
        .sort_values("jumlah", ascending=False)
    )


def get_tren_bulanan(df: pd.DataFrame) -> pd.DataFrame:
    """
    Hitung tren pemasukan & pengeluaran per bulan.

    Returns:
        DataFrame dengan kolom: bulan, pemasukan, pengeluaran, saldo
    """
    if df.empty:
        return pd.DataFrame(columns=["bulan", "pemasukan", "pengeluaran", "saldo"])

    df = df.copy()
    df["bulan"] = df["tanggal"].dt.to_period("M").astype(str)

    tren = df.pivot_table(
        index="bulan",
        columns="tipe",
        values="jumlah",
        aggfunc="sum",
        fill_value=0,
    ).reset_index()

    # Pastikan kedua kolom ada
    if "Pemasukan" not in tren.columns:
        tren["Pemasukan"] = 0
    if "Pengeluaran" not in tren.columns:
        tren["Pengeluaran"] = 0

    tren = tren.rename(columns={"Pemasukan": "pemasukan", "Pengeluaran": "pengeluaran"})
    tren["saldo"] = tren["pemasukan"] - tren["pengeluaran"]

    return tren.sort_values("bulan")


def format_rupiah(angka: float) -> str:
    """Format angka ke format Rupiah Indonesia."""
    return f"Rp {angka:,.0f}".replace(",", ".")


def filter_by_period(df: pd.DataFrame, periode: str) -> pd.DataFrame:
    """
    Filter DataFrame berdasarkan periode waktu.

    Args:
        df: DataFrame transaksi
        periode: '7 Hari', '30 Hari', '3 Bulan', '6 Bulan', 'Semua'
    """
    if df.empty or periode == "Semua":
        return df

    today = pd.Timestamp.now()
    period_map = {
        "7 Hari": today - pd.Timedelta(days=7),
        "30 Hari": today - pd.Timedelta(days=30),
        "3 Bulan": today - pd.Timedelta(days=90),
        "6 Bulan": today - pd.Timedelta(days=180),
    }

    cutoff = period_map.get(periode, today - pd.Timedelta(days=30))
    return df[df["tanggal"] >= cutoff]


# ─── Data untuk AI Advisor ─────────────────────────────────────────────────────
def get_context_for_ai(df: pd.DataFrame) -> str:
    """
    Buat ringkasan data transaksi dalam format teks untuk dikirim ke AI.
    Digunakan oleh groq_tools.py (tools chatbot).

    Returns:
        String ringkasan yang bisa dipahami LLM
    """
    if df.empty:
        return "Belum ada data transaksi yang tersedia."

    summary = get_summary(df)
    kategori_df = get_pengeluaran_per_kategori(df)

    lines = [
        f"=== RINGKASAN KEUANGAN ===",
        f"Total Pemasukan: {format_rupiah(summary['total_pemasukan'])}",
        f"Total Pengeluaran: {format_rupiah(summary['total_pengeluaran'])}",
        f"Saldo: {format_rupiah(summary['saldo'])}",
        f"Jumlah Transaksi: {summary['jumlah_transaksi']}",
        f"Rata-rata Pengeluaran Harian: {format_rupiah(summary['rata_pengeluaran_harian'])}",
        "",
        "=== PENGELUARAN PER KATEGORI ===",
    ]

    for _, row in kategori_df.iterrows():
        lines.append(f"- {row['kategori']}: {format_rupiah(row['jumlah'])}")

    # Transaksi terbaru (10 terakhir)
    recent = df.sort_values("tanggal", ascending=False).head(10)
    lines.append("")
    lines.append("=== 10 TRANSAKSI TERAKHIR ===")
    for _, row in recent.iterrows():
        tanggal_str = row["tanggal"].strftime("%d %b %Y") if pd.notna(row["tanggal"]) else "?"
        lines.append(
            f"[{tanggal_str}] {row['tipe']} | {row['kategori']} | "
            f"{row['deskripsi']} | {format_rupiah(row['jumlah'])}"
        )

    return "\n".join(lines)
