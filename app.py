import streamlit as st
import joblib
import pandas as pd
import os

MODEL_PATH = "saved_models/best_model_text_classification.pkl"
SCALER_PATH = "saved_models/text_scaler.pkl"
VECTORIZER_PATH = "saved_models/tfidf_vectorizer.pkl"
FEATURE_PATH = "saved_models/tfidf_feature_names.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
feature_names = joblib.load(FEATURE_PATH)

st.set_page_config(page_title="Mental Health Prediction", layout="centered")

st.title("Mental Health Prediction")

age = st.slider("Usia", 10, 80, 25)
sleep = st.slider("Jam tidur per hari", 0, 12, 7)
stress = st.selectbox("Tingkat stres", ["Jarang", "Kadang-kadang", "Sering", "Sangat sering"])
exercise = st.selectbox("Frekuensi olahraga", ["Tidak pernah", "1-2 kali", "3-5 kali", "Setiap hari"])
support = st.selectbox("Dukungan sosial", ["Tidak ada", "Sedikit", "Cukup", "Kuat"])
diet = st.selectbox("Pola makan", ["Tidak sehat", "Cukup sehat", "Sehat"])
screen = st.slider("Waktu layar per hari", 0, 16, 6)
work = st.selectbox("Tekanan kerja/studi", ["Tidak", "Kadang-kadang", "Sering", "Sangat sering"])

def form_to_text():
    return (
        f"Saya berusia {age} tahun, tidur {sleep} jam per hari, "
        f"tingkat stres {stress.lower()}, "
        f"olahraga {exercise.lower()}, "
        f"dukungan sosial {support.lower()}, "
        f"pola makan {diet.lower()}, "
        f"waktu layar {screen} jam per hari, "
        f"tekanan kerja {work.lower()}."
    )

if st.button("Prediksi"):
    text_input = form_to_text()

    X_tfidf = vectorizer.transform([text_input]).toarray()
    X_df = pd.DataFrame(X_tfidf, columns=vectorizer.get_feature_names_out())

    for col in feature_names:
        if col not in X_df.columns:
            X_df[col] = 0

    X_df = X_df[feature_names]
    X_scaled = scaler.transform(X_df.values)

    prediction = model.predict(X_scaled)[0]

    st.subheader("Hasil Prediksi")
    st.write(f"Kondisi mental terprediksi: {prediction}")
