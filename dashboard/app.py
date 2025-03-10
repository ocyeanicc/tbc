import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data dengan cache terbaru
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv")  # Pastikan file tersedia di direktori yang benar
        return df
    except FileNotFoundError:
        st.error("❌ File 'data.csv' tidak ditemukan. Pastikan file ada atau unggah file baru.")
        return None

# Sidebar untuk upload file (opsional)
st.sidebar.title("Dashboard Visualisasi Data")
uploaded_file = st.sidebar.file_uploader("Unggah file CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = load_data()

if df is not None:  # Pastikan data ada sebelum menjalankan visualisasi
    option = st.sidebar.selectbox("Pilih Visualisasi", [
        "Presentase Rumah, Sanitasi, dan Perilaku Tidak Layak",
        "Jumlah Pasien per Puskesmas",
        "Tren Kunjungan Pasien",
        "Pekerjaan Pasien",
        "Gender Pasien",
        "Presentase Rumah Layak & Tidak Layak",
        "Presentase Sanitasi Layak & Tidak Layak",
        "Presentase Perilaku Baik & Tidak Baik"
    ])

    # 1️⃣ Presentase Rumah, Sanitasi, dan Perilaku Tidak Layak
    if option == "Presentase Rumah, Sanitasi, dan Perilaku Tidak Layak":
        st.title("Presentase Rumah, Sanitasi, dan Perilaku Tidak Layak")

        labels = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
        values = [df['rumah_tidak_layak'].mean(), df['sanitasi_tidak_layak'].mean(), df['perilaku_tidak_baik'].mean()]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=['#E74C3C', '#3498DB', '#FF7F0E'], startangle=140)
        ax.set_title("Distribusi Faktor Tidak Layak")
        st.pyplot(fig)

    # 2️⃣ Jumlah Pasien per Puskesmas
    elif option == "Jumlah Pasien per Puskesmas":
        st.title("Jumlah Pasien per Puskesmas")
        puskesmas_counts = df['puskesmas'].value_counts()

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=puskesmas_counts.values, y=puskesmas_counts.index, ax=ax, palette="viridis")
        ax.set_xlabel("Jumlah Pasien")
        ax.set_ylabel("Puskesmas")
        ax.set_title("Jumlah Pasien per Puskesmas")
        st.pyplot(fig)

    # 3️⃣ Tren Kunjungan Pasien
    elif option == "Tren Kunjungan Pasien":
        st.title("Tren Kunjungan Pasien")
        df['tanggal'] = pd.to_datetime(df['tanggal'])
        daily_visits = df.groupby(df['tanggal'].dt.date)['pasien'].count()

        fig, ax = plt.subplots()
        ax.plot(daily_visits.index, daily_visits.values, marker='o', linestyle='-')
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Jumlah Pasien")
        ax.set_title("Tren Kunjungan Pasien")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # 4️⃣ Pekerjaan Pasien
    elif option == "Pekerjaan Pasien":
        st.title("Distribusi Pekerjaan Pasien")
        pekerjaan_counts = df['pekerjaan'].value_counts()

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(y=pekerjaan_counts.index, x=pekerjaan_counts.values, ax=ax, palette="coolwarm")
        ax.set_xlabel("Jumlah Pasien")
        ax.set_ylabel("Pekerjaan")
        ax.set_title("Distribusi Pekerjaan Pasien")
        st.pyplot(fig)

    # 5️⃣ Gender Pasien
    elif option == "Gender Pasien":
        st.title("Distribusi Gender Pasien")
        gender_counts = df['gender'].value_counts()

        fig, ax = plt.subplots(figsize=(7, 5))
        sns.barplot(y=gender_counts.index, x=gender_counts.values, ax=ax, palette="pastel")
        ax.set_xlabel("Jumlah Pasien")
        ax.set_ylabel("Gender")
        ax.set_title("Distribusi Gender Pasien")
        st.pyplot(fig)

    # 6️⃣ Presentase Rumah Layak & Tidak Layak
    elif option == "Presentase Rumah Layak & Tidak Layak":
        st.title("Presentase Rumah Layak & Tidak Layak")

        labels = ["Layak", "Tidak Layak"]
        sizes = [df['rumah_layak'].mean(), df['rumah_tidak_layak'].mean()]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#4CAF50', '#E74C3C'], startangle=140, explode=(0, 0.1))
        ax.set_title("Persentase Rumah Layak dan Tidak Layak")
        st.pyplot(fig)

    # 7️⃣ Presentase Sanitasi Layak & Tidak Layak
    elif option == "Presentase Sanitasi Layak & Tidak Layak":
        st.title("Presentase Sanitasi Layak & Tidak Layak")

        labels = ["Layak", "Tidak Layak"]
        sizes = [df['sanitasi_layak'].mean(), df['sanitasi_tidak_layak'].mean()]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#3498DB', '#E74C3C'], startangle=140, explode=(0, 0.1))
        ax.set_title("Persentase Sanitasi Layak dan Tidak Layak")
        st.pyplot(fig)

    # 8️⃣ Presentase Perilaku Baik & Tidak Baik
    elif option == "Presentase Perilaku Baik & Tidak Baik":
        st.title("Presentase Perilaku Baik & Tidak Baik")

        labels = ["Baik", "Tidak Baik"]
        sizes = [df['perilaku_baik'].mean(), df['perilaku_tidak_baik'].mean()]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#1F77B4', '#FF7F0E'], startangle=140, explode=(0, 0.1))
        ax.set_title("Persentase Perilaku Baik dan Tidak Baik")
        st.pyplot(fig)

else:
    st.warning("⚠️ Data tidak tersedia. Silakan unggah file CSV atau pastikan 'data.csv' ada di direktori yang benar.")
