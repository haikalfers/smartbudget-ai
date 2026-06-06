## Setup Awal

1. Clone repository

```bash
git clone <repo-url>
cd smartbudget-ai
```

2. Buat secrets.toml

```bash
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
```

3. Isi API Key Groq pada file secrets.toml

4. Install dependency

```bash
pip install -r requirements.txt
```

5. Jalankan aplikasi

```bash
streamlit run app.py
```