import streamlit as st
import joblib
import pandas as pd
import os

# ======================================================
# PATH AMAN (STREAMLIT CLOUD)
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "best_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "standard_scaler.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "feature_names.pkl")

# ======================================================
# VALIDASI FILE
# ======================================================
if not os.path.exists(MODEL_PATH):
    st.error("File best_model.pkl tidak ditemukan")
    st.stop()

if not os.path.exists(SCALER_PATH):
    st.error("File standard_scaler.pkl tidak ditemukan")
    st.stop()

if not os.path.exists(FEATURE_PATH):
    st.error("File feature_names.pkl tidak ditemukan")
    st.stop()

# ======================================================
# LOAD MODEL
# ======================================================
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_names = joblib.load(FEATURE_PATH)

# ======================================================
# UI
# ======================================================
st.set_page_config(page_title="Mental Health Prediction", layout="centered")

st.title("Mental Health Prediction App")
st.write("Prediksi kondisi kesehatan mental berdasarkan data pengguna")

st.subheader("Input Data")

# ======================================================
# INPUT SESUAI DATA NUMERIK
# ======================================================
age = st.slider("Usia", 10, 80, 25)
sleep_hours = st.slider("Jam tidur per hari", 0, 12, 7)
stress_level = st.slider("Tingkat stres (0–10)", 0, 10, 5)
anxiety_level = st.slider("Tingkat kecemasan (0–10)", 0, 10, 5)
depression_level = st.slider("Tingkat depresi (0–10)", 0, 10, 5)
social_support = st.slider("Dukungan sosial (0–10)", 0, 10, 5)
physical_activity = st.slider("Aktivitas fisik (jam/minggu)", 0, 20, 3)
screen_time = st.slider("Waktu layar per hari (jam)", 0, 16, 6)

# ======================================================
# PREDIKSI
# ======================================================
if st.button("Prediksi"):
    try:
        # Buat dataframe SESUAI feature_names saat training
        input_data = pd.DataFrame([{
            feature_names[0]: age,
            feature_names[1]: sleep_hours,
            feature_names[2]: stress_level,
            feature_names[3]: anxiety_level,
            feature_names[4]: depression_level,
            feature_names[5]: social_support,
            feature_names[6]: physical_activity,
            feature_names[7]: screen_time
        }])

        # Pastikan urutan kolom sama
        input_data = input_data[feature_names]

        # Scaling
        input_scaled = scaler.transform(input_data)

        # Prediksi
        prediction = model.predict(input_scaled)[0]

        st.subheader("Hasil Prediksi")
        st.success(f"Kondisi kesehatan mental: {prediction}")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat prediksi: {e}")

# ======================================================
# FOOTER
# ======================================================
st.markdown("---")
st.caption("Model Machine Learning dengan StandardScaler")
