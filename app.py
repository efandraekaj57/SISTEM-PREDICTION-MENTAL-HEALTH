# =============================================
# STREAMLIT APP — Mental Health Prediction
# =============================================
import streamlit as st
import pandas as pd
import joblib
import os

# =============================================
# LOAD PIPELINE & FEATURE NAMES
# =============================================
MODEL_PATH = "mental_health_pipeline.pkl"
FEATURE_PATH = "feature_names.pkl"

if not os.path.exists(MODEL_PATH) or not os.path.exists(FEATURE_PATH):
    st.error("❌ File model atau feature names tidak ditemukan.")
    st.stop()

pipeline = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURE_PATH)

# =============================================
# KONFIGURASI HALAMAN
# =============================================
st.set_page_config(
    page_title="Mental Health Predictor",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Mental Health Prediction App")
st.markdown(
    "Aplikasi ini memprediksi **risiko kesehatan mental** berdasarkan data yang Anda masukkan."
)

# =============================================
# INPUT USER
# =============================================
st.subheader(" Jawab Pertanyaan Berikut")

age = st.slider("Usia", 10, 80, 25)
sleep_hours = st.slider("Jam tidur per hari", 0, 12, 7)

stress_level = st.selectbox(
    "Tingkat stres",
    ["Jarang", "Kadang-kadang", "Sering", "Sangat sering"]
)

exercise_freq = st.selectbox(
    "Frekuensi olahraga",
    ["Tidak pernah", "1-2 kali", "3-5 kali", "Setiap hari"]
)

social_support = st.selectbox(
    "Dukungan sosial",
    ["Tidak sama sekali", "Sedikit", "Cukup", "Sangat kuat"]
)

diet_quality = st.selectbox(
    "Pola makan",
    ["Tidak sehat", "Cukup sehat", "Sehat"]
)

screen_time = st.slider("Screen time (jam/hari)", 0, 16, 6)

work_pressure = st.selectbox(
    "Tekanan kerja/studi",
    ["Tidak", "Kadang-kadang", "Sering", "Sangat sering"]
)

# =============================================
# DATAFRAME USER
# =============================================
user_df = pd.DataFrame([{
    "age": age,
    "sleep_hours": sleep_hours,
    "stress_level": stress_level,
    "exercise_freq": exercise_freq,
    "social_support": social_support,
    "diet_quality": diet_quality,
    "screen_time": screen_time,
    "work_pressure": work_pressure
}])

# Encoding HARUS SAMA DENGAN TRAINING
user_df = pd.get_dummies(user_df)

# Tambahkan kolom yang hilang
for col in feature_names:
    if col not in user_df.columns:
        user_df[col] = 0

# Urutkan kolom
user_df = user_df[feature_names]

# =============================================
# PREDIKSI
# =============================================
st.markdown("---")

if st.button(" Prediksi Sekarang"):
    prediction = pipeline.predict(user_df)[0]
    proba = pipeline.predict_proba(user_df)[0][1]

    st.subheader(" Hasil Prediksi")

    if prediction == 1:
        st.error("⚠️ **Berisiko Mengalami Masalah Kesehatan Mental**")
    else:
        st.success(" **Tidak Berisiko / Sehat**")

    st.write(f"**Keyakinan Model:** {proba*100:.2f}%")

# =============================================
# FOOTER
# =============================================
st.markdown("---")
st.caption("Model Machine Learning dengan Pipeline (Scaler + Model)")
