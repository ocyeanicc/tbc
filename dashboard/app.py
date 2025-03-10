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

        # Membersihkan nama kolom (menghapus spasi tersembunyi dan mengubah ke huruf kecil)
        df.columns = df.columns.str.strip().str.lower()

        st.write("### 🔍 Data yang Diunggah")
        st.dataframe(df.head(10))

        # Pastikan kolom yang diperlukan ada dalam dataset
        required_columns = ["ventilasi", "sarana_air_bersih", "perilaku_merokok", "dinding"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Kolom yang hilang: {', '.join(missing_columns)}. Pastikan CSV memiliki kolom ini.")
            st.stop()

        # Konversi kolom ke tipe numerik
        for col in ["ventilasi", "sarana_air_bersih", "perilaku_merokok"]:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Menentukan kategori berdasarkan kondisi
        df["kategori"] = df.apply(
            lambda row: "Layak" if row["ventilasi"] > 2 and row["dinding"].strip().lower() == "permanen" else "Tidak Layak",
            axis=1
        )

        # Menambahkan kolom 'Skor Kelayakan'
        df["skor_kelayakan"] = df[["ventilasi", "sarana_air_bersih", "perilaku_merokok"]].mean(axis=1)

        st.write("### ✅ Data dengan Kategori dan Skor Kelayakan")
        st.dataframe(df[["kategori", "skor_kelayakan"]].head(10))

        # Pilihan Visualisasi
        st.sidebar.header("📊 Pilih Visualisasi")
        visual_option = st.sidebar.selectbox("Pilih Grafik", [
            "Distribusi Kategori Rumah",
            "Jumlah Pasien per Puskesmas",
            "Tren Kunjungan Pasien",
            "Gender vs Jumlah Pasien",
            "Pasien vs Pekerjaan"
        ])
        
        # Visualisasi Berdasarkan Pilihan
        if visual_option == "Distribusi Kategori Rumah":
            kategori_counts = df["kategori"].value_counts()
            fig, ax = plt.subplots()
            ax.bar(kategori_counts.index, kategori_counts.values, color=['red', 'blue'])
            ax.set_xlabel("Kategori")
            ax.set_ylabel("Jumlah")
            ax.set_title("Distribusi Kategori Rumah Layak dan Tidak Layak")
            st.pyplot(fig)

        elif visual_option == "Jumlah Pasien per Puskesmas" and "puskesmas" in df.columns:
            puskesmas_counts = df["puskesmas"].value_counts()
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x=puskesmas_counts.values, y=puskesmas_counts.index, ax=ax)
            ax.set_title("Jumlah Pasien per Puskesmas")
            st.pyplot(fig)

        elif visual_option == "Tren Kunjungan Pasien" and "date_start" in df.columns:
            df["date_start"] = pd.to_datetime(df["date_start"], errors="coerce")
            date_counts = df["date_start"].dt.to_period("M").value_counts().sort_index()
            fig, ax = plt.subplots()
            date_counts.plot(kind='line', marker="o", ax=ax)
            ax.set_title("Tren Kunjungan Pasien")
            ax.set_xlabel("Bulan")
            ax.set_ylabel("Jumlah Pasien")
            st.pyplot(fig)

        elif visual_option == "Gender vs Jumlah Pasien" and "gender" in df.columns:
            gender_counts = df["gender"].value_counts()
            fig, ax = plt.subplots()
            sns.barplot(x=gender_counts.index, y=gender_counts.values, ax=ax)
            ax.set_title("Gender vs Jumlah Pasien")
            st.pyplot(fig)

        elif visual_option == "Pasien vs Pekerjaan" and "pekerjaan" in df.columns:
            pekerjaan_counts = df["pekerjaan"].value_counts()
            fig, ax = plt.subplots()
            sns.barplot(x=pekerjaan_counts.values, y=pekerjaan_counts.index, ax=ax)
            ax.set_title("Pekerjaan vs Jumlah Pasien")
            st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.info("Silakan upload file CSV untuk menampilkan data.")
