import streamlit as st
from textblob import TextBlob

# Judul aplikasi
st.title("Aplikasi Analisis Sentimen Sederhana")

# Deskripsi
st.write("""
Aplikasi ini menganalisis sentimen teks yang Anda masukkan. 
Sentimen akan dikategorikan sebagai **Positif**, **Negatif**, atau **Netral** berdasarkan polaritas teks.
""")

# Input teks dari pengguna
user_input = st.text_area("Masukkan teks di sini:", placeholder="Contoh: Saya sangat senang hari ini!")

if st.button("Analisis Sentimen"):
    if user_input.strip():
        # Analisis sentimen menggunakan TextBlob
        blob = TextBlob(user_input)
        sentiment_score = blob.sentiment.polarity  # Skor polaritas: -1 (negatif) hingga +1 (positif)
        
        # Klasifikasi sentimen
        if sentiment_score > 0:
            sentiment = "Positif"
        elif sentiment_score < 0:
            sentiment = "Negatif"
        else:
            sentiment = "Netral"

        # Menampilkan hasil analisis
        st.subheader("Hasil Analisis")
        st.write(f"**Teks**: {user_input}")
        st.write(f"**Skor Sentimen**: {sentiment_score:.2f}")
        st.write(f"**Klasifikasi Sentimen**: {sentiment}")
        
        # Visualisasi tambahan
        st.subheader("Visualisasi Sentimen")
        st.bar_chart({"Sentimen": [sentiment_score]})
    else:
        st.warning("Harap masukkan teks untuk dianalisis!")
