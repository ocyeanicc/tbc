import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit UI
st.title("Dashboard Analisis TBC")
st.write("Unggah file CSV untuk dianalisis.")

# File uploader
uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Mencoba membaca file CSV dengan deteksi otomatis delimiter
        df = pd.read_csv(uploaded_file, sep=None, engine="python")
        st.success("File berhasil dibaca!")
        
        # Menampilkan data
        st.subheader("Data yang Digunakan")
        st.dataframe(df.head())

        # Pastikan kolom yang diperlukan ada dalam dataset
        required_columns = ['rumah_tidak_layak', 'sanitasi_tidak_layak', 'perilaku_tidak_baik']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error("Kolom yang dibutuhkan tidak ditemukan dalam dataset.")
        else:
            # Menghitung metrik dari data
            total_data = len(df)
            rumah_tidak_layak = (df['rumah_tidak_layak'].sum() / total_data) * 100
            sanitasi_tidak_layak = (df['sanitasi_tidak_layak'].sum() / total_data) * 100
            perilaku_tidak_baik = (df['perilaku_tidak_baik'].sum() / total_data) * 100

            st.write(f"**Persentase Rumah Tidak Layak:** {rumah_tidak_layak:.2f}%")
            st.write(f"**Persentase Sanitasi Tidak Layak:** {sanitasi_tidak_layak:.2f}%")
            st.write(f"**Persentase Perilaku Tidak Baik:** {perilaku_tidak_baik:.2f}%")

            # Pilihan visualisasi
            st.subheader("Pilih Visualisasi")
            opsi_visualisasi = [
                "Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak"
            ]
            pilihan = st.selectbox("Pilih Visualisasi", opsi_visualisasi)

            # Menampilkan visualisasi
            if pilihan == "Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak":
                st.subheader("📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
                fig, ax = plt.subplots()
                kategori = ["Rumah Tidak Layak", "Perilaku Tidak Baik", "Sanitasi Tidak Layak"]
                nilai = [rumah_tidak_layak, perilaku_tidak_baik, sanitasi_tidak_layak]
                warna = ["red", "orange", "blue"]
                bars = ax.bar(kategori, nilai, color=warna)

                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}%', ha='center', va='bottom')

                ax.set_ylabel("Persentase (%)")
                ax.set_xlabel("Kategori")
                ax.set_title("Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
                st.pyplot(fig)
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file CSV: {e}")
        st.write("Cek apakah delimiter di dalam file menggunakan ',' atau ';'.")
