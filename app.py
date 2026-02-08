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
if not os.path.exists(MODEL_PATH):
    st.error("File best_model.pkl tidak ditemukan")
    st.stop()

if not os.path.exists(FEATURE_PATH):
    st.error("File feature_names.pkl tidak ditemukan")
    st.stop()

# ======================================================
# LOAD MODEL
# ======================================================
model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURE_PATH)
TOTAL_FEATURES = model.n_features_in_

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="Mental Health Prediction",
    layout="centered"
)

# ======================================================
# HEADER
# ======================================================
st.title("Mental Health Prediction App")
st.write(
    "Silakan jawab beberapa pertanyaan berikut untuk mengetahui "
    "perkiraan kondisi kesehatan mental Anda."
)

st.markdown("---")

# ======================================================
# FORM INPUT
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
        st.warning("Silakan isi minimal satu jawaban.")
    else:
        try:
            X_input = pd.DataFrame(
                0,
                index=[0],
                columns=range(TOTAL_FEATURES)
            )

            for idx, word in enumerate(feature_names):
                if word in user_text:
                    X_input.iloc[0, idx] = 1

            prediction = model.predict(X_input)[0]

            st.subheader("Hasil Prediksi")

            if prediction == 0:
                st.success(
                    "Kondisi Kesehatan Mental: "
                    "Tidak Berisiko / Relatif Stabil"
                )
            else:
                st.error(
                    "Kondisi Kesehatan Mental: "
                    "Berisiko Mengalami Masalah"
                )

        except Exception as e:
            st.error(f"Terjadi kesalahan saat prediksi: {e}")

# ======================================================
# FOOTER
# ======================================================
st.markdown("---")
st.caption("Model Machine Learning berbasis Text Classification")
