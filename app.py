import streamlit as st
import pandas as pd
from nltk.tag import CRFTagger
from textblob import TextBlob  # Contoh untuk analisis sentimen sederhana
import urllib.request  # Untuk mengunduh file

# Unduh model CRF jika belum ada
MODEL_URL = "https://raw.githubusercontent.com/dhavinaocxa/latihan-datmin/main/all_indo_man_tag_corpus_model.crf.tagger"
MODEL_PATH = "all_indo_man_tag_corpus_model.crf.tagger"

try:
    # Cek apakah file model sudah ada
    with open(MODEL_PATH, "r") as f:
        pass
except FileNotFoundError:
    st.write("Mengunduh model CRF...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

# Judul aplikasi
st.title("POS Tagging, Filter Nouns, dan Analisis Sentimen")

# Upload file
uploaded_file = st.file_uploader("Upload dataset CSV Anda", type=["csv"])
if uploaded_file is not None:
    try:
        # Baca file CSV
        data = pd.read_csv(uploaded_file, encoding='ISO-8859-1')  # Sesuaikan encoding dengan dataset Anda
        st.write("Dataset asli:")
        st.dataframe(data.head())  # Tampilkan dataset asli

        # Asumsi kolom tweet bernama 'tweet'
        if 'tweet' in data.columns:
            tweets = data['tweet']

            # POS Tagging
            st.write("Proses POS Tagging...")
            ct = CRFTagger()
            ct.set_model_file(MODEL_PATH)  # Path ke model CRF

            # Tagging setiap tweet
            tagged_tweets = [ct.tag_sents([tweet.split()])[0] for tweet in tweets]

            # Tambahkan hasil POS tagging ke dataset
            data['pos_tagging'] = tagged_tweets

            # Filter hanya nouns
            filtered_tweets = []
            for tagged in tagged_tweets:
                nouns = [word for word, tag in tagged if tag in ['NN', 'NNS', 'NNP', 'NNPS']]
                filtered_tweets.append(" ".join(nouns))

            data['filtered_nouns'] = filtered_tweets

            # Periksa dan hapus nilai kosong
            st.write("Memeriksa nilai kosong pada dataset...")
            data.dropna(subset=['filtered_nouns'], inplace=True)

            if data.empty:
                st.error("Dataset tidak memiliki data yang valid setelah memfilter nilai kosong!")
            else:
                # Analisis Sentimen menggunakan TextBlob (demo)
                st.write("Proses Analisis Sentimen...")
                sentiments = []
                for tweet in data['filtered_nouns']:
                    analysis = TextBlob(tweet)
                    if analysis.sentiment.polarity > 0:
                        sentiments.append("positif")
                    elif analysis.sentiment.polarity < 0:
                        sentiments.append("negatif")
                    else:
                        sentiments.append("netral")

                data['predicted_sentiment'] = sentiments

                # Tampilkan dataset hasil tagging dan sentimen
                st.write("Dataset dengan hasil POS tagging dan prediksi sentimen:")
                st.dataframe(data[['tweet', 'pos_tagging', 'filtered_nouns', 'predicted_sentiment']])

                # Download dataset hasil
                csv = data.to_csv(index=False, encoding='utf-8')
                st.download_button(
                    label="Download Dataset Hasil",
                    data=csv,
                    file_name="sentiment_analysis_tweets.csv",
                    mime="text/csv"
                )
        else:
            st.warning("Dataset Anda harus memiliki kolom 'tweet'.")
    except FileNotFoundError:
        st.error("Model CRF tidak ditemukan. Pastikan file model tersedia.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")
