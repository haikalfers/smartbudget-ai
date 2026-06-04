# utils/llm_utils.py

from groq import Groq
import streamlit as st

def get_llm_response(prompt: str, system_prompt: str = "") -> str:
    """
    Fungsi utama untuk memanggil LLM.
    Urutan: Groq (utama) → fallback pesan error informatif
    """
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            max_tokens=1024,
            temperature=0.7
        )
        return response.choices[0].message.content
    
    except Exception as e:
        error_msg = str(e)
        if "rate_limit" in error_msg.lower():
            return "⚠️ AI sedang sibuk, coba lagi dalam 1 menit."
        elif "quota" in error_msg.lower():
            return "⚠️ Batas harian tercapai, coba lagi besok."
        else:
            return f"⚠️ AI tidak tersedia saat ini: {error_msg}"