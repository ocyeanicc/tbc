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
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Kolom '{col}' tidak ditemukan dalam dataset. Pastikan CSV memiliki kolom ini.")
                st.stop()

        # Konversi kolom ke tipe numerik untuk menghindari error dalam perhitungan
        for col in ["ventilasi", "sarana_air_bersih", "perilaku_merokok"]:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Menambahkan kolom 'Kategori' berdasarkan kondisi tertentu
        df["Kategori"] = df.apply(lambda row: "Layak" if row["ventilasi"] > 2 and row["dinding"] == "permanen" else "Tidak Layak", axis=1)

        # Menambahkan kolom 'Skor Kelayakan'
        df["Skor Kelayakan"] = df[["ventilasi", "sarana_air_bersih", "perilaku_merokok"]].sum(axis=1) / 3

        st.write("### ✅ Data dengan Kategori dan Skor Kelayakan")
        st.dataframe(df[["Kategori", "Skor Kelayakan"]].head(10))

        # Menghitung persentase kategori tidak layak
        total_data = len(df)
        persentase_tidak_layak_rumah = (df[df["Kategori"] == "Tidak Layak"].shape[0] / total_data) * 100
        persentase_tidak_layak_sanitasi = (df[df["sarana_air_bersih"] == 0].shape[0] / total_data) * 100
        persentase_tidak_baik_perilaku = (df[df["perilaku_merokok"] == 1].shape[0] / total_data) * 100

        # Pilihan Visualisasi
        st.sidebar.header("📊 Pilih Visualisasi")
        visual_option = st.sidebar.selectbox("Pilih Grafik", [
            "Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak",
            "Jumlah Pasien per Puskesmas",
            "Tren Kunjungan Pasien",
            "Gender vs Jumlah Pasien",
            "Pasien vs Pekerjaan"
        ])
        
        # Visualisasi Berdasarkan Pilihan
        if visual_option == "Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak":
            kategori = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
            persentase = [persentase_tidak_layak_rumah, persentase_tidak_layak_sanitasi, persentase_tidak_baik_perilaku]

            sorted_indices = sorted(range(len(persentase)), key=lambda i: persentase[i], reverse=True)
            kategori = [kategori[i] for i in sorted_indices]
            persentase = [persentase[i] for i in sorted_indices]

            plt.figure(figsize=(8, 5))
            plt.bar(kategori, persentase, color=['red', 'orange', 'blue'])
            plt.xlabel("Kategori")
            plt.ylabel("Persentase (%)")
            plt.title("Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
            plt.ylim(0, 100)
            plt.grid(axis="y", linestyle="--", alpha=0.7)

            for i, v in enumerate(persentase):
                plt.text(i, v + 2, f"{v:.2f}%", ha="center", fontsize=10)
            
            st.pyplot(plt)

        elif visual_option == "Jumlah Pasien per Puskesmas":
            if "puskesmas" in df.columns and "pasien" in df.columns:
                puskesmas_counts = df.groupby("puskesmas")["pasien"].count().reset_index()
                puskesmas_counts.columns = ["puskesmas", "jumlah_pasien"]
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.barplot(data=puskesmas_counts, x="jumlah_pasien", y="puskesmas", ax=ax)
                ax.set_title("Jumlah Pasien per Puskesmas")
                st.pyplot(fig)
            else:
                st.warning("Kolom 'puskesmas' atau 'pasien' tidak ditemukan dalam dataset.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.info("Silakan upload file CSV untuk menampilkan data.")
