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
        # Membaca dataset dengan pemisah yang sesuai (bisa ',' atau ';')
        df = pd.read_csv(uploaded_file, sep=None, engine='python')
        
        # Menampilkan beberapa baris pertama dataset
        st.write("### 🔍 Data Awal:")
        st.dataframe(df.head())
        
        # Menampilkan nama kolom agar pengguna bisa melihat struktur dataset
        st.write("### 🏷️ Nama Kolom dalam Dataset:")
        st.write(df.columns.tolist())
        
        # Mencari nama kolom yang mirip dengan 'Kategori' dan 'Label'
        kategori_col = next((col for col in df.columns if "kategori" in col.lower()), None)
        label_col = next((col for col in df.columns if "label" in col.lower()), None)
        
        if kategori_col and label_col:
            # Menghitung persentase kategori yang tidak layak
            def calculate_percentage(kategori_name):
                subset = df[df[kategori_col].str.strip() == kategori_name]
                return (subset[label_col].str.strip().value_counts(normalize=True).get("Tidak Layak", 0)) * 100
            
            persentase_tidak_layak_rumah = calculate_percentage("Rumah")
            persentase_tidak_layak_sanitasi = calculate_percentage("Sanitasi")
            persentase_tidak_baik_perilaku = calculate_percentage("Perilaku")

            # Menampilkan Bar Chart
            st.write("### 📊 Persentase Tidak Layak")
            kategori = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
            persentase = [persentase_tidak_layak_rumah, persentase_tidak_layak_sanitasi, persentase_tidak_baik_perilaku]
            
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
        
        else:
            st.error("Kolom yang sesuai tidak ditemukan dalam dataset. Pastikan dataset memiliki format yang benar.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.info("Silakan upload file CSV untuk memulai analisis.")
