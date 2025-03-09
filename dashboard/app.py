import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Analisis TBC", layout="wide")

# Judul Aplikasi
st.title("📊 Dashboard Analisis TBC")
st.write("Aplikasi ini menganalisis hubungan antara sanitasi, perilaku, rumah, dan penyakit TBC berdasarkan dataset yang diunggah.")

# **Fitur Upload File**
st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Membaca dataset dengan pemisah otomatis
        df = pd.read_csv(uploaded_file, sep=None, engine='python')
        
        # Menampilkan beberapa baris pertama dataset
        st.write("### 🔍 Data Awal:")
        st.dataframe(df.head())
        
        # **Definisi kategori berdasarkan notebook**
        kategori_rumah = ['status_rumah', 'langit_langit', 'lantai', 'dinding',
                          'jendela_kamar_tidur', 'jendela_ruang_keluarga', 'ventilasi',
                          'lubang_asap_dapur', 'pencahayaan']
        
        kategori_sanitasi = ['sarana_air_bersih', 'jamban', 'sarana_pembuangan_air_limbah',
                             'sarana_pembuangan_sampah', 'sampah']
        
        kategori_perilaku = ['perilaku_merokok', 'anggota_keluarga_merokok', 'membuka_jendela_kamar_tidur',
                             'membuka_jendela_ruang_keluarga', 'membersihkan_rumah', 'membuang_tinja']
        
        # Menentukan kriteria "Tidak Layak" (asumsi: nilai 'Tidak' berarti tidak layak)
        def hitung_tidak_layak(kategori):
            return (df[kategori] == 'Tidak').sum().sum()
        
        jumlah_tidak_layak_rumah = hitung_tidak_layak(kategori_rumah)
        jumlah_tidak_layak_sanitasi = hitung_tidak_layak(kategori_sanitasi)
        jumlah_tidak_layak_perilaku = hitung_tidak_layak(kategori_perilaku)
        
        total_data = len(df)
        persentase_tidak_layak_rumah = (jumlah_tidak_layak_rumah / total_data) * 100
        persentase_tidak_layak_sanitasi = (jumlah_tidak_layak_sanitasi / total_data) * 100
        persentase_tidak_layak_perilaku = (jumlah_tidak_layak_perilaku / total_data) * 100
        
        # Menampilkan Bar Chart
        st.write("### 📊 Persentase Tidak Layak")
        kategori = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
        persentase = [persentase_tidak_layak_rumah, persentase_tidak_layak_sanitasi, persentase_tidak_layak_perilaku]
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(kategori, persentase, color=['red', 'orange', 'blue'])
        ax.set_xlabel("Kategori")
        ax.set_ylabel("Persentase (%)")
        ax.set_title("Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
        ax.set_ylim(0, 100)
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        
        # Menampilkan nilai di atas batang
        for i, v in enumerate(persentase):
            ax.text(i, v + 2, f"{v:.2f}%", ha="center", fontsize=10)
        
        st.pyplot(fig)
        
        # Menampilkan Pie Chart
        st.write("### 🎯 Distribusi Tidak Layak dalam Pie Chart")
        fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
        ax_pie.pie(persentase, labels=kategori, autopct='%1.1f%%', colors=['red', 'orange', 'blue'], startangle=140)
        ax_pie.axis('equal')
        st.pyplot(fig_pie)
    
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.info("Silakan upload file CSV untuk memulai analisis.")
