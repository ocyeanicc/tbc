import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Kelayakan", layout="wide")

# Judul aplikasi
st.title("📊 Dashboard Kelayakan Rumah, Sanitasi, dan Perilaku")

# Sidebar untuk mengunggah dataset
st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload Data (gabungan rumah, sanitasi, perilaku)", type=["csv"])

# Menentukan threshold kelayakan
threshold = 70

# Jika file diunggah, baca datanya
if uploaded_file is not None:
    # Membaca data
    df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')

    # Pastikan dataset memiliki kolom yang sesuai
    expected_columns = ["Kategori", "Skor Kelayakan"]
    if not all(col in df.columns for col in expected_columns):
        st.error("Dataset harus memiliki kolom: 'Kategori' dan 'Skor Kelayakan'.")
    else:
        # Fungsi untuk melabeli berdasarkan skor kelayakan
        def label_kelayakan(skor):
            return "Layak" if skor >= threshold else "Tidak Layak"

        # Menambahkan kolom label
        df["Label"] = df["Skor Kelayakan"].apply(label_kelayakan)

        # Menghitung jumlah dan persentase "Tidak Layak" untuk setiap kategori
        kategori_tidak_layak = df[df["Label"] == "Tidak Layak"]["Kategori"].value_counts()
        total_per_kategori = df["Kategori"].value_counts()
        persentase_tidak_layak = (kategori_tidak_layak / total_per_kategori) * 100

        # Menampilkan informasi jumlah kategori tidak layak
        st.write("### Jumlah dan Persentase Kategori Tidak Layak")
        for kategori, jumlah in kategori_tidak_layak.items():
            persentase = persentase_tidak_layak[kategori]
            st.write(f"**{kategori}:** {jumlah} kasus ({persentase:.2f}%)")

        # Pilihan visualisasi
        st.write("### Pilih Visualisasi")
        options = ["📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak"]
        selected_option = st.selectbox("Pilih Visualisasi", options)

        if selected_option == "📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak":
            st.subheader("📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")

            # Data untuk grafik
            kategori_list = kategori_tidak_layak.index.tolist()
            persentase_list = persentase_tidak_layak.tolist()

            # Mengurutkan data dari terbesar ke terkecil
            sorted_indices = sorted(range(len(persentase_list)), key=lambda i: persentase_list[i], reverse=True)
            kategori_list = [kategori_list[i] for i in sorted_indices]
            persentase_list = [persentase_list[i] for i in sorted_indices]

            # Membuat bar chart
            fig, ax = plt.subplots(figsize=(8, 5))
            colors = ['red', 'orange', 'blue'][:len(kategori_list)]
            ax.bar(kategori_list, persentase_list, color=colors)

            # Menambahkan label
            ax.set_xlabel("Kategori")
            ax.set_ylabel("Persentase (%)")
            ax.set_title("Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
            ax.set_ylim(0, 100)  # Batas sumbu Y dari 0 hingga 100%
            ax.grid(axis="y", linestyle="--", alpha=0.7)

            # Menampilkan nilai di atas batang
            for i, v in enumerate(persentase_list):
                ax.text(i, v + 2, f"{v:.2f}%", ha="center", fontsize=10)

            # Menampilkan grafik di Streamlit
            st.pyplot(fig)

else:
    st.info("Silakan unggah file dataset untuk memulai analisis.")
