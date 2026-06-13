"""
pages/4_AI_Advisor.py
Halaman Chatbot AI Advisor — UI/UX didesain ulang.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_utils import (
    init_session_state,
    load_transactions,
    get_context_for_ai,
    format_rupiah,
    get_summary,
)
from utils.chat_history_utils import (
    load_chat_history,
    save_chat_history,
    clear_chat_history,
)
from styles import GLOBAL_CSS
from components.sidebar import render_sidebar
from utils.init_styles import apply_global_styles

# ─── Setup ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Advisor | SmartBudget AI", page_icon="💬", layout="centered")
init_session_state()
render_sidebar()
apply_global_styles()

# Extra styles khusus halaman ini
st.markdown("""
<style>
.quick-btn-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin-bottom: 1.25rem;
}
.chat-container {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.25rem;
    min-height: 420px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    margin-bottom: 0.75rem;
}
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 6px 0 !important;
}
[data-testid="stChatMessage"][data-testid*="user"] > div {
    background: #eff6ff !important;
    border-radius: 12px 12px 4px 12px !important;
    padding: 10px 14px !important;
}
[data-testid="stChatMessageContent"] {
    font-size: 0.9rem !important;
    line-height: 1.65 !important;
}
.stChatInputContainer {
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
}
.context-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.25rem;
    font-size: 0.825rem;
    color: #64748b;
    font-family: 'DM Mono', monospace;
    white-space: pre-wrap;
    max-height: 180px;
    overflow-y: auto;
}
.history-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #0a1628;
    margin: 1rem 0 10px 0;
    display: flex;
    align-items: center;
    gap: 6px;
}
.history-divider {
    border: none;
    border-top: 1px dashed #e2e8f0;
    margin: 6px 0;
}

/* Mobile Responsive */
@media (max-width: 768px) {
    .quick-btn-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 6px;
        margin-bottom: 1rem;
    }
    .chat-container {
        padding: 1rem;
        min-height: 320px;
    }
}

