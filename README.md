<div align="center">

# 💸 SmartBudget AI

**Aplikasi manajemen keuangan mahasiswa berbasis Machine Learning & Agentic AI**
<br>
*AI-powered personal finance management app for students*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://smartbudget-ai-dsga.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-F7931E?logo=scikit-learn&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-412991)
![License](https://img.shields.io/badge/License-MIT-green)

[🚀 Live Demo](https://smartbudget-ai-dsga.streamlit.app/) · [📁 Repository](https://github.com/haikalfers/smartbudget-ai) · [📋 Laporan](#)

</div>

---

## 📌 Daftar Isi / Table of Contents

- [Tentang Proyek / About](#-tentang-proyek--about)
- [Fitur Utama / Key Features](#-fitur-utama--key-features)
- [Tech Stack](#-tech-stack)
- [Struktur Proyek / Project Structure](#-struktur-proyek--project-structure)
- [Instalasi / Installation](#-instalasi--installation)
- [Cara Penggunaan / Usage](#-cara-penggunaan--usage)
- [Tim / Team](#-tim--team)
- [Program](#-program)

---

## 🧠 Tentang Proyek / About

**🇮🇩 Indonesia**

SmartBudget AI adalah aplikasi web manajemen keuangan yang dirancang khusus untuk mahasiswa. Aplikasi ini menggabungkan *machine learning* untuk klasifikasi dan prediksi keuangan, serta *agentic AI* berbasis Groq untuk memberikan rekomendasi finansial secara real-time berdasarkan data transaksi pengguna.

Proyek ini dikembangkan sebagai tugas akhir program **Studi Independen Data Science & Generative AI** di PT Celerates, dengan deadline 15 Juni 2026.

**🇬🇧 English**

SmartBudget AI is a web-based personal finance management application designed specifically for students. It combines machine learning for expense classification and financial prediction, with Groq-powered agentic AI to deliver real-time financial recommendations based on the user's transaction data.

This project was developed as a final project for the **Independent Study Program in Data Science & Generative AI** at PT Celerates.

---

## ✨ Fitur Utama / Key Features

| Fitur / Feature | Deskripsi 🇮🇩 | Description 🇬🇧 |
|---|---|---|
| 📊 **Dashboard** | Ringkasan keuangan real-time dengan chart interaktif | Real-time financial summary with interactive charts |
| ✏️ **Input Transaksi** | Catat pemasukan & pengeluaran dengan auto-klasifikasi AI | Log income & expenses with AI auto-classification |
| 📈 **Analisis** | Distribusi pengeluaran per kategori & tren bulanan | Spending distribution by category & monthly trends |
| 🔮 **Prediksi** | Prediksi pengeluaran bulan depan berbasis ML | Next-month spending prediction using ML |
| 💬 **AI Advisor** | Chatbot finansial berbasis Groq (LLaMA 3.1) dengan agentic tools | Groq-powered financial chatbot (LLaMA 3.1) with agentic tools |

### 🤖 Kemampuan AI / AI Capabilities

- **Auto-klasifikasi** — Model TF-IDF + Logistic Regression mengklasifikasikan kategori transaksi otomatis dari deskripsi teks
- **Prediksi keuangan** — Linear Regression + Polynomial Features untuk memproyeksikan pengeluaran bulan depan
- **Agentic AI Advisor** — LLaMA 3.1 via Groq API dengan *function calling* (`analyze_spending`, `get_budget_recommendation`) yang menganalisis data keuangan user secara real-time

---

## 🛠 Tech Stack

### Machine Learning
| Library | Kegunaan / Purpose |
|---|---|
| `scikit-learn` | TF-IDF Vectorizer, Logistic Regression, Linear Regression, PolynomialFeatures |
| `joblib` | Serialisasi model `.pkl` / Model serialization |
| `pandas` & `numpy` | Manipulasi & preprocessing data / Data manipulation & preprocessing |

### AI & LLM
| Library | Kegunaan / Purpose |
|---|---|
| `groq` | Groq API client — LLaMA 3.1 8B Instant |
| Function Calling | Agentic tools: `analyze_spending`, `get_budget_recommendation` |

### Frontend & Visualisasi
| Library | Kegunaan / Purpose |
|---|---|
| `streamlit` | Framework UI web app |
| `plotly` | Chart interaktif (pie, bar, line) / Interactive charts |

### Data & Deployment
| Komponen | Detail |
|---|---|
| Penyimpanan | CSV + `st.session_state` |
| Deploy | Streamlit Cloud |
| Secrets | `GROQ_API_KEY` via Streamlit Cloud Secrets |

---

## 📁 Struktur Proyek / Project Structure

```
smartbudget-ai/
├── pages/
│   ├── 1_Dashboard.py          # Ringkasan keuangan / Financial summary
│   ├── 2_Input_Transaksi.py    # Input transaksi + auto-klasifikasi AI
│   ├── 3_Analisis.py           # Analisis & visualisasi / Analysis & charts
│   ├── 4_Prediksi.py           # Prediksi ML / ML prediction
│   └── 5_AI_Advisor.py         # Chatbot Groq + agentic tools
├── models/
│   ├── classifier.pkl          # Trained TF-IDF + Logistic Regression
│   ├── predictor.pkl           # Trained Linear Regression
│   ├── train_classifier.py     # Script training klasifikasi
│   └── train_predictor.py      # Script training prediksi
├── data/
│   └── generate_dataset.py     # Generator dataset sintetis
├── utils/
│   ├── data_utils.py           # CRUD transaksi & helper functions
│   ├── classifier_utils.py     # Wrapper model klasifikasi
│   ├── predictor_utils.py      # Wrapper model prediksi
│   ├── groq_tools.py           # Agentic AI tools & Groq API
│   └── sidebar_style.py        # CSS global sidebar (terpusat)
├── .streamlit/
│   ├── config.toml             # Tema & konfigurasi Streamlit
│   └── secrets.toml            # ⚠️ TIDAK di-commit — isi manual
├── app.py                      # Entry point + health check + auto-train
├── requirements.txt
├── check_integration.py        # Pre-deploy integration checker
└── README.md
```

---

## 🚀 Instalasi / Installation

### Prasyarat / Prerequisites

- Python 3.10+
- Groq API Key — daftar gratis di [console.groq.com](https://console.groq.com)

### Langkah / Steps

**1. Clone repository**
```bash
git clone https://github.com/haikalfers/smartbudget-ai.git
cd smartbudget-ai
```

**2. Buat virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Konfigurasi Groq API Key**

Buat file `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxx"
```

**5. Generate dataset & train model**
```bash
python data/generate_dataset.py
python models/train_classifier.py
python models/train_predictor.py
```

**6. Jalankan aplikasi**
```bash
streamlit run app.py
```

Buka browser di `http://localhost:8501` 🎉

---

## 📖 Cara Penggunaan / Usage

**🇮🇩**

1. **Mulai** — Klik "Load Sample Data" di halaman utama untuk melihat demo dengan data contoh, atau langsung input transaksimu sendiri.
2. **Input Transaksi** — Isi tanggal, deskripsi, jumlah, dan tipe. AI akan otomatis menyarankan kategori berdasarkan deskripsi.
3. **Dashboard** — Pantau saldo, total pemasukan & pengeluaran, serta chart distribusi kategori.
4. **Analisis** — Lihat breakdown pengeluaran per kategori dan tren bulanan.
5. **Prediksi** — Lihat proyeksi pengeluaran bulan depan berdasarkan pola historis.
6. **AI Advisor** — Chat langsung dengan AI untuk mendapat analisis dan rekomendasi finansial personal.

**🇬🇧**

1. **Start** — Click "Load Sample Data" on the home page to explore with sample data, or start logging your own transactions.
2. **Input Transaction** — Fill in the date, description, amount, and type. AI will automatically suggest a category based on the description.
3. **Dashboard** — Monitor your balance, total income & expenses, and category distribution charts.
4. **Analysis** — View spending breakdown by category and monthly trends.
5. **Prediction** — See next-month spending projections based on historical patterns.
6. **AI Advisor** — Chat directly with AI for personalized financial analysis and recommendations.

---

## 👥 Kelompok 5 / Shavira Nurulita

Program **Studi Independen Data Science & Generative AI** — PT Celerates

| No | Nama Lengkap |
|----|-------------|
| 1 | Haikal Ferdian Saputra |
| 2 | Muhammad Rafi Dwi Saputra |
| 3 | Galih Pikatra |
| 4 | Muhammad Zaky Taj Aldien |

---

## 🏫 Program

<div align="center">

**Studi Independen Data Science & Generative AI**
<br>
PT Celerates · 2026

</div>

---

<div align="center">

Dibuat dengan Kelompok 5 - Shavira Nurulita

</div>
