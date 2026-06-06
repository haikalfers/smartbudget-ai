"""
pages/5_AI_Advisor.py
Halaman Chatbot AI Advisor dengan Groq API + 2 Tools (Agentic AI).
👤 Dikerjakan oleh: Ketua

INSTRUKSI KETUA:
- Buat utils/groq_tools.py dengan fungsi analyze_spending() dan get_budget_recommendation()
- Pastikan GROQ_API_KEY ada di .streamlit/secrets.toml
- Ini halaman inti yang menunjukkan agentic AI system (wajib untuk penilaian)
- Deadline internal: 13 Juni
"""

import streamlit as st
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
    clear_chat_history
)

# ─── Setup ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Advisor | SmartBudget AI", page_icon="💬", layout="wide")
init_session_state()

if "chat_history" not in st.session_state:

    st.session_state.chat_history = (
        load_chat_history()
    )

elif not st.session_state.chat_history:

    st.session_state.chat_history = (
        load_chat_history()
    )

st.title("💬 AI Financial Advisor")
st.markdown("Tanyakan apa saja tentang keuanganmu — AI akan menganalisis datamu secara real-time.")

# ─── Import Tools (Ketua isi ini) ──────────────────────────────────────────────
try:
    from utils.groq_tools import (
        analyze_spending,
        get_budget_recommendation,
        chat_with_advisor,
    )
    GROQ_READY = True
except ImportError:
    GROQ_READY = False

# ─── Tampilkan Ringkasan Konteks ───────────────────────────────────────────────
df = load_transactions()
summary = get_summary(df)

with st.expander("📊 Data keuanganmu yang dilihat AI", expanded=False):
    if df.empty:
        st.info("Belum ada data transaksi.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("💳 Saldo", format_rupiah(summary["saldo"]))
        col2.metric("📥 Pemasukan", format_rupiah(summary["total_pemasukan"]))
        col3.metric("📤 Pengeluaran", format_rupiah(summary["total_pengeluaran"]))
        st.text(get_context_for_ai(df))

st.divider()

# ─── Quick Action Buttons ──────────────────────────────────────────────────────
st.subheader("⚡ Tanya Cepat")
col1, col2, col3, col4 = st.columns(4)

quick_prompts = {
    col1: "Analisis pola pengeluaranku bulan ini",
    col2: "Berikan rekomendasi penghematan untukku",
    col3: "Kategori apa yang paling boros?",
    col4: "Apakah kondisi keuanganku sehat?",
}

# for col, prompt in quick_prompts.items():
#     with col:

#         if st.button(prompt, use_container_width=True):

#             st.session_state.chat_history.append({
#                 "role": "user",
#                 "content": prompt
#             })

#             if GROQ_READY and not df.empty:

#                 try:

#                     response = chat_with_advisor(
#                         user_input=prompt,
#                         chat_history=st.session_state.chat_history[:-1],
#                         df=df
#                     )

#                 except Exception as e:

#                     response = f"Terjadi error: {str(e)}"

#             elif df.empty:

#                 response = (
#                     "Belum ada data transaksi untuk dianalisis. "
#                     "Silakan tambahkan transaksi terlebih dahulu."
#                 )

#             else:

#                 response = (
#                     "AI Advisor belum siap digunakan. "
#                     "Periksa konfigurasi Groq API."
#                 )

#             st.session_state.chat_history.append({
#                 "role": "assistant",
#                 "content": response
#             })

#             st.rerun()

def process_prompt(prompt):

    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt
    })

    save_chat_history(
        st.session_state.chat_history
    )

    try:

        response = chat_with_advisor(
            user_input=prompt,
            chat_history=st.session_state.chat_history[:-1],
            df=df
        )

    except Exception as e:

        response = f"Terjadi error: {str(e)}"

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })

    save_chat_history(
        st.session_state.chat_history
    )

    st.rerun()

for idx, (col, prompt) in enumerate(
    quick_prompts.items()
):

    with col:

        if st.button(
            prompt,
            key=f"btn_{idx}_{prompt[:10]}",
            use_container_width=True
        ):
            process_prompt(prompt)
            
st.divider()

# ─── Chat Interface ────────────────────────────────────────────────────────────
st.subheader("💬 Chat")

# Tampilkan riwayat chat
chat_container = st.container()
with chat_container:
    if not st.session_state.chat_history:
        st.markdown("""
        <div style='text-align:center; color:#888; padding: 2rem;'>
            👋 Halo! Saya AI Financial Advisor SmartBudget.<br>
            Tanyakan apa saja tentang keuanganmu!<br><br>
            <i>Contoh: "Kenapa pengeluaranku meningkat?" atau "Bagaimana cara hemat lebih banyak?"</i>
        </div>
        """, unsafe_allow_html=True)

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ─── Input Chat ────────────────────────────────────────────────────────────────
user_input = st.chat_input("Tanya tentang keuanganmu...")

if user_input:
    # Tambah pesan user ke history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    save_chat_history(
        st.session_state.chat_history
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Proses respon AI
    with st.chat_message("assistant"):
        if not GROQ_READY:
            # Placeholder jika groq_tools.py belum dibuat
            st.warning("⚙️ **Ketua:** `utils/groq_tools.py` belum tersedia. Implementasikan fungsi chatbot di sana.")
            response = "Maaf, AI Advisor sedang dalam tahap pengembangan. Silakan cek kembali nanti."
        elif df.empty:
            response = (
                "Halo! Saya belum bisa memberikan analisis karena kamu belum memiliki data transaksi. "
                "Yuk mulai catat keuanganmu di halaman **Input Transaksi** terlebih dahulu! 📝"
            )
            st.markdown(response)
        else:
            # TODO Ketua: Panggil chat_with_advisor dari groq_tools.py
            # response = chat_with_advisor(
            #     user_input=user_input,
            #     chat_history=st.session_state.chat_history[:-1],
            #     df=df,
            # )
            with st.spinner("AI sedang menganalisis keuanganmu..."):
                try:
                    response = chat_with_advisor(
                        user_input=user_input,
                        chat_history=st.session_state.chat_history[:-1],
                        df=df,
                    )
                    st.markdown(response)
                except Exception as e:
                    response = f"Terjadi error: {str(e)}"
                    st.error(response)

    st.session_state.chat_history.append({"role": "assistant", "content": response})

    save_chat_history(
        st.session_state.chat_history
    )

# ─── Tombol Reset Chat ──────────────────────────────────────────────────────────
if st.button("🗑️ Hapus Riwayat Chat"):

    st.session_state.chat_history = []

    clear_chat_history()

    st.success(
        "Riwayat chat berhasil dihapus."
    )

    st.rerun()
