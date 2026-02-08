import streamlit as st
import joblib
import pandas as pd
import os

# ======================================================
# PATH FILE
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "best_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "feature_names.pkl")

# ======================================================
# VALIDASI FILE
# ======================================================
for path, name in [
    (MODEL_PATH, "best_model.pkl"),
    (FEATURE_PATH, "feature_names.pkl")
]:
    if not os.path.exists(path):
        st.error(f"File {name} tidak ditemukan")
        st.stop()

# ======================================================
# LOAD MODEL
# ======================================================
model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURE_PATH)

TOTAL_FEATURES = model.n_features_in_

# ======================================================
# UI
# ======================================================
st.set_page_config(page_title="Mental Health Prediction", layout="centered")

st.title("Mental Health Prediction App")
st.write("Jawab pertanyaan berikut sesuai kondisi mental Anda")

st.markdown("---")

# ======================================================
# FORM INPUT (TAMPILAN MIRIP SEBELUM)
# ======================================================
st.subheader("Jawab Pertanyaan Berikut")

q1 = st.text_input("Bagaimana perasaan Anda akhir-akhir ini?")
q2 = st.text_input("Apakah Anda sering merasa stres atau cemas?")
q3 = st.text_input("Bagaimana kualitas tidur Anda?")
q4 = st.text_input("Bagaimana kondisi emosi Anda?")
q5 = st.text_input("Apakah Anda masih menikmati aktivitas sehari-hari?")

user_text = " ".join([q1, q2, q3, q4, q5]).lower()

st.markdown("---")

# ======================================================
# PREDIKSI
# ======================================================
if st.button("Prediksi Sekarang"):
    if user_text.strip() == "":
        st.warning("Silakan isi minimal satu jawaban")
    else:
        try:
            # Buat input sesuai jumlah fitur model
            X_input = pd.DataFrame(
                0,
                index=[0],
                columns=range(TOTAL_FEATURES)
            )

            # Isi fitur yang dikenal
            for idx, word in enumerate(feature_names):
                if word in user_text:
                    X_input.iloc[0, idx] = 1

            # PREDIKSI TANPA SCALER
            prediction = model.predict(X_input)[0]

            st.subheader("Hasil Prediksi")
            st.success(f"Kondisi Kesehatan Mental: {prediction}")

        except Exception as e:
            st.error(f"Terjadi kesalahan saat prediksi: {e}")

# ======================================================
# FOOTER
# ======================================================
st.markdown("---")
st.caption("RandomForest Text Classification Model")
