"""
pages/2_Input_Transaksi.py
Halaman Input, Edit, dan Hapus Transaksi — UI/UX didesain ulang.
"""

import streamlit as st
import pandas as pd
from datetime import date
import math
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
from styles import GLOBAL_CSS
from components.sidebar import render_sidebar

# ─── Setup ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Input Transaksi | SmartBudget AI", page_icon="➕", layout="wide")
init_session_state()
render_sidebar()
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# Extra styles untuk halaman ini
st.markdown("""
<style>
.tipe-selector {display:flex;gap:8px;margin-bottom:4px;}
.tipe-card {
    flex:1;padding:12px;border:2px solid #e2e8f0;border-radius:10px;
    text-align:center;cursor:pointer;transition:all 0.15s;background:#fff;
}
.tipe-card.out.selected {border-color:#ef4444;background:#fff5f5;}
.tipe-card.in.selected {border-color:#22c55e;background:#f0fdf4;}
.tipe-icon {font-size:1.4rem;margin-bottom:4px;}
.tipe-label {font-size:0.8rem;font-weight:600;}
</style>
""", unsafe_allow_html=True)

# ─── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="sb-page-header">
    <h1>➕ Input Transaksi</h1>
    <p>Catat semua pemasukan dan pengeluaranmu di sini.</p>
