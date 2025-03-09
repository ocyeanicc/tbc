import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Dashboard Analisis TBC", layout="wide")

# Judul Aplikasi
st.title("📊 Dashboard Analisis TBC")
st.write(
    "Aplikasi ini membantu dalam menganalisis hubungan antara sanitasi, perilaku, rumah, "
    "dan penyakit TBC berdasarkan dataset yang diunggah."
)

# **Fitur Upload File**
st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Membaca dataset dengan pemisah yang sesuai (sesuaikan jika perlu)
        df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')

        # **Menampilkan Data yang Diunggah**
        st.write("### 🔍 Data yang Diunggah")
        st.dataframe(df)  # Menampilkan semua data tanpa limit

        # **Menampilkan Info Dataset secara benar**
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        st.subheader("📋 Info Dataset")
        st.text(info_str)  # Menampilkan info dataset dengan format yang lebih baik

        # **Menampilkan Statistik Dasar**
        st.write("### 📊 Statistik Dasar")
        st.write(df.describe())

        # **Visualisasi Sesuai File IPYNB**
        st.write("### 📈 Visualisasi Data")

        # Pilih Kolom Numerik untuk Visualisasi
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_columns) > 0:
            selected_column = st.selectbox("Pilih kolom untuk histogram:", numeric_columns)

            fig, ax = plt.subplots(figsize=(8, 4))
            sns.histplot(df[selected_column], bins=30, kde=True, ax=ax)
            ax.set_title(f'Distribusi {selected_column}')
            st.pyplot(fig)

        else:
            st.warning("Dataset tidak memiliki kolom numerik untuk divisualisasikan.")

        # **Visualisasi Lanjutan (Sesuaikan dengan IPYNB)**
        st.write("### 📌 Visualisasi Tambahan")
        
        # Contoh: Pie Chart Distribusi Kategori
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        if len(categorical_columns) > 0:
            selected_category = st.selectbox("Pilih kolom kategori untuk pie chart:", categorical_columns)

            fig, ax = plt.subplots()
            df[selected_category].value_counts().plot.pie(autopct='%1.1f%%', ax=ax, cmap='viridis')
            ax.set_ylabel('')
            ax.set_title(f'Distribusi {selected_category}')
            st.pyplot(fig)
        else:
            st.warning("Dataset tidak memiliki kolom kategori untuk divisualisasikan.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")

else:
    st.info("Silakan upload file CSV untuk memulai analisis.")
