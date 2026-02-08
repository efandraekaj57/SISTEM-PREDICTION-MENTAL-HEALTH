import streamlit as st

# =============================================
# KONFIGURASI HALAMAN
# =============================================
st.set_page_config(
    page_title="Mental Health Self Check",
    page_icon="🧠",
    layout="centered"
)

# =============================================
# HEADER
# =============================================
st.title("Mental Health Self-Assessment")
st.markdown(
    """
Aplikasi ini membantu **skrining awal** kondisi kesehatan mental  
berdasarkan jawaban yang Anda berikan.

**Bukan diagnosis medis**
"""
)

# =============================================
# INPUT PENGGUNA
# =============================================
st.subheader("Pertanyaan")

feeling = st.selectbox(
    "Bagaimana perasaan Anda akhir-akhir ini?",
    [
        "Saya merasa baik-baik saja",
        "Saya merasa lelah",
        "Saya kehilangan semangat",
        "Saya merasa sangat sedih"
    ]
)

stress = st.selectbox(
    "Apakah Anda sering merasa stres atau cemas?",
    [
        "Jarang",
        "Kadang-kadang",
        "Saya sering khawatir tanpa alasan",
        "Saya merasa cemas hampir setiap hari"
    ]
)

sleep = st.selectbox(
    "Bagaimana kualitas tidur Anda?",
    [
        "Tidur nyenyak",
        "Kadang sulit tidur",
        "Saya sering terbangun di malam hari",
        "Saya hampir tidak bisa tidur"
    ]
)

emotion = st.selectbox(
    "Bagaimana kondisi emosi Anda?",
    [
        "Stabil",
        "Mudah lelah",
        "Saya sering panik dan mudah emosi",
        "Emosi saya sering tidak terkendali"
    ]
)

interest = st.selectbox(
    "Apakah Anda masih menikmati aktivitas sehari-hari?",
    [
        "Masih sangat menikmati",
        "Sedikit berkurang",
        "Saya kehilangan minat yang disukai",
        "Saya tidak tertarik pada apa pun"
    ]
)

# =============================================
# FUNGSI HITUNG SKOR
# =============================================
def calculate_score():
    score = 0
    detail = {}

    # Perasaan
    if feeling in ["Saya kehilangan semangat", "Saya merasa sangat sedih"]:
        score += 2
        detail["Perasaan"] = 2
    else:
        detail["Perasaan"] = 0

    # Stres
    if stress in ["Saya sering khawatir tanpa alasan", "Saya merasa cemas hampir setiap hari"]:
        score += 2
        detail["Stres / Kecemasan"] = 2
    else:
        detail["Stres / Kecemasan"] = 0

    # Tidur
    if sleep in ["Saya sering terbangun di malam hari", "Saya hampir tidak bisa tidur"]:
        score += 1
        detail["Kualitas Tidur"] = 1
    else:
        detail["Kualitas Tidur"] = 0

    # Emosi
    if emotion in ["Saya sering panik dan mudah emosi", "Emosi saya sering tidak terkendali"]:
        score += 2
        detail["Stabilitas Emosi"] = 2
    else:
        detail["Stabilitas Emosi"] = 0

    # Minat
    if interest in ["Saya kehilangan minat yang disukai", "Saya tidak tertarik pada apa pun"]:
        score += 2
        detail["Minat Aktivitas"] = 2
    else:
        detail["Minat Aktivitas"] = 0

    return score, detail

# =============================================
# PREDIKSI
# =============================================
st.markdown("---")
st.subheader("Hasil Penilaian")

if st.button("Prediksi Sekarang"):
    score, detail = calculate_score()

    # Tampilkan skor detail
    st.markdown("###  Rincian Skor")
    for k, v in detail.items():
        st.write(f"- **{k}**: {v}")

    st.markdown(f"### Total Skor: **{score} / 9**")

    # Keputusan
    if score >= 6:
        st.error("**Berisiko Tinggi terhadap masalah kesehatan mental**")

        st.markdown(
            """
### Peringatan
Hasil ini menunjukkan adanya **indikator kuat** yang sering
dikaitkan dengan gangguan kecemasan atau depresi.

### 💬 Saran Profesional
- Pertimbangkan **berbicara dengan psikolog atau psikiater**
- Ceritakan kondisi Anda kepada **orang yang dipercaya**
- Jika merasa sangat tertekan atau memiliki pikiran menyakiti diri:
  **SEGERA cari bantuan profesional atau layanan darurat**
"""
        )

    elif score >= 4:
        st.warning("**Berisiko Sedang**")

        st.markdown(
            """
### Saran
- Perhatikan pola tidur & manajemen stres
- Coba teknik relaksasi (napas dalam, olahraga ringan)
- Jika kondisi berlangsung >2 minggu, **konsultasi profesional dianjurkan**
"""
        )

    else:
        st.success("**Relatif Stabil**")

        st.markdown(
            """
###  Tetap Jaga Kesehatan Mental
- Pertahankan pola hidup sehat
- Luangkan waktu untuk diri sendiri
- Jangan ragu mencari bantuan bila kondisi berubah
"""
        )

# =============================================
# FOOTER
# =============================================
st.markdown(
    """
---
**Catatan Penting:**  
Aplikasi ini hanya untuk **skrining awal**, bukan diagnosis medis.  
Untuk hasil yang akurat, konsultasikan dengan tenaga profesional.
"""
)
