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

        # **Hitung Jumlah & Persentase Kategori "Tidak Layak"**
        if 'kategori' in df.columns:  # Pastikan kolom kategori ada
            kategori_counts = df['kategori'].value_counts()
            kategori_percent = df['kategori'].value_counts(normalize=True) * 100

            kategori_df = pd.DataFrame({
                'Jumlah': kategori_counts,
                'Persentase': kategori_percent.map('{:.2f}%'.format)
            })

            st.write("### 📊 Distribusi Kategori")
            st.dataframe(kategori_df)  # Menampilkan jumlah dan persentase di tabel

            # **Pie Chart Kategori**
            fig, ax = plt.subplots()
            kategori_counts.plot.pie(
                autopct=lambda p: '{:.1f}%\n({:.0f})'.format(p, (p/100)*sum(kategori_counts)), 
                ax=ax, cmap='coolwarm', startangle=90
            )
            ax.set_ylabel('')
            ax.set_title("Distribusi Kategori")
            st.pyplot(fig)

        else:
            st.warning("Kolom 'kategori' tidak ditemukan dalam dataset.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")

else:
    st.info("Silakan upload file CSV untuk memulai analisis.")
