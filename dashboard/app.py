import streamlit as st
import pandas as pd

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Analisis TBC", layout="wide")

# Judul Aplikasi
st.title("📊 Dashboard Analisis TBC")
st.write("Aplikasi ini membantu dalam menampilkan data yang diunggah.")

# **Fitur Upload File**
st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Membaca dataset dengan pemisah ; dan encoding UTF-8
        df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
        
        # **Menampilkan Data yang Diunggah**
        st.write("### 🔍 Data yang Diunggah")
        st.dataframe(df.head(10))
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.info("Silakan upload file CSV untuk menampilkan data.")
