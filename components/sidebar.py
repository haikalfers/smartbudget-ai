import streamlit as st
from utils.data_utils import load_transactions

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding: 8px 0 16px;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
                <div style="width:36px;height:36px;background:linear-gradient(135deg,#1e6ab3,#0f4c81);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px">💰</div>
                <div>
                    <div style="font-size:1.1rem;font-weight:700;color:#fff">SmartBudget AI</div>
                    <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);margin-top:1px">Kelola keuangan dengan cerdas</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        transactions = load_transactions()
        if not transactions.empty:
            total_pemasukan = transactions[transactions["tipe"] == "Pemasukan"]["jumlah"].sum()
            total_pengeluaran = transactions[transactions["tipe"] == "Pengeluaran"]["jumlah"].sum()
            saldo = total_pemasukan - total_pengeluaran
            saldo_color = "#4ade80" if saldo >= 0 else "#f87171"

            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.08);border-radius:10px;padding:14px;margin-bottom:8px">
                <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px">Saldo Saat Ini</div>
                <div style="font-size:1.6rem;font-weight:700;color:{saldo_color}">Rp {saldo:,.0f}</div>
                <div style="display:flex;justify-content:space-between;margin-top:10px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.1)">
                    <div>
                        <div style="font-size:0.68rem;color:rgba(255,255,255,0.45)">↑ Masuk</div>
                        <div style="font-size:0.8rem;color:#4ade80;font-weight:600">Rp {total_pemasukan:,.0f}</div>
                    </div>
                    <div>
                        <div style="font-size:0.68rem;color:rgba(255,255,255,0.45)">↓ Keluar</div>
                        <div style="font-size:0.8rem;color:#f87171;font-weight:600">Rp {total_pengeluaran:,.0f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(255,255,255,0.08);border-radius:10px;padding:14px;text-align:center;margin-bottom:8px">
                <div style="font-size:1.5rem;margin-bottom:6px">📭</div>
                <div style="font-size:0.8rem;color:rgba(255,255,255,0.6)">Belum ada transaksi</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:20px">
            <div style="font-size:0.68rem;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;padding:0 4px">Menu</div>
        </div>
        """, unsafe_allow_html=True)

        # Use page_link for native navigation
        try:
            st.page_link("app.py", label="🏠  Beranda", use_container_width=True)
            st.page_link("pages/1_Dashboard.py", label="📊  Dashboard", use_container_width=True)
            st.page_link("pages/2_Input_Transaksi.py", label="➕  Input Transaksi", use_container_width=True)
            st.page_link("pages/3_Analisis.py", label="📈  Analisis", use_container_width=True)
            st.page_link("pages/4_Prediksi.py", label="🔮  Prediksi", use_container_width=True)
            st.page_link("pages/5_AI_Advisor.py", label="💬  AI Advisor", use_container_width=True)
        except Exception:
            # Fallback rendering (if st.page_link not available)
            links = [
                ("🏠  Beranda", "app.py"),
                ("📊  Dashboard", "pages/1_Dashboard.py"),
                ("➕  Input Transaksi", "pages/2_Input_Transaksi.py"),
                ("📈  Analisis", "pages/3_Analisis.py"),
                ("🔮  Prediksi", "pages/4_Prediksi.py"),
                ("💬  AI Advisor", "pages/5_AI_Advisor.py"),
            ]
            for label, path in links:
                st.markdown(f"<div style='margin:6px 0'><a href='?page={path}' style='text-decoration:none;color:inherit;padding:8px 10px;display:block;border-radius:8px;background:rgba(255,255,255,0.02)'>{label}</a></div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("""
        <div style="font-size:0.7rem;color:rgba(255,255,255,0.3);text-align:center;padding:4px 0">
            SmartBudget AI v2.0<br>Studi Independen Data Science
        </div>
        """, unsafe_allow_html=True)