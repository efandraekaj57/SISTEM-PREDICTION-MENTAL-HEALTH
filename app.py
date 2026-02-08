# =============================================
# STREAMLIT APP — Mental Health Prediction
# =============================================
import streamlit as st
import pandas as pd
import joblib
import os

# =============================================
# LOAD MODEL, SCALER, FEATURE NAMES
# =============================================
MODEL_PATH = "best_model.pkl"
SCALER_PATH = "standard_scaler.pkl"
FEATURE_PATH = "feature_names.pkl"

if not (os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH) and os.path.exists(FEATURE_PATH)):
    st.error("File model, scaler, atau feature names tidak ditemukan.")
    st.stop()

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_names = joblib.load(FEATURE_PATH)

# =============================================
# KONFIGURASI HALAMAN
# =============================================
st.set_page_config(
    page_title="Mental Health Predictor",
    page_icon="🧠",
    layout="centered"
)

# =============================================
# HEADER
# =============================================
st.title("Mental Health Prediction App")
st.markdown(
    "Aplikasi ini digunakan untuk memprediksi risiko masalah kesehatan mental "
    "berdasarkan data yang dimasukkan pengguna."
)

# =============================================
# INPUT USER
# =============================================
st.subheader("Input Data")

age = st.slider("Usia", 10, 80, 25)
sleep_hours = st.slider("Jam tidur per hari", 0, 12, 7)

stress_level = st.selectbox(
    "Tingkat stres",
    ["Jarang", "Kadang-kadang", "Sering", "Sangat sering"]
)

exercise_freq = st.selectbox(
    "Frekuensi olahraga per minggu",
    ["Tidak pernah", "1-2 kali", "3-5 kali", "Setiap hari"]
)

social_support = st.selectbox(
    "Dukungan sosial",
    ["Tidak sama sekali", "Sedikit", "Cukup", "Sangat kuat"]
)

diet_quality = st.selectbox(
    "Kualitas pola makan",
    ["Tidak sehat", "Cukup sehat", "Sehat"]
)

screen_time = st.slider("Waktu layar per hari (jam)", 0, 16, 6)

work_pressure = st.selectbox(
    "Tekanan pekerjaan atau studi",
    ["Tidak", "Kadang-kadang", "Sering", "Sangat sering"]
)

# =============================================
# DATAFRAME USER
# =============================================
user_data = pd.DataFrame([{
    "age": age,
    "sleep_hours": sleep_hours,
    "stress_level": stress_level,
    "exercise_freq": exercise_freq,
    "social_support": social_support,
    "diet_quality": diet_quality,
    "screen_time": screen_time,
    "work_pressure": work_pressure
}])

# =============================================
# PREPROCESSING (SAMAKAN DENGAN TRAINING)
# =============================================
user_data = pd.get_dummies(user_data)

for col in feature_names:
    if col not in user_data.columns:
        user_data[col] = 0

user_data = user_data[feature_names]

# =============================================
# PREDIKSI
# =============================================
st.markdown("---")

if st.button("Prediksi"):
    try:
        scaled_data = scaler.transform(user_data)
        prediction = model.predict(scaled_data)[0]

        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(scaled_data)[0][1]
        else:
            probability = None

        st.subheader("Hasil Prediksi")

        if prediction == 1:
            st.error("Berisiko mengalami masalah kesehatan mental.")
        else:
            st.success("Tidak berisiko mengalami masalah kesehatan mental.")

        if probability is not None:
            st.write(f"Tingkat keyakinan model: {probability * 100:.2f}%")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat prediksi: {e}")

# =============================================
# FOOTER
# =============================================
st.markdown("---")
st.caption(
    f"Model: {model.__class__.__name__} | "
    "Scaler: StandardScaler | "
    "Preprocessing: One-Hot Encoding"
)
