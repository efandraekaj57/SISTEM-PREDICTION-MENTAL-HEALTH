import streamlit as st
import joblib
import pandas as pd
import os

# ======================================================
# PATH FILE
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "best_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "standard_scaler.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "feature_names.pkl")

# ======================================================
# VALIDASI FILE
# ======================================================
for path, name in [
    (MODEL_PATH, "best_model.pkl"),
    (SCALER_PATH, "standard_scaler.pkl"),
    (FEATURE_PATH, "feature_names.pkl")
]:
    if not os.path.exists(path):
        st.error(f"File {name} tidak ditemukan")
        st.stop()

# ======================================================
# LOAD MODEL
# ======================================================
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_names = joblib.load(FEATURE_PATH)

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
st.markdown("""
Selamat datang di aplikasi prediksi kesehatan mental.  
Silakan jawab beberapa pertanyaan berikut sesuai dengan kondisi Anda.
""")

st.markdown("---")

# ======================================================
# FORM PERTANYAAN (TAMPILAN MIRIP SEBELUM)
# ======================================================
st.subheader("Jawab Pertanyaan Berikut")

q1 = st.text_input(
    "Bagaimana perasaan Anda akhir-akhir ini?",
    placeholder="Contoh: Saya merasa sedih dan kehilangan semangat"
)

q2 = st.text_input(
    "Apakah Anda sering merasa stres atau cemas?",
    placeholder="Contoh: Saya sering khawatir tanpa alasan jelas"
)

q3 = st.text_input(
    "Bagaimana kondisi tidur Anda?",
    placeholder="Contoh: Saya sulit tidur dan sering terbangun malam hari"
)

q4 = st.text_input(
    "Bagaimana kondisi emosi Anda saat menghadapi masalah?",
    placeholder="Contoh: Saya mudah panik dan sulit mengendalikan emosi"
)

q5 = st.text_input(
    "Apakah Anda masih menikmati aktivitas sehari-hari?",
    placeholder="Contoh: Saya kehilangan minat pada hal yang dulu saya sukai"
)

# Gabungkan semua jawaban menjadi satu teks
user_text = " ".join([q1, q2, q3, q4, q5])

st.markdown("---")

# ======================================================
# PREDIKSI
# ======================================================
if st.button("Prediksi Sekarang"):
    if user_text.strip() == "":
        st.warning("Silakan isi minimal satu jawaban.")
    else:
        try:
            total_features = model.n_features_in_

            # Buat dataframe kosong sesuai jumlah fitur model
            X_input = pd.DataFrame(
                0,
                index=[0],
                columns=range(total_features)
            )

            # Isi fitur yang ADA di feature_names
            for idx, word in enumerate(feature_names):
                if word in user_text.lower():
                    X_input.iloc[0, idx] = 1

            # Scaling
            X_scaled = scaler.transform(X_input)

            # Prediksi
            prediction = model.predict(X_scaled)[0]

            st.subheader("Hasil Prediksi")
            st.success(f"Kondisi Kesehatan Mental: {prediction}")

        except Exception as e:
            st.error(f"Terjadi kesalahan saat prediksi: {e}")

# ======================================================
# FOOTER
# ======================================================
st.markdown("---")
st.caption("Model Machine Learning berbasis Text Classification (TF-IDF)")
