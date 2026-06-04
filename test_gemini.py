import joblib

model = joblib.load("models/classifier.pkl")
kategori = model.predict(["beli nasi goreng"])[0]
# Output: "Makan"