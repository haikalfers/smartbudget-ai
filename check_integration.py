"""
check_integration.py — Checklist pre-deploy SmartBudget AI
Jalankan: python check_integration.py
Akan mengecek semua komponen sebelum deploy ke Streamlit Cloud.
"""

import os
import sys
import importlib

RESET  = "\033[0m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"

def ok(msg):    print(f"  {GREEN}✅ {msg}{RESET}")
def warn(msg):  print(f"  {YELLOW}⚠️  {msg}{RESET}")
def fail(msg):  print(f"  {RED}❌ {msg}{RESET}")
def header(msg):print(f"\n{BOLD}{msg}{RESET}")

errors = 0
warnings = 0

# ─── 1. Struktur Folder & File Wajib ─────────────────────────────────────────
header("1. Struktur Folder & File Wajib")
FILES_WAJIB = [
    "app.py",
    "requirements.txt",
    ".gitignore",
    ".streamlit/config.toml",
    "utils/__init__.py",
    "utils/data_utils.py",
    "utils/classifier_utils.py",
    "utils/predictor_utils.py",
    "utils/groq_tools.py",
    "pages/1_Insights_Keuangan.py",
    "pages/2_Input_Transaksi.py",
    "pages/3_Prediksi.py",
    "pages/4_AI_Advisor.py",
    "data/generate_dataset.py",
    "models/train_classifier.py",
    "models/train_predictor.py",
]
FILES_OPSIONAL = [
    "data/sample_data.csv",
    "models/classifier.pkl",
    "models/predictor.pkl",
]

for f in FILES_WAJIB:
    if os.path.exists(f):
        ok(f)
    else:
        fail(f"TIDAK ADA: {f}")
        errors += 1

for f in FILES_OPSIONAL:
    if os.path.exists(f):
        ok(f"(opsional) {f}")
    else:
        warn(f"(opsional) TIDAK ADA: {f} — perlu di-generate dulu")
        warnings += 1

# ─── 2. Syntax Check Python Files ────────────────────────────────────────────
header("2. Syntax Check Python Files")
import ast, glob

py_files = glob.glob("**/*.py", recursive=True)
py_files = [f for f in py_files if "venv" not in f and "__pycache__" not in f]

for f in py_files:
    try:
        with open(f, "r", encoding="utf-8") as fh:
            ast.parse(fh.read())
        ok(f)
    except SyntaxError as e:
        fail(f"SYNTAX ERROR di {f}: {e}")
        errors += 1

# ─── 3. Requirements.txt ─────────────────────────────────────────────────────
header("3. requirements.txt")
PACKAGES_WAJIB = [
    "streamlit", "pandas", "numpy", "scikit-learn",
    "plotly", "groq", "joblib", "python-dateutil"
]
if os.path.exists("requirements.txt"):
    with open("requirements.txt") as f:
        req_content = f.read().lower()
    for pkg in PACKAGES_WAJIB:
        if pkg.lower() in req_content:
            ok(pkg)
        else:
            fail(f"TIDAK ADA di requirements.txt: {pkg}")
            errors += 1
else:
    fail("requirements.txt tidak ditemukan!")
    errors += 1

# ─── 4. Import Check ─────────────────────────────────────────────────────────
header("4. Import Check Utils")
sys.path.insert(0, ".")
MODULES = [
    ("utils.data_utils",       ["init_session_state", "tambah_transaksi", "format_rupiah",
                                 "KATEGORI_PENGELUARAN", "KATEGORI_PEMASUKAN"]),
    ("utils.classifier_utils", ["klasifikasi_teks", "is_classifier_ready"]),
    ("utils.predictor_utils",  ["load_predictor", "is_predictor_ready", "predict_future"]),
    ("utils.groq_tools",       ["analyze_spending", "get_budget_recommendation",
                                 "jalankan_tool", "TOOLS_DEFINITION"]),
]

for mod_name, attrs in MODULES:
    try:
        mod = importlib.import_module(mod_name)
        missing = [a for a in attrs if not hasattr(mod, a)]
        if missing:
            fail(f"{mod_name} — fungsi/atribut tidak ada: {missing}")
            errors += 1
        else:
            ok(f"{mod_name} — semua {len(attrs)} fungsi/atribut tersedia")
    except ImportError as e:
        fail(f"Tidak bisa import {mod_name}: {e}")
        errors += 1

