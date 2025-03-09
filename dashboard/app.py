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
            "Pasien vs Pekerjaan",
            "Pasien vs Kondisi Lantai Rumah",
            "Pasien vs Jenis Langit-Langit Rumah",
            "Pasien vs Perilaku Merokok",
            "Pasien vs Anggota Keluarga Merokok",
            "Pasien vs Kebiasaan Membuka Jendela Kamar",
            "Pasien vs Jenis Dinding Rumah",
            "Pasien vs Ventilasi Rumah"
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

        elif visual_option == "Jumlah Pasien per Puskesmas":
            puskesmas_counts = df.groupby("puskesmas")["pasien"].count().reset_index()
            puskesmas_counts.columns = ["puskesmas", "jumlah_pasien"]
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(data=puskesmas_counts, x="jumlah_pasien", y="puskesmas", ax=ax)
            ax.set_title("Jumlah Pasien per Puskesmas")
            st.pyplot(fig)
        
        elif visual_option == "Tren Kunjungan Pasien":
            df["date_start"] = pd.to_datetime(df["date_start"], errors="coerce")
            df["year_month"] = df["date_start"].dt.to_period("M")
            date_counts = df.groupby("year_month")["pasien"].count().reset_index()
            fig, ax = plt.subplots()
            sns.lineplot(data=date_counts, x="year_month", y="pasien", marker="o", ax=ax)
            ax.set_title("Tren Kunjungan Pasien")
            st.pyplot(fig)
        
        elif visual_option == "Gender vs Jumlah Pasien":
            gender_counts = df.groupby("gender")["pasien"].count().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(data=gender_counts, x="pasien", y="gender", ax=ax)
            ax.set_title("Gender vs Jumlah Pasien")
            st.pyplot(fig)
        
        elif visual_option == "Pasien vs Pekerjaan":
            pekerjaan_counts = df.groupby("pekerjaan")["pasien"].count().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(data=pekerjaan_counts, x="pasien", y="pekerjaan", ax=ax)
            ax.set_title("Pekerjaan vs Jumlah Pasien")
            st.pyplot(fig)
        
        # Tambahkan visualisasi lainnya sesuai kebutuhan
        
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.info("Silakan upload file CSV untuk menampilkan data.")
