"""
pages/2_Input_Transaksi.py
Halaman untuk input, edit, dan hapus transaksi keuangan.
👤 Dikerjakan oleh: Member 3
"""

import streamlit as st
import pandas as pd
from datetime import date
from utils.data_utils import (
    init_session_state,
    load_transactions,
    add_transaction,
    delete_transaction,
    update_transaction,
    format_rupiah,
    KATEGORI_PENGELUARAN,
    KATEGORI_PEMASUKAN,
)
import math

# ─── Setup ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Input Transaksi | SmartBudget AI", page_icon="➕", layout="wide")
init_session_state()

st.title("➕ Input Transaksi")
st.markdown("Catat semua pemasukan dan pengeluaranmu di sini.")

# ─── Form Input Transaksi Baru ─────────────────────────────────────────────────
with st.expander("➕ Tambah Transaksi Baru", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        tipe = st.radio("Tipe Transaksi", ["Pengeluaran", "Pemasukan"], horizontal=True)
        tanggal = st.date_input("Tanggal", value=date.today(), max_value=date.today())
        jumlah = st.number_input(
            "Jumlah (Rp)", min_value=0, step=1000, format="%d",
            help="Masukkan nominal dalam Rupiah"
        )

    with col2:
        # Kategori dinamis berdasarkan tipe
        if tipe == "Pengeluaran":
            # Jika Member 1 sudah deploy model klasifikasi, deskripsi bisa auto-classify
            # Untuk sekarang, user pilih manual
            kategori = st.selectbox("Kategori", KATEGORI_PENGELUARAN)
        else:
            kategori = st.selectbox("Kategori", KATEGORI_PEMASUKAN)

        deskripsi = st.text_input("Deskripsi", placeholder="Contoh: Makan siang di kantin")

    submitted = st.button("💾 Simpan Transaksi", type="primary", use_container_width=True)

    if submitted:
        if jumlah <= 0:
            st.error("⚠️ Jumlah harus lebih dari 0!")
        elif not deskripsi.strip():
            st.error("⚠️ Deskripsi tidak boleh kosong!")
        else:
            success = add_transaction(tanggal, deskripsi, jumlah, tipe, kategori)
            if success:
                st.success(f"✅ Transaksi **{deskripsi}** sebesar **{format_rupiah(jumlah)}** berhasil disimpan!")
                st.rerun()
            else:
                st.error("❌ Gagal menyimpan transaksi. Silakan coba lagi.")

st.divider()

# ─── Tabel Semua Transaksi (dengan Edit & Hapus) ───────────────────────────────
st.subheader("📋 Semua Transaksi")

df = load_transactions()

if df.empty:
    st.info("📭 Belum ada transaksi. Tambahkan transaksi pertamamu di atas!")
    st.stop()

# Filter pencarian
search = st.text_input("🔍 Cari transaksi...", placeholder="Ketik nama atau kategori")
if search:
    df = df[
        df["deskripsi"].str.contains(search, case=False, na=False) |
        df["kategori"].str.contains(search, case=False, na=False)
    ]

# Tampilkan tabel (pagination)
df_sorted = df.sort_values("tanggal", ascending=False).reset_index(drop=True)

# Setup paging
PAGE_SIZE = 10
total_rows = len(df_sorted)
total_pages = math.ceil(total_rows / PAGE_SIZE)

if "tx_page" not in st.session_state:
    st.session_state["tx_page"] = 0
# Clamp page
st.session_state["tx_page"] = max(0, min(st.session_state["tx_page"], max(0, total_pages - 1)))
page = st.session_state["tx_page"]
start = page * PAGE_SIZE
end = start + PAGE_SIZE

# Replace Controls: info + navigation (move navigation below table)
# Tampilkan hanya info jumlah di atas; tombol navigasi dipindah ke bawah tabel agar berada di bawah 10 baris
col_info = st.columns([1])[0]
col_info.write(f"Menampilkan {min(start+1, total_rows)}–{min(end, total_rows)} dari {total_rows} transaksi")

# Header tabel (kolom)
h1, h2, h3, h4, h5, h6 = st.columns([2, 3, 2, 2, 1.5, 1.5])
with h1:
    st.caption("Tanggal")
with h2:
    st.caption("Deskripsi")
with h3:
    st.caption("Kategori")
with h4:
    st.caption("Jumlah")
with h5:
    st.caption("Edit")
with h6:
    st.caption("Hapus")

# Slice page
df_page = df_sorted.iloc[start:end]

# Ganti loop agar selalu punya id unik (fallback ke indeks jika kolom 'id' kosong)
for i, (_, row) in enumerate(df_page.iterrows()):
    # Jika ada kolom 'id' dan nilainya tidak null, pakai itu; kalau tidak, pakai indeks global sebagai id unik
    rid = int(row["id"]) if ("id" in row and pd.notnull(row["id"])) else int(start + i)

    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 2, 2, 1.5, 1.5])

        tipe_icon = "📥" if row["tipe"] == "Pemasukan" else "📤"
        tipe_color = "green" if row["tipe"] == "Pemasukan" else "red"

        with col1:
            st.caption(str(row["tanggal"])[:10])
        with col2:
            st.write(row["deskripsi"])
        with col3:
            st.caption(row["kategori"])
        with col4:
            st.markdown(f"<span style='color:{tipe_color}'>{tipe_icon} {format_rupiah(row['jumlah'])}</span>", unsafe_allow_html=True)
        with col5:
            # Edit button — buka modal/expander
            if st.button("✏️ Edit", key=f"edit_{rid}"):
                st.session_state[f"edit_mode_{rid}"] = True
        with col6:
            if st.button("🗑️ Hapus", key=f"del_{rid}"):
                if delete_transaction(rid):
                    st.success("Transaksi dihapus!")
                    st.rerun()

        # Edit form (muncul jika tombol Edit diklik)
        if st.session_state.get(f"edit_mode_{rid}", False):
            with st.form(key=f"form_edit_{rid}"):
                st.markdown(f"**Edit Transaksi ID {rid}**")
                ec1, ec2 = st.columns(2)
                with ec1:
                    e_tipe = st.radio("Tipe", ["Pengeluaran", "Pemasukan"],
                                      index=0 if row["tipe"] == "Pengeluaran" else 1,
                                      key=f"et_{rid}", horizontal=True)
                    e_tanggal = st.date_input("Tanggal", value=pd.Timestamp(row["tanggal"]).date(),
                                              key=f"etanggal_{rid}")
                    e_jumlah = st.number_input("Jumlah (Rp)", value=float(row["jumlah"]),
                                               min_value=0.0, step=1000.0, key=f"ejumlah_{rid}")
                with ec2:
                    kat_list = KATEGORI_PENGELUARAN if e_tipe == "Pengeluaran" else KATEGORI_PEMASUKAN
                    default_idx = kat_list.index(row["kategori"]) if row["kategori"] in kat_list else 0
                    e_kategori = st.selectbox("Kategori", kat_list, index=default_idx, key=f"ekat_{rid}")
                    e_deskripsi = st.text_input("Deskripsi", value=row["deskripsi"], key=f"edesc_{rid}")

                save_col, cancel_col = st.columns(2)
                with save_col:
                    save_edit = st.form_submit_button("💾 Simpan Perubahan", type="primary")
                with cancel_col:
                    cancel_edit = st.form_submit_button("❌ Batal")

                if save_edit:
                    update_transaction(rid, e_tanggal, e_deskripsi, e_jumlah, e_tipe, e_kategori)
                    st.session_state[f"edit_mode_{rid}"] = False
                    st.rerun()
                if cancel_edit:
                    st.session_state[f"edit_mode_{rid}"] = False
                    st.rerun()

    st.divider()

# ─── Navigation (pindah ke bawah tabel) ────────────────────────────────────────
# Tombol Back / Next ditempatkan pada satu baris dan disejajarkan di tengah
st.markdown("")  # spacer
nav_left, nav_back, nav_center, nav_next, nav_right = st.columns([3,1.2,0.6,1.2,3])

with nav_back:
    if st.button("⬅️ Back", key="tx_prev"):
        if st.session_state["tx_page"] > 0:
            st.session_state["tx_page"] -= 1
            st.rerun()

with nav_next:
    if st.button("Next ➡️", key="tx_next"):
        if st.session_state["tx_page"] < total_pages - 1:
            st.session_state["tx_page"] += 1
            st.rerun()

# Tampilkan indikator halaman sedikit di bawah / di sisi tombol (rapi)
st.markdown(f"<div style='text-align:center; margin-top:6px;'>Halaman <strong>{page+1}</strong> dari <strong>{max(1,total_pages)}</strong></div>", unsafe_allow_html=True)
