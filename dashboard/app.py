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
        
        # Pastikan kolom yang diperlukan ada dalam dataset
        required_columns = {"status_rumah", "sarana_air_bersih", "jamban", "perilaku_merokok", "membersihkan_rumah"}
        if required_columns.issubset(df.columns):
            # Fungsi untuk menghitung jumlah dan persentase "Tidak Layak"
            def calculate_percentage(column, condition):
                total = len(df)
                tidak_layak = df[df[column].str.strip().str.lower() == condition.lower()].shape[0]
                persentase = (tidak_layak / total * 100) if total > 0 else 0
                return tidak_layak, persentase
            
            # Perhitungan jumlah dan persentase berdasarkan dataset
            jumlah_rumah_tidak_layak, persentase_tidak_layak_rumah = calculate_percentage("status_rumah", "Tidak Layak")
            jumlah_sanitasi_tidak_layak = df[(df["sarana_air_bersih"].str.strip().str.lower() == "tidak layak") | 
                                              (df["jamban"].str.strip().str.lower() == "tidak layak")].shape[0]
            persentase_tidak_layak_sanitasi = (jumlah_sanitasi_tidak_layak / len(df) * 100) if len(df) > 0 else 0
            
            jumlah_perilaku_tidak_baik = df[(df["perilaku_merokok"].str.strip().str.lower() == "ya") | 
                                             (df["membersihkan_rumah"].str.strip().str.lower() == "jarang")].shape[0]
            persentase_tidak_baik_perilaku = (jumlah_perilaku_tidak_baik / len(df) * 100) if len(df) > 0 else 0
            
            kategori = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
            persentase = [persentase_tidak_layak_rumah, persentase_tidak_layak_sanitasi, persentase_tidak_baik_perilaku]
            jumlah = [jumlah_rumah_tidak_layak, jumlah_sanitasi_tidak_layak, jumlah_perilaku_tidak_baik]
            
            # Mengurutkan data dari terbesar ke terkecil
            sorted_indices = sorted(range(len(persentase)), key=lambda i: persentase[i], reverse=True)
            kategori = [kategori[i] for i in sorted_indices]
            persentase = [persentase[i] for i in sorted_indices]
            jumlah = [jumlah[i] for i in sorted_indices]
            
            # Menampilkan Bar Chart
            st.write("### 📊 Persentase Tidak Layak")
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(kategori, persentase, color=['red', 'orange', 'blue'])
            ax.set_xlabel("Kategori")
            ax.set_ylabel("Persentase (%)")
            ax.set_title("Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
            ax.set_ylim(0, 100)
            ax.grid(axis="y", linestyle="--", alpha=0.7)
            for i, v in enumerate(persentase):
                ax.text(i, v + 2, f"{v:.2f}%", ha="center", fontsize=10)
            st.pyplot(fig)
            
            # Menampilkan Pie Chart
            st.write("### 🎯 Distribusi Tidak Layak dalam Pie Chart")
            fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
            ax_pie.pie(persentase, labels=kategori, autopct='%1.1f%%', colors=['red', 'orange', 'blue'], startangle=140)
            ax_pie.axis('equal')
            st.pyplot(fig_pie)
            
            # Menampilkan Tabel Hasil
            st.write("### 📋 Tabel Persentase dan Jumlah Tidak Layak")
            hasil_df = pd.DataFrame({"Kategori": kategori, "Jumlah": jumlah, "Persentase (%)": persentase})
            st.dataframe(hasil_df)
        else:
            st.error("Kolom yang diperlukan tidak ditemukan dalam dataset. Pastikan dataset memiliki format yang benar.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.info("Silakan upload file CSV untuk memulai analisis.")
