import os
import pickle
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression

from utils.data_utils import get_tren_bulanan

MODEL_PATH = "models/predictor.pkl"


def train_predictor(df):

    tren = get_tren_bulanan(df)

    if len(tren) < 2:
        return None

    X = np.arange(len(tren)).reshape(-1, 1)
    y = tren["saldo"].values

    model = LinearRegression()
    model.fit(X, y)

    return model


def save_predictor(model):

    os.makedirs("models", exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)


def load_predictor():

    if not os.path.exists(MODEL_PATH):
        return None

    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except:
        return None


def is_predictor_ready() -> bool:
    """Cek apakah model predictor sudah siap digunakan."""
    if not os.path.exists(MODEL_PATH):
        return False
    try:
        load_predictor()
        return True
    except Exception:
        return False


def calculate_volatility(series):

    if len(series) < 3:
        return 0.15

    pct_changes = pd.Series(series).pct_change()

    volatility = pct_changes.std()

    if pd.isna(volatility):
        return 0.15

    volatility = max(volatility, 0.05)
    volatility = min(volatility, 0.50)

    return volatility


def predict_future(
    df,
    horizon=3,
    target="Pengeluaran"
):

    tren = get_tren_bulanan(df)

    if len(tren) < 2:
        return pd.DataFrame()

    mapping = {
        "Pengeluaran": "pengeluaran",
        "Pemasukan": "pemasukan",
        "Saldo": "saldo"
    }

    col = mapping[target]

    y = tren[col].astype(float).values

    X = np.arange(len(y)).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)

    future_x = np.arange(
        len(y),
        len(y) + horizon
    ).reshape(-1, 1)

    normal = model.predict(future_x)

    volatility = calculate_volatility(y)

    if target == "Pengeluaran":

        pesimis = normal * (1 + volatility)
        optimis = normal * (1 - volatility)

    else:

        pesimis = normal * (1 - volatility)
        optimis = normal * (1 + volatility)

    last_month = pd.Period(
        tren["bulan"].iloc[-1],
        freq="M"
    )

    months = [
        str(last_month + i + 1)
        for i in range(horizon)
    ]

    result = pd.DataFrame({
        "bulan": months,
        "pesimis": pesimis.round(0),
        "normal": normal.round(0),
        "optimis": optimis.round(0)
    })

    result["volatility"] = round(
        volatility * 100,
        1
    )

    return result
