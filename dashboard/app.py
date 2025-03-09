import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Analisis TBC", layout="wide")

# Judul Aplikasi
st.title("📊 Dashboard Analisis TBC")
st.write("Aplikasi ini membantu dalam menampilkan data yang diunggah.")

# Fitur Upload File
st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Membaca dataset
        df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
        st.write("### 🔍 Data yang Diunggah")
        st.dataframe(df.head(10))
        
        # Konversi kolom yang seharusnya numerik
        numeric_columns = ["ventilasi", "sanitasi", "perilaku"]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Ubah teks menjadi angka
        
        df[numeric_columns] = df[numeric_columns].fillna(0)  # Gantilah NaN dengan 0
        
        # Menambahkan kolom 'Kategori' berdasarkan kondisi tertentu
        df["Kategori"] = df.apply(lambda row: "Layak" if row["ventilasi"] > 2 and row["dinding"] == "permanen" else "Tidak Layak", axis=1)

        # Menambahkan kolom 'Skor Kelayakan' sebagai contoh perhitungan
        faktor_kelayakan = ["ventilasi", "sanitasi", "perilaku"]
        df["Skor Kelayakan"] = df[faktor_kelayakan].sum(axis=1) / len(faktor_kelayakan)

        st.write("### ✅ Data dengan Kategori dan Skor Kelayakan")
        st.dataframe(df[["Kategori", "Skor Kelayakan"]].head(10))

        # Pilihan Visualisasi
        st.sidebar.header("📊 Pilih Visualisasi")
        visual_option = st.sidebar.selectbox("Pilih Grafik", [
            "Kategori Rumah, Sanitasi, Perilaku Tidak Layak",
            "Jumlah Pasien per Puskesmas",
            "Tren Kunjungan Pasien",
            "Gender vs Jumlah Pasien",
            "Pasien vs Pekerjaan"
        ])
        
        # Visualisasi Berdasarkan Pilihan
        if visual_option == "Kategori Rumah, Sanitasi, Perilaku Tidak Layak":
            kategori_counts = df["Kategori"].value_counts()
            fig, ax = plt.subplots()
            ax.bar(kategori_counts.index, kategori_counts.values, color=['red', 'blue'])
            ax.set_xlabel("Kategori")
            ax.set_ylabel("Jumlah")
            ax.set_title("Distribusi Kategori Rumah Layak dan Tidak Layak")
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.info("Silakan upload file CSV untuk menampilkan data.")
