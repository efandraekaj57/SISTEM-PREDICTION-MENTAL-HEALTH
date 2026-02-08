import streamlit as st

# =============================================
# KONFIGURASI HALAMAN
# =============================================
st.set_page_config(
    page_title="Mental Health Self Assessment",
    layout="centered"
)

# =============================================
# HEADER
# =============================================
st.title("Mental Health Self-Assessment")
st.markdown(
    """
Aplikasi ini membantu skrining awal kondisi kesehatan mental
berdasarkan jawaban yang Anda berikan.

Aplikasi ini **bukan alat diagnosis medis**.
"""
)

# =============================================
# INPUT PENGGUNA
# =============================================
st.subheader("Pertanyaan")

q1 = st.selectbox(
    "1. Bagaimana perasaan Anda akhir-akhir ini?",
    [
        "Saya merasa baik-baik saja",
        "Saya merasa lelah",
        "Saya kehilangan semangat",
        "Saya merasa sangat sedih"
    ]
)

q2 = st.selectbox(
    "2. Apakah Anda sering merasa stres atau cemas?",
    [
        "Jarang",
        "Kadang-kadang",
        "Saya sering khawatir tanpa alasan",
        "Saya merasa cemas hampir setiap hari"
    ]
)

q3 = st.selectbox(
    "3. Bagaimana kualitas tidur Anda?",
    [
        "Tidur nyenyak",
        "Kadang sulit tidur",
        "Saya sering terbangun di malam hari",
        "Saya hampir tidak bisa tidur"
    ]
)

q4 = st.selectbox(
    "4. Bagaimana kondisi emosi Anda?",
    [
        "Stabil",
        "Mudah lelah",
        "Saya sering panik dan mudah emosi",
        "Emosi saya sering tidak terkendali"
    ]
)

q5 = st.selectbox(
    "5. Apakah Anda masih menikmati aktivitas sehari-hari?",
    [
        "Masih sangat menikmati",
        "Sedikit berkurang",
        "Saya kehilangan minat yang disukai",
        "Saya tidak tertarik pada apa pun"
    ]
)

q6 = st.selectbox(
    "6. Seberapa sering Anda merasa tidak berharga atau menyalahkan diri sendiri?",
    [
        "Tidak pernah",
        "Jarang",
        "Sering",
        "Hampir setiap hari"
    ]
)

q7 = st.selectbox(
    "7. Apakah Anda sulit berkonsentrasi saat bekerja atau belajar?",
    [
        "Tidak",
        "Kadang-kadang",
        "Sering",
        "Hampir selalu"
    ]
)

q8 = st.selectbox(
    "8. Apakah Anda merasa kelelahan secara fisik tanpa sebab yang jelas?",
    [
        "Tidak",
        "Kadang-kadang",
        "Sering",
        "Hampir setiap hari"
    ]
)

q9 = st.selectbox(
    "9. Apakah Anda menarik diri dari lingkungan sosial?",
    [
        "Tidak",
        "Sedikit",
        "Cukup sering",
        "Hampir selalu"
    ]
)

q10 = st.selectbox(
    "10. Apakah akhir-akhir ini Anda merasa kewalahan menghadapi hidup?",
    [
        "Tidak",
        "Kadang-kadang",
        "Sering",
        "Hampir setiap hari"
    ]
)

# =============================================
# FUNGSI SKOR
# =============================================
def score_question(answer, low, medium, high):
    if answer in high:
        return 2
    elif answer in medium:
        return 1
    else:
        return 0

def calculate_score():
    details = {}

    details["Perasaan"] = score_question(
        q1,
        ["Saya merasa baik-baik saja"],
        ["Saya merasa lelah"],
        ["Saya kehilangan semangat", "Saya merasa sangat sedih"]
    )

    details["Stres"] = score_question(
        q2,
        ["Jarang"],
        ["Kadang-kadang"],
        ["Saya sering khawatir tanpa alasan", "Saya merasa cemas hampir setiap hari"]
    )

    details["Tidur"] = score_question(
        q3,
        ["Tidur nyenyak"],
        ["Kadang sulit tidur"],
        ["Saya sering terbangun di malam hari", "Saya hampir tidak bisa tidur"]
    )

    details["Emosi"] = score_question(
        q4,
        ["Stabil"],
        ["Mudah lelah"],
        ["Saya sering panik dan mudah emosi", "Emosi saya sering tidak terkendali"]
    )

    details["Minat"] = score_question(
        q5,
        ["Masih sangat menikmati"],
        ["Sedikit berkurang"],
        ["Saya kehilangan minat yang disukai", "Saya tidak tertarik pada apa pun"]
    )

    details["Harga Diri"] = score_question(
        q6,
        ["Tidak pernah"],
        ["Jarang"],
        ["Sering", "Hampir setiap hari"]
    )

    details["Konsentrasi"] = score_question(
        q7,
        ["Tidak"],
        ["Kadang-kadang"],
        ["Sering", "Hampir selalu"]
    )

    details["Kelelahan"] = score_question(
        q8,
        ["Tidak"],
        ["Kadang-kadang"],
        ["Sering", "Hampir setiap hari"]
    )

    details["Sosial"] = score_question(
        q9,
        ["Tidak"],
        ["Sedikit"],
        ["Cukup sering", "Hampir selalu"]
    )

    details["Kewalahan"] = score_question(
        q10,
        ["Tidak"],
        ["Kadang-kadang"],
        ["Sering", "Hampir setiap hari"]
    )

    total_score = sum(details.values())
    return total_score, details

# =============================================
# HASIL
# =============================================
st.markdown("---")
st.subheader("Hasil Penilaian")

if st.button("Prediksi Sekarang"):
    score, details = calculate_score()

    st.markdown("Rincian Skor:")
    for k, v in details.items():
        st.write(f"- {k}: {v}")

    st.markdown(f"Total Skor: {score} / 20")

    if score >= 13:
        st.error("Risiko Tinggi Masalah Kesehatan Mental")

        st.markdown(
            """
Peringatan:
Hasil ini menunjukkan banyak indikator yang sering dikaitkan
dengan gangguan kecemasan atau depresi.

Saran Profesional:
- Sangat dianjurkan berkonsultasi dengan psikolog atau psikiater
- Jangan menghadapi kondisi ini sendirian
- Jika muncul pikiran menyakiti diri, segera cari bantuan profesional
"""
        )

    elif score >= 7:
        st.warning("Risiko Sedang Masalah Kesehatan Mental")

        st.markdown(
            """
Saran:
- Perhatikan pola tidur, stres, dan keseimbangan aktivitas
- Cobalah teknik relaksasi dan dukungan sosial
- Konsultasi profesional dianjurkan jika kondisi berlanjut
"""
        )

    else:
        st.success("Kondisi Relatif Stabil")

        st.markdown(
            """
Tetap Jaga Kesehatan Mental:
- Pertahankan kebiasaan sehat
- Jaga komunikasi dengan orang terdekat
- Lakukan evaluasi diri secara berkala
"""
        )

# =============================================
# FOOTER
# =============================================
st.markdown(
    """
Catatan:
Aplikasi ini hanya untuk skrining awal dan tidak menggantikan
diagnosis atau penanganan dari tenaga kesehatan profesional.
"""
)
