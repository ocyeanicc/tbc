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
        # Membaca dataset dengan pemisah yang sesuai
        df = pd.read_csv(uploaded_file, sep=None, engine='python')
        
        # Menampilkan beberapa baris pertama dataset
        st.write("### 🔍 Data Awal:")
        st.dataframe(df.head())
        
        # Menampilkan nama kolom
        st.write("### 🏷️ Nama Kolom dalam Dataset:")
        st.write(df.columns.tolist())
        
        # Pastikan kolom yang diperlukan ada dalam dataset
        required_columns = {"Kategori", "Label"}
        if required_columns.issubset(df.columns):
            # Menghitung jumlah dan persentase "Tidak Layak" untuk setiap kategori
            kategori_list = ["Rumah", "Sanitasi", "Perilaku"]
            hasil = []
            for kategori in kategori_list:
                total = df[df["Kategori"] == kategori].shape[0]
                tidak_layak = df[(df["Kategori"] == kategori) & (df["Label"] == "Tidak Layak")].shape[0]
                persentase = (tidak_layak / total * 100) if total > 0 else 0
                hasil.append((kategori, tidak_layak, persentase))
            
            # Menampilkan hasil dalam tabel
            st.write("### 📊 Persentase Tidak Layak")
            hasil_df = pd.DataFrame(hasil, columns=["Kategori", "Jumlah Tidak Layak", "Persentase (%)"])
            st.dataframe(hasil_df)
            
            # Menampilkan Bar Chart
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(hasil_df["Kategori"], hasil_df["Persentase (%)"], color=['red', 'orange', 'blue'])
            ax.set_xlabel("Kategori")
            ax.set_ylabel("Persentase (%)")
            ax.set_title("Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
            ax.set_ylim(0, 100)
            ax.grid(axis="y", linestyle="--", alpha=0.7)
            for i, v in enumerate(hasil_df["Persentase (%)"]):
                ax.text(i, v + 2, f"{v:.2f}%", ha="center", fontsize=10)
            st.pyplot(fig)
            
            # Menampilkan Pie Chart
            st.write("### 🎯 Distribusi Tidak Layak dalam Pie Chart")
            fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
            ax_pie.pie(hasil_df["Persentase (%)"], labels=hasil_df["Kategori"], autopct='%1.1f%%', colors=['red', 'orange', 'blue'], startangle=140)
            ax_pie.axis('equal')
            st.pyplot(fig_pie)
        else:
            st.error("Kolom 'Kategori' atau 'Label' tidak ditemukan dalam dataset. Pastikan dataset memiliki format yang benar.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.info("Silakan upload file CSV untuk memulai analisis.")
