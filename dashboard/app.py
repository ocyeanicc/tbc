import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Analisis TBC", layout="wide")

# Judul Aplikasi
st.title("📊 Dashboard Analisis TBC")
st.write("Aplikasi ini membantu dalam menganalisis hubungan antara sanitasi, perilaku, rumah, dan penyakit TBC berdasarkan dataset yang diunggah.")

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

        # **Menampilkan Info Dataset (Diperbaiki)**
        buffer = io.StringIO()
        df.info(buf=buffer)  # ✅ Simpan output info dataset ke buffer
        info_str = buffer.getvalue()  # ✅ Ambil isi buffer sebagai string
        st.text_area("ℹ️ Info Dataset", info_str, height=200)

        # **Menampilkan Statistik Dasar**
        st.write("### 📊 Statistik Dasar")
        st.write(df.describe())

        # **Visualisasi: Histogram dari Kolom Numerik**
        st.write("### 📈 Distribusi Data")
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

        if len(numeric_columns) > 0:
            selected_column = st.selectbox("Pilih kolom untuk histogram:", numeric_columns)
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.histplot(df[selected_column], bins=30, kde=True, ax=ax)
            ax.set_title(f'Distribusi {selected_column}')
            st.pyplot(fig)
        else:
            st.warning("Dataset tidak memiliki kolom numerik untuk divisualisasikan.")

        # **Visualisasi: Korelasi Antar Variabel**
        st.write("### 🔗 Korelasi Antar Variabel")
        if len(numeric_columns) > 1:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(df[numeric_columns].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Dataset memiliki kurang dari dua kolom numerik, tidak dapat menampilkan heatmap korelasi.")
    
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")

else:
    st.info("Silakan upload file CSV untuk memulai analisis.")
