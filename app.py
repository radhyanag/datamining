pip install -r requirements.txt

streamlit run app.py

import streamlit as st
import pycrfsuite  # Untuk menggunakan model CRF

# Fungsi untuk memuat dan menggunakan model CRF
def load_crf_model(model_path):
    tagger = pycrfsuite.Tagger()
    tagger.open(model_path)
    return tagger

def analyze_sentiment_crf(tagger, text):
    words = text.split()  # Membagi teks menjadi kata-kata
    features = [{'word': word} for word in words]  # Membuat fitur sederhana
    try:
        prediction = tagger.tag([feat['word'] for feat in features])
        return prediction
    except Exception as e:
        return f"Error dalam analisis: {e}"

# Muat model CRF
model_path = "all_indo_man_tag_corpus_model.crf.tagger"
st.write("Memuat model...")
try:
    crf_tagger = load_crf_model(model_path)
    st.success("Model berhasil dimuat!")
except Exception as e:
    st.error(f"Gagal memuat model: {e}")

# Judul aplikasi
st.title("Aplikasi Analisis Sentimen dengan CRF")

# Deskripsi
st.write("""
Aplikasi ini menganalisis sentimen teks menggunakan model CRF yang telah dilatih. 
Sentimen akan dikategorikan berdasarkan model yang dimuat.
""")

# Input teks dari pengguna
user_input = st.text_area("Masukkan teks di sini:", placeholder="Contoh: Saya sangat senang hari ini!")

if st.button("Analisis Sentimen"):
    if user_input.strip():
        if 'crf_tagger' in locals():
            # Analisis sentimen menggunakan model CRF
            sentiment = analyze_sentiment_crf(crf_tagger, user_input)
            st.subheader("Hasil Analisis")
            st.write(f"**Teks**: {user_input}")
            st.write(f"**Prediksi Sentimen**: {sentiment}")
        else:
            st.error("Model belum dimuat dengan benar. Periksa file model Anda.")
    else:
        st.warning("Harap masukkan teks untuk dianalisis!")
