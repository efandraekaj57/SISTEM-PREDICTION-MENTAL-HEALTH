import streamlit as st
import joblib
import pandas as pd
import os

MODEL_PATH = "saved_models/best_model_text_classification.pkl"
SCALER_PATH = "saved_models/text_scaler.pkl"
VECTORIZER_PATH = "saved_models/tfidf_vectorizer.pkl"
FEATURE_PATH = "saved_models/tfidf_feature_names.pkl"

if not all(os.path.exists(p) for p in [
    MODEL_PATH, SCALER_PATH, VECTORIZER_PATH, FEATURE_PATH
]):
    st.error("File model atau komponen preprocessing tidak ditemukan.")
    st.stop()

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
feature_names = joblib.load(FEATURE_PATH)

st.set_page_config(
    page_title="Mental Health Text Classification",
    layout="centered"
)

st.title("Mental Health Text Classification")
st.write("Masukkan teks pernyataan untuk memprediksi kondisi kesehatan mental.")

text_input = st.text_area(
    "Masukkan pernyataan Anda:",
    height=150
)

if st.button("Prediksi"):
    if text_input.strip() == "":
        st.warning("Teks tidak boleh kosong.")
    else:
        X_tfidf = vectorizer.transform([text_input]).toarray()
        X_df = pd.DataFrame(
            X_tfidf,
            columns=vectorizer.get_feature_names_out()
        )

        for col in feature_names:
            if col not in X_df.columns:
                X_df[col] = 0

        X_df = X_df[feature_names]

        X_scaled = scaler.transform(X_df.values)
        prediction = model.predict(X_scaled)[0]

        st.subheader("Hasil Prediksi")
        st.write(f"Klasifikasi: {prediction}")