@media (max-width: 480px) {
    .quick-btn-grid {
        grid-template-columns: 1fr;
        gap: 6px;
    }
    .chat-container {
        padding: 0.85rem;
        min-height: 280px;
    }
}
</style>
""", unsafe_allow_html=True)

# ─── Chat History Init ─────────────────────────────────────────────────────────
if "chat_history" not in st.session_state or not st.session_state.chat_history:
    st.session_state.chat_history = load_chat_history()

# ─── Import AI Tools ───────────────────────────────────────────────────────────
try:
    from utils.groq_tools import (
        analyze_spending,
        get_budget_recommendation,
        chat_with_advisor,
    )
    GROQ_READY = True
except ImportError:
    GROQ_READY = False

# ─── Load Data ─────────────────────────────────────────────────────────────────
df = load_transactions()
summary = get_summary(df)

# ─── Layout: Main (chat) + Sidebar kanan (konteks) ────────────────────────────
col_main, col_side = st.columns([2.5, 1], gap="large")

with col_side:
    # ── Header Sidebar Kanan ───────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:0.85rem;font-weight:700;color:#0a1628;margin-bottom:10px">
        📊 Data Keuanganmu
    </div>
    """, unsafe_allow_html=True)

    # Metric mini cards
    saldo = summary["saldo"]
    saldo_color = "#16a34a" if saldo >= 0 else "#dc2626"

    st.markdown(f"""
    <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:1rem">
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:9px;padding:10px 12px;box-shadow:0 1px 2px rgba(0,0,0,0.04)">
            <div style="font-size:0.68rem;color:#94a3b8;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:3px">Saldo</div>
            <div style="font-size:1rem;font-weight:700;color:{saldo_color}">{format_rupiah(saldo)}</div>
        </div>
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:9px;padding:10px 12px;box-shadow:0 1px 2px rgba(0,0,0,0.04)">
            <div style="font-size:0.68rem;color:#94a3b8;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:3px">Pemasukan</div>
            <div style="font-size:1rem;font-weight:700;color:#16a34a">{format_rupiah(summary["total_pemasukan"])}</div>
        </div>
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:9px;padding:10px 12px;box-shadow:0 1px 2px rgba(0,0,0,0.04)">
            <div style="font-size:0.68rem;color:#94a3b8;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:3px">Pengeluaran</div>
            <div style="font-size:1rem;font-weight:700;color:#dc2626">{format_rupiah(summary["total_pengeluaran"])}</div>
        </div>
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:9px;padding:10px 12px;box-shadow:0 1px 2px rgba(0,0,0,0.04)">
            <div style="font-size:0.68rem;color:#94a3b8;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:3px">Total Transaksi</div>
            <div style="font-size:1rem;font-weight:700;color:#0a1628">{summary["jumlah_transaksi"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Status AI ──────────────────────────────────────────────────────────────
    if GROQ_READY:
        st.markdown("""
        <div style="background:#f0fdf4;border:1px solid #86efac;border-radius:9px;padding:10px 12px;margin-bottom:1rem">
            <div style="font-size:0.75rem;font-weight:600;color:#166534;display:flex;align-items:center;gap:5px">
                <span style="width:7px;height:7px;background:#22c55e;border-radius:50%;display:inline-block"></span>
                AI Advisor Aktif
            </div>
            <div style="font-size:0.72rem;margin-top:2px;color:#16a34a">Groq API terhubung</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#fef3c7;border:1px solid #fde047;border-radius:9px;padding:10px 12px;margin-bottom:1rem">
            <div style="font-size:0.75rem;font-weight:600;color:#92400e;display:flex;align-items:center;gap:5px">
                <span style="width:7px;height:7px;background:#f59e0b;border-radius:50%;display:inline-block"></span>
                Mode Demo
            </div>
            <div style="font-size:0.72rem;color:#92400e;margin-top:2px">Konfigurasi Groq API untuk mengaktifkan AI</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Konteks Data (collapsible) ─────────────────────────────────────────────
    with st.expander("🔍 Lihat Konteks Data AI", expanded=False):
        if df.empty:
            st.caption("Belum ada data transaksi.")
        else:
            st.code(get_context_for_ai(df), language=None)

    # ── Hapus Riwayat ──────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️  Hapus Riwayat Chat", use_container_width=True):
        st.session_state.chat_history = []
        clear_chat_history()
        st.toast("Riwayat chat dihapus!", icon="✅")
        st.rerun()

# ─── Main: Header + Input + Quick Actions + Riwayat ──────────────────────────
with col_main:
    st.markdown("""
    <div class="sb-page-header">
        <h1>💬 AI Financial Advisor</h1>
        <p>Tanyakan apa saja tentang keuanganmu — AI menganalisis datamu secara real-time.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── [1] Chat Input — PALING ATAS ──────────────────────────────────────────
    user_input = st.chat_input("Tanya tentang keuanganmu...")

    # ── [2] Quick Action Buttons ───────────────────────────────────────────────
    st.markdown('<div style="font-size:0.85rem;font-weight:600;color:#0a1628;margin-bottom:10px">⚡ Tanya Cepat</div>', unsafe_allow_html=True)

    quick_prompts = [
        ("📊", "Analisis pola pengeluaranku bulan ini"),
        ("💰", "Berikan rekomendasi penghematan untukku"),
        ("🔥", "Kategori apa yang paling boros?"),
        ("❤️", "Apakah kondisi keuanganku sehat?"),
    ]

    def process_prompt(prompt: str):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        save_chat_history(st.session_state.chat_history)

        if GROQ_READY and not df.empty:
            try:
                response = chat_with_advisor(
                    user_input=prompt,
                    chat_history=st.session_state.chat_history[:-1],
                    df=df,
                )
            except Exception as e:
                response = f"Terjadi error: {str(e)}"
        elif df.empty:
            response = (
                "Halo! Saya belum bisa memberikan analisis karena kamu belum memiliki "
                "data transaksi. Yuk mulai catat keuanganmu di halaman **Input Transaksi** terlebih dahulu! 📝"
            )
        else:
            response = (
                "Maaf, AI Advisor sedang dalam mode demo. "
                "Konfigurasi Groq API di `.streamlit/secrets.toml` untuk mengaktifkan fitur ini."
            )

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        save_chat_history(st.session_state.chat_history)
        st.rerun()

    q1, q2 = st.columns(2)
    q3, q4 = st.columns(2)

    for col, (icon, prompt) in zip([q1, q2, q3, q4], quick_prompts):
        with col:
            if st.button(
                f"{icon}  {prompt}",
                key=f"quick_{prompt[:15]}",
                use_container_width=True,
            ):
                process_prompt(prompt)

    # ── [3] Proses user_input dari chat_input ──────────────────────────────────
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        save_chat_history(st.session_state.chat_history)

        if not GROQ_READY:
            response = (
                "Maaf, AI Advisor sedang dalam mode demo. "
                "Konfigurasi Groq API di `.streamlit/secrets.toml` untuk mengaktifkan fitur ini."
            )
        elif df.empty:
            response = (
                "Halo! Saya belum bisa memberikan analisis karena kamu belum memiliki "
                "data transaksi. Yuk mulai catat keuanganmu di halaman **Input Transaksi** terlebih dahulu! 📝"
            )
        else:
            with st.spinner("AI sedang menganalisis keuanganmu..."):
                try:
                    response = chat_with_advisor(
                        user_input=user_input,
                        chat_history=st.session_state.chat_history[:-1],
                        df=df,
                    )
                except Exception as e:
                    response = f"Terjadi error: {str(e)}"

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        save_chat_history(st.session_state.chat_history)
        st.rerun()

    # ── [4] Riwayat Chat — TERBARU DI ATAS ────────────────────────────────────
    st.markdown('<div class="history-label">💬 Riwayat Chat <span style="font-size:0.75rem;font-weight:400;color:#94a3b8">(terbaru di atas)</span></div>', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:2.5rem;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
            <div style="font-size:2.5rem;margin-bottom:10px">🤖</div>
            <div style="font-size:0.95rem;font-weight:600;color:#0a1628;margin-bottom:6px">Halo! Saya AI Financial Advisor SmartBudget.</div>
            <div style="font-size:0.85rem;color:#64748b;line-height:1.7">
                Tanyakan apa saja tentang keuanganmu!<br>
                <span style="color:#94a3b8;font-style:italic">Contoh: "Kenapa pengeluaranku meningkat?" atau "Bagaimana cara hemat lebih banyak?"</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Pasangkan pesan user + assistant jadi satu pasang (pair),
        # lalu tampilkan dari pasang terbaru ke terlama.
        history = st.session_state.chat_history

        # Bangun list pasangan (user_msg, assistant_msg)
        pairs = []
        i = 0
        while i < len(history):
            if history[i]["role"] == "user":
                user_msg = history[i]
                assistant_msg = history[i + 1] if (i + 1 < len(history) and history[i + 1]["role"] == "assistant") else None
                pairs.append((user_msg, assistant_msg))
                i += 2 if assistant_msg else 1
            else:
                # assistant tanpa pasangan user (edge case)
                pairs.append((None, history[i]))
                i += 1

        # Tampilkan dari pasang terbaru ke terlama
        for idx, (user_msg, assistant_msg) in enumerate(reversed(pairs)):
            if idx > 0:
                st.markdown('<hr class="history-divider">', unsafe_allow_html=True)

            # Tampilkan assistant dulu (karena sudah dibalik, assistant = respons dari user di bawahnya)
            if assistant_msg:
                with st.chat_message("assistant"):
                    st.markdown(assistant_msg["content"])
            if user_msg:
                with st.chat_message("user"):
                    st.markdown(user_msg["content"])