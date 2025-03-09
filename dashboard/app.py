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
        # Membaca dataset dengan pemisah ; dan encoding UTF-8
        df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')

        # **Menghitung Persentase Tidak Layak**
        if "Label" in df.columns:
            persentase_tidak_layak_rumah = (df[df["Kategori"] == "Rumah"]["Label"].value_counts(normalize=True).get("Tidak Layak", 0)) * 100
            persentase_tidak_layak_sanitasi = (df[df["Kategori"] == "Sanitasi"]["Label"].value_counts(normalize=True).get("Tidak Layak", 0)) * 100
            persentase_tidak_baik_perilaku = (df[df["Kategori"] == "Perilaku"]["Label"].value_counts(normalize=True).get("Tidak Layak", 0)) * 100

            # **Menampilkan Bar Chart**
            st.write("### 📊 Persentase Tidak Layak")
            kategori = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
            persentase = [persentase_tidak_layak_rumah, persentase_tidak_layak_sanitasi, persentase_tidak_baik_perilaku]

            # Urutkan dari terbesar ke terkecil
            sorted_indices = sorted(range(len(persentase)), key=lambda i: persentase[i], reverse=True)
            kategori = [kategori[i] for i in sorted_indices]
            persentase = [persentase[i] for i in sorted_indices]

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(kategori, persentase, color=['red', 'orange', 'blue'])

            # Menambahkan label
            ax.set_xlabel("Kategori")
            ax.set_ylabel("Persentase (%)")
            ax.set_title("Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
            ax.set_ylim(0, 100)
            ax.grid(axis="y", linestyle="--", alpha=0.7)

            # Menampilkan nilai di atas batang
            for i, v in enumerate(persentase):
                ax.text(i, v + 2, f"{v:.2f}%", ha="center", fontsize=10)

            # Tampilkan Bar Chart
            st.pyplot(fig)

            # **Menampilkan Pie Chart**
            st.write("### 🎯 Distribusi Tidak Layak dalam Pie Chart")
            fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
            ax_pie.pie(persentase, labels=kategori, autopct='%1.1f%%', colors=['red', 'orange', 'blue'], startangle=140)
            ax_pie.axis('equal')  # Agar pie chart berbentuk lingkaran sempurna

            st.pyplot(fig_pie)

        else:
            st.error("Kolom 'Label' atau 'Kategori' tidak ditemukan dalam dataset. Pastikan dataset yang diunggah sesuai format.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")

else:
    st.info("Silakan upload file CSV untuk memulai analisis.")