# ─── 5. Kategori Konsistensi ─────────────────────────────────────────────────
header("5. Konsistensi Nama Kategori")
try:
    from utils.data_utils import KATEGORI_PENGELUARAN, KATEGORI_PEMASUKAN
    EXPECTED_KELUAR = {"Makanan & Minuman", "Transportasi", "Pendidikan", "Hiburan",
                       "Kesehatan", "Belanja", "Tagihan & Utilitas", "Lainnya"}
    EXPECTED_MASUK  = {"Uang Saku", "Beasiswa", "Freelance / Part-time", "Hadiah", "Lainnya"}

    if set(KATEGORI_PENGELUARAN) == EXPECTED_KELUAR:
        ok("KATEGORI_PENGELUARAN sesuai spesifikasi")
    else:
        diff = EXPECTED_KELUAR.symmetric_difference(set(KATEGORI_PENGELUARAN))
        fail(f"KATEGORI_PENGELUARAN tidak sesuai. Beda: {diff}")
        errors += 1

    if set(KATEGORI_PEMASUKAN) == EXPECTED_MASUK:
        ok("KATEGORI_PEMASUKAN sesuai spesifikasi")
    else:
        diff = EXPECTED_MASUK.symmetric_difference(set(KATEGORI_PEMASUKAN))
        fail(f"KATEGORI_PEMASUKAN tidak sesuai. Beda: {diff}")
        errors += 1
except Exception as e:
    fail(f"Tidak bisa cek kategori: {e}")
    errors += 1

# ─── 6. .gitignore Check ─────────────────────────────────────────────────────
header("6. .gitignore")
GITIGNORE_WAJIB = [
    ".streamlit/secrets.toml",
    "models/*.pkl",
    "data/dataset_transaksi.csv",
    "data/sample_data.csv",
    "__pycache__/",
    "*.pyc",
    "venv/",
    ".env",
]
if os.path.exists(".gitignore"):
    with open(".gitignore") as f:
        gi = f.read()
    for entry in GITIGNORE_WAJIB:
        if entry in gi:
            ok(entry)
        else:
            fail(f"TIDAK ADA di .gitignore: {entry}")
            errors += 1
else:
    fail(".gitignore tidak ditemukan!")
    errors += 1

# ─── 7. secrets.toml ─────────────────────────────────────────────────────────
header("7. Konfigurasi Secrets")
if os.path.exists(".streamlit/secrets.toml"):
    with open(".streamlit/secrets.toml") as f:
        s = f.read()
    if "GROQ_API_KEY" in s and "isi-api-key" not in s:
        ok("secrets.toml ada dan GROQ_API_KEY diisi")
    elif "GROQ_API_KEY" in s:
        warn("secrets.toml ada tapi GROQ_API_KEY masih placeholder — isi dengan key asli!")
        warnings += 1
    else:
        fail("secrets.toml ada tapi GROQ_API_KEY tidak ditemukan")
        errors += 1
else:
    warn("secrets.toml TIDAK ADA — wajib dibuat sebelum deploy!")
    warn("Isi dengan: GROQ_API_KEY = 'gsk_xxxxxxxxxxxxx'")
    warnings += 1

# ─── 8. Model Files ───────────────────────────────────────────────────────────
header("8. Model Files (perlu di-generate sebelum deploy)")
MODEL_FILES = ["models/classifier.pkl", "models/predictor.pkl"]
for mf in MODEL_FILES:
    if os.path.exists(mf):
        size_kb = os.path.getsize(mf) / 1024
        ok(f"{mf} ({size_kb:.1f} KB)")
    else:
        warn(f"{mf} belum ada — jalankan train script terlebih dahulu")
        warnings += 1

# ─── Ringkasan ────────────────────────────────────────────────────────────────
header("=" * 50)
print(f"\n{BOLD}HASIL CHECKLIST:{RESET}")
if errors == 0 and warnings == 0:
    print(f"  {GREEN}{BOLD}🎉 SEMUA LULUS! Project siap untuk deploy.{RESET}")
elif errors == 0:
    print(f"  {YELLOW}{BOLD}⚠️  {warnings} warning ditemukan. Cek sebelum deploy.{RESET}")
else:
    print(f"  {RED}{BOLD}❌ {errors} error + {warnings} warning. Wajib diperbaiki sebelum deploy!{RESET}")

print(f"\n  Error   : {RED}{errors}{RESET}")
print(f"  Warning : {YELLOW}{warnings}{RESET}")
print()

sys.exit(1 if errors > 0 else 0)
