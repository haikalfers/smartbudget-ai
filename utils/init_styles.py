"""
utils/init_styles.py
Utility untuk memastikan CSS global dan sidebar styling di-load di setiap halaman.
Harus dipanggil di app.py dan semua pages/ untuk konsistensi visual.
"""

import streamlit as st
from styles import GLOBAL_CSS


def apply_global_styles():
    """
    Apply CSS global ke current halaman.
    Pastikan sidebar dan semua komponen styling berjalan konsisten di semua halaman.
    """
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def init_page():
    """
    Initialize halaman dengan setup lengkap.
    Harus dipanggil di awal setiap page (tepat setelah st.set_page_config).
    """
    apply_global_styles()
    # Session state sudah di-init di app.py, tidak perlu di-repeat di pages
    # Tapi bisa di-check di sini untuk safety
    if "transactions" not in st.session_state:
        from utils.data_utils import init_session_state
        init_session_state()