</div>
""", unsafe_allow_html=True)

# ─── Form Tambah Transaksi ─────────────────────────────────────────────────────
with st.expander("➕  Tambah Transaksi Baru", expanded=True):
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_form1, col_form2 = st.columns(2, gap="large")
    
    with col_form1:
        tipe = st.radio(
            "Tipe Transaksi",
            ["📤 Pengeluaran", "📥 Pemasukan"],
            horizontal=True,
        )
        tipe_clean = "Pengeluaran" if "Pengeluaran" in tipe else "Pemasukan"
        
        tanggal = st.date_input(
            "Tanggal Transaksi",
            value=date.today(),
            max_value=date.today(),
        )
        
        jumlah = st.number_input(
            "Jumlah (Rp)",
            min_value=0,
            step=1000,
            format="%d",
            help="Masukkan nominal dalam Rupiah",
            placeholder="0",
        )
        
        # Preview format rupiah
        if jumlah > 0:
            st.markdown(f"""
            <div style="background:#f0fdf4;border:1px solid #86efac;border-radius:8px;padding:8px 12px;font-size:0.85rem;color:#166534;margin-top:-8px">
                ✓ <strong>{format_rupiah(jumlah)}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    with col_form2:
        kat_list = KATEGORI_PENGELUARAN if tipe_clean == "Pengeluaran" else KATEGORI_PEMASUKAN
        kategori = st.selectbox("Kategori", kat_list)
        
        deskripsi = st.text_input(
            "Deskripsi",
            placeholder="Contoh: Makan siang di kantin",
            help="Jelaskan transaksi secara singkat",
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        submitted = st.button(
            "💾  Simpan Transaksi",
            type="primary",
            use_container_width=True,
        )
    
    if submitted:
        if jumlah <= 0:
            st.error("⚠️ Jumlah harus lebih dari 0!")
        elif not deskripsi.strip():
            st.error("⚠️ Deskripsi tidak boleh kosong!")
        else:
            success = add_transaction(tanggal, deskripsi, jumlah, tipe_clean, kategori)
            if success:
                st.success(f"✅ Transaksi **{deskripsi}** sebesar **{format_rupiah(jumlah)}** berhasil disimpan!")
                st.rerun()
            else:
                st.error("❌ Gagal menyimpan transaksi. Silakan coba lagi.")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabel Transaksi ───────────────────────────────────────────────────────────
st.markdown('<div class="sb-section-title">📋 Semua Transaksi</div>', unsafe_allow_html=True)

df = load_transactions()

if df.empty:
    st.markdown("""
    <div style="background:#fff;border:1px dashed #cbd5e1;border-radius:12px;padding:3rem;text-align:center">
        <div style="font-size:2.5rem;margin-bottom:10px">📭</div>
        <div style="font-size:0.95rem;font-weight:600;color:#334155;margin-bottom:4px">Belum ada transaksi</div>
        <div style="font-size:0.825rem;color:#94a3b8">Tambahkan transaksi pertamamu di form di atas!</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Search & Filter Bar ───────────────────────────────────────────────────────
col_search, col_tipe_filter, col_info = st.columns([3, 2, 1])
with col_search:
    search = st.text_input(
        "Cari",
        placeholder="🔍  Cari deskripsi atau kategori...",
        label_visibility="collapsed",
    )
with col_tipe_filter:
    tipe_filter_opt = st.selectbox(
        "Filter Tipe",
        ["Semua", "Pemasukan", "Pengeluaran"],
        label_visibility="collapsed",
    )

df_sorted = df.sort_values("tanggal", ascending=False).reset_index(drop=True)
if search:
    df_sorted = df_sorted[
        df_sorted["deskripsi"].str.contains(search, case=False, na=False) |
        df_sorted["kategori"].str.contains(search, case=False, na=False)
    ]
if tipe_filter_opt != "Semua":
    df_sorted = df_sorted[df_sorted["tipe"] == tipe_filter_opt]

with col_info:
    st.markdown(f"""
    <div style="height:38px;display:flex;align-items:center;font-size:0.8rem;color:#94a3b8">
        {len(df_sorted)} transaksi
    </div>
    """, unsafe_allow_html=True)

# ─── Pagination ────────────────────────────────────────────────────────────────
PAGE_SIZE = 10
total_rows = len(df_sorted)
total_pages = max(1, math.ceil(total_rows / PAGE_SIZE))

if "tx_page" not in st.session_state:
    st.session_state["tx_page"] = 0
st.session_state["tx_page"] = max(0, min(st.session_state["tx_page"], total_pages - 1))
page = st.session_state["tx_page"]
start = page * PAGE_SIZE
end = start + PAGE_SIZE
df_page = df_sorted.iloc[start:end]

# ─── Table Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px 10px 0 0;padding:8px 0;display:grid;grid-template-columns:120px 1fr 140px 150px 100px 90px;gap:0">
    <div style="padding:0 12px;font-size:0.72rem;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.05em">Tanggal</div>
    <div style="padding:0 12px;font-size:0.72rem;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.05em">Deskripsi</div>
    <div style="padding:0 12px;font-size:0.72rem;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.05em">Kategori</div>
    <div style="padding:0 12px;font-size:0.72rem;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.05em">Jumlah</div>
    <div style="padding:0 12px;font-size:0.72rem;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.05em">Tipe</div>
    <div style="padding:0 12px;font-size:0.72rem;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.05em">Aksi</div>
</div>
""", unsafe_allow_html=True)

# ─── Table Rows ────────────────────────────────────────────────────────────────
st.markdown('<div style="border:1px solid #e2e8f0;border-top:none;border-radius:0 0 10px 10px;overflow:hidden;background:#fff;">', unsafe_allow_html=True)

for i, (_, row) in enumerate(df_page.iterrows()):
    rid = int(row["id"]) if ("id" in row and pd.notnull(row["id"])) else int(start + i)
    
    tipe_icon = "📥" if row["tipe"] == "Pemasukan" else "📤"
    jumlah_color = "#16a34a" if row["tipe"] == "Pemasukan" else "#dc2626"
    jumlah_prefix = "+" if row["tipe"] == "Pemasukan" else "-"
    badge_style = "background:#dcfce7;color:#166534;" if row["tipe"] == "Pemasukan" else "background:#fee2e2;color:#991b1b;"
    row_bg = "#ffffff" if i % 2 == 0 else "#fafafa"
    
    col1, col2, col3, col4, col5, col6 = st.columns([1.5, 3, 2, 2, 1.5, 1.5])
    
    with col1:
        st.markdown(
            f'<div style="font-size:0.8rem;color:#64748b;padding:10px 4px">{str(row["tanggal"])[:10]}</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div style="font-size:0.875rem;color:#334155;padding:10px 4px;font-weight:500">{row["deskripsi"]}</div>',
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f'<div style="padding:10px 4px"><span style="font-size:0.75rem;background:#f1f5f9;color:#64748b;padding:3px 8px;border-radius:20px">{row["kategori"]}</span></div>',
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f'<div style="font-size:0.875rem;font-weight:600;color:{jumlah_color};padding:10px 4px">{jumlah_prefix}{format_rupiah(row["jumlah"])}</div>',
            unsafe_allow_html=True
        )
    with col5:
        st.markdown(
            f'<div style="padding:10px 4px"><span style="font-size:0.72rem;font-weight:600;padding:3px 8px;border-radius:20px;{badge_style}">{tipe_icon} {row["tipe"]}</span></div>',
            unsafe_allow_html=True
        )
    with col6:
        c_edit, c_del = st.columns(2)
        with c_edit:
            if st.button("✏️", key=f"edit_{rid}", help="Edit transaksi"):
                st.session_state[f"edit_mode_{rid}"] = True
        with c_del:
            if st.button("🗑️", key=f"del_{rid}", help="Hapus transaksi"):
                if delete_transaction(rid):
                    st.toast("Transaksi dihapus!", icon="✅")
                    st.rerun()
    
    # ─── Edit Form ─────────────────────────────────────────────────────────────
    if st.session_state.get(f"edit_mode_{rid}", False):
        st.markdown(f"""
        <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;padding:1rem;margin:4px 0 8px">
            <div style="font-size:0.85rem;font-weight:600;color:#0f4c81;margin-bottom:12px">✏️ Edit Transaksi ID {rid}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form(key=f"form_edit_{rid}"):
            ec1, ec2 = st.columns(2)
            with ec1:
                e_tipe = st.radio(
                    "Tipe",
                    ["Pengeluaran", "Pemasukan"],
                    index=0 if row["tipe"] == "Pengeluaran" else 1,
                    key=f"et_{rid}",
                    horizontal=True,
                )
                e_tanggal = st.date_input("Tanggal", value=pd.Timestamp(row["tanggal"]).date(), key=f"etanggal_{rid}")
                e_jumlah = st.number_input("Jumlah (Rp)", value=float(row["jumlah"]), min_value=0.0, step=1000.0, key=f"ejumlah_{rid}")
            with ec2:
                kat_list = KATEGORI_PENGELUARAN if e_tipe == "Pengeluaran" else KATEGORI_PEMASUKAN
                default_idx = kat_list.index(row["kategori"]) if row["kategori"] in kat_list else 0
                e_kategori = st.selectbox("Kategori", kat_list, index=default_idx, key=f"ekat_{rid}")
                e_deskripsi = st.text_input("Deskripsi", value=row["deskripsi"], key=f"edesc_{rid}")
            
            col_save, col_cancel = st.columns(2)
            with col_save:
                save_edit = st.form_submit_button("💾 Simpan Perubahan", type="primary", use_container_width=True)
            with col_cancel:
                cancel_edit = st.form_submit_button("❌ Batal", use_container_width=True)
            
            if save_edit:
                update_transaction(rid, e_tanggal, e_deskripsi, e_jumlah, e_tipe, e_kategori)
                st.session_state[f"edit_mode_{rid}"] = False
                st.rerun()
            if cancel_edit:
                st.session_state[f"edit_mode_{rid}"] = False
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ─── Pagination Controls ───────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
nav_l, nav_back, nav_mid, nav_next, nav_r = st.columns([3, 1.2, 0.8, 1.2, 3])

with nav_back:
    if st.button("← Sebelumnya", disabled=(page == 0), use_container_width=True):
        st.session_state["tx_page"] -= 1
        st.rerun()

with nav_mid:
    st.markdown(
        f'<div style="text-align:center;padding:8px 0;font-size:0.8rem;color:#64748b;font-weight:500">{page+1}/{total_pages}</div>',
        unsafe_allow_html=True
    )

with nav_next:
    if st.button("Berikutnya →", disabled=(page >= total_pages - 1), use_container_width=True):
        st.session_state["tx_page"] += 1
        st.rerun()