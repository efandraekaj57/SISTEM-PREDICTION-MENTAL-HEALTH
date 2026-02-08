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
# UI
# ======================================================
st.set_page_config(page_title="Mental Health Text Prediction", layout="centered")

st.title("Mental Health Prediction (Text-Based)")
st.write("Masukkan teks yang menggambarkan perasaan atau kondisi mental")

# ======================================================
# INPUT TEKS
# ======================================================
user_text = st.text_area(
    "Tulis perasaan Anda di sini",
    placeholder="Contoh: Saya merasa sedih dan kehilangan semangat hidup"
)

# ======================================================
# PREDIKSI
# ======================================================
if st.button("Prediksi"):
    if user_text.strip() == "":
        st.warning("Teks tidak boleh kosong")
    else:
        try:
            # =============================================
            # TF-IDF MANUAL SESUAI FEATURE TRAINING
            # =============================================
            text_series = pd.Series([user_text])

            tfidf_df = pd.DataFrame(0, index=[0], columns=feature_names)

            for word in user_text.lower().split():
                if word in tfidf_df.columns:
                    tfidf_df.at[0, word] += 1

            # =============================================
            # SCALING
            # =============================================
            X_scaled = scaler.transform(tfidf_df)

            # =============================================
            # PREDIKSI
            # =============================================
            prediction = model.predict(X_scaled)[0]

            st.subheader("Hasil Prediksi")
            st.success(f"Kondisi Mental: {prediction}")

        except Exception as e:
            st.error(f"Terjadi kesalahan saat prediksi: {e}")

# ======================================================
# FOOTER
# ======================================================
st.markdown("---")
st.caption("Text Classification Model dengan TF-IDF dan StandardScaler")
