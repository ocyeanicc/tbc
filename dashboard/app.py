import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Kelayakan", layout="wide")

# Judul Aplikasi
st.title("📊 Dashboard Kelayakan Rumah, Sanitasi, dan Perilaku")

# Sidebar untuk mengunggah dataset
st.sidebar.header("📂 Upload Dataset")
uploaded_file_rumah = st.sidebar.file_uploader("Upload Data Rumah", type=["csv"])
uploaded_file_sanitasi = st.sidebar.file_uploader("Upload Data Sanitasi", type=["csv"])
uploaded_file_perilaku = st.sidebar.file_uploader("Upload Data Perilaku", type=["csv"])

# Menentukan threshold kelayakan
threshold = 70

def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
        return df
    return None

# Membaca data
df_rumah = load_data(uploaded_file_rumah)
df_sanitasi = load_data(uploaded_file_sanitasi)
df_perilaku = load_data(uploaded_file_perilaku)

# Jika semua data telah diunggah
if df_rumah is not None and df_sanitasi is not None and df_perilaku is not None:
    
    # Fungsi untuk melabeli berdasarkan skor kelayakan
    def label_kelayakan(skor):
        return "Layak" if skor >= threshold else "Tidak Layak"

    # Menambahkan kolom label ke masing-masing DataFrame
    df_rumah["Label"] = df_rumah["Skor Kelayakan"].apply(label_kelayakan)
    df_sanitasi["Label"] = df_sanitasi["Skor Kelayakan"].apply(label_kelayakan)
    df_perilaku["Label"] = df_perilaku["Skor Kelayakan"].apply(label_kelayakan)

    # Menghitung persentase "Tidak Layak" untuk rumah, sanitasi, dan perilaku
    persentase_tidak_layak_rumah = (df_rumah[df_rumah["Label"] == "Tidak Layak"].shape[0] / df_rumah.shape[0]) * 100
    persentase_tidak_layak_sanitasi = (df_sanitasi[df_sanitasi["Label"] == "Tidak Layak"].shape[0] / df_sanitasi.shape[0]) * 100
    persentase_tidak_baik_perilaku = (df_perilaku[df_perilaku["Label"] == "Tidak Layak"].shape[0] / df_perilaku.shape[0]) * 100

    # Menampilkan hasil
    st.write(f"**Persentase Rumah Tidak Layak:** {persentase_tidak_layak_rumah:.2f}%")
    st.write(f"**Persentase Sanitasi Tidak Layak:** {persentase_tidak_layak_sanitasi:.2f}%")
    st.write(f"**Persentase Perilaku Tidak Baik:** {persentase_tidak_baik_perilaku:.2f}%")

    # Dropdown untuk memilih visualisasi
    st.write("### Pilih Visualisasi")
    options = ["📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak"]
    selected_option = st.selectbox("Pilih Visualisasi", options)

    if selected_option == "📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak":
        st.subheader("📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")

        # Data untuk grafik
        kategori = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
        persentase = [persentase_tidak_layak_rumah, persentase_tidak_layak_sanitasi, persentase_tidak_baik_perilaku]

        # Mengurutkan data dari terbesar ke terkecil
        sorted_indices = sorted(range(len(persentase)), key=lambda i: persentase[i], reverse=True)
        kategori = [kategori[i] for i in sorted_indices]
        persentase = [persentase[i] for i in sorted_indices]

        # Membuat bar chart
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['red', 'orange', 'blue']
        ax.bar(kategori, persentase, color=[colors[i] for i in sorted_indices])

        # Menambahkan label
        ax.set_xlabel("Kategori")
        ax.set_ylabel("Persentase (%)")
        ax.set_title("Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
        ax.set_ylim(0, 100)  # Batas sumbu Y dari 0 hingga 100%
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        # Menampilkan nilai di atas batang
        for i, v in enumerate(persentase):
            ax.text(i, v + 2, f"{v:.2f}%", ha="center", fontsize=10)

        # Menampilkan grafik di Streamlit
        st.pyplot(fig)

else:
    st.info("Silakan unggah ketiga file dataset (Rumah, Sanitasi, Perilaku) untuk memulai analisis.")
