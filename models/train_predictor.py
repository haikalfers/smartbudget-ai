"""
models/train_predictor.py

Training predictor SmartBudget AI.
Jalankan:

python models/train_predictor.py
"""

import sys
import os

sys.path.append(os.path.abspath("."))

from utils.data_utils import load_transactions
from utils.predictor_utils import (
    train_predictor,
    save_predictor
)

print("Loading dataset...")

df = load_transactions()

if len(df) < 10:
    print("Data transaksi masih terlalu sedikit.")
    exit()

model = train_predictor(df)

if model is None:
    print("Minimal butuh data 2 bulan.")
    exit()

save_predictor(model)

print("Model berhasil disimpan ke:")
print("models/predictor.pkl")