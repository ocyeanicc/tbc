import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk membaca file CSV dengan fleksibilitas tinggi
def load_uploaded_file(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)  # Coba baca dengan format default
    except pd.errors.ParserError:
        uploaded_file.seek(0)
        try:
            df = pd.read_csv(uploaded_file, delimiter=";")  # Coba delimiter titik koma
        except pd.errors.ParserError:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")  # Coba encoding lain
    return df

# Sidebar untuk unggah file
st.sidebar.title("📊 Dashboard Visualisasi Data")
uploaded_file = st.sidebar.file_uploader("📂 Unggah file CSV", type=["csv"])

if uploaded_file is not None:
    df = load_uploaded_file(uploaded_file)

    # Normalisasi nama kolom agar tidak error (menghapus spasi & lowercase)
    df.columns = df.columns.str.strip().str.lower()

    st.sidebar.success("✅ File CSV berhasil diunggah!")

    # Menampilkan daftar nama kolom agar bisa dicek
    st.sidebar.write("🔍 **Kolom dalam file:**")
    st.sidebar.write(df.columns.tolist())

    # Pilihan visualisasi
    option = st.sidebar.selectbox("📊 Pilih Visualisasi", [
        "Presentase Rumah, Sanitasi, dan Perilaku Tidak Layak",
        "Jumlah Pasien per Puskesmas",
        "Tren Kunjungan Pasien",
        "Pekerjaan Pasien",
        "Gender Pasien",
        "Presentase Rumah Layak & Tidak Layak",
        "Presentase Sanitasi Layak & Tidak Layak",
        "Presentase Perilaku Baik & Tidak Baik",
    ])

    # 1️⃣ Presentase Rumah, Sanitasi, dan Perilaku Tidak Layak
    if option == "Presentase Rumah, Sanitasi, dan Perilaku Tidak Layak":
        st.title("🏡 Presentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
        
        # Sesuaikan dengan dataset
        if all(col in df.columns for col in ["rumah_tidak_layak", "sanitasi_tidak_layak", "perilaku_tidak_baik"]):
            labels = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
            values = [df["rumah_tidak_layak"].mean(), df["sanitasi_tidak_layak"].mean(), df["perilaku_tidak_baik"].mean()]

            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%', colors=['#E74C3C', '#3498DB', '#FF7F0E'], startangle=140)
            ax.set_title("Distribusi Faktor Tidak Layak")
            st.pyplot(fig)
        else:
            st.error("⚠️ Kolom yang dibutuhkan tidak ditemukan dalam dataset!")

    # 2️⃣ Jumlah Pasien per Puskesmas
    elif option == "Jumlah Pasien per Puskesmas":
        st.title("🏥 Jumlah Pasien per Puskesmas")

        if "puskesmas" in df.columns:
            puskesmas_counts = df["puskesmas"].value_counts()
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x=puskesmas_counts.values, y=puskesmas_counts.index, ax=ax, palette="viridis")
            ax.set_xlabel("Jumlah Pasien")
            ax.set_ylabel("Puskesmas")
            ax.set_title("Jumlah Pasien per Puskesmas")
            st.pyplot(fig)
        else:
            st.error("⚠️ Kolom 'puskesmas' tidak ditemukan!")

    # 3️⃣ Pekerjaan Pasien
    elif option == "Pekerjaan Pasien":
        st.title("👨‍🔧 Distribusi Pekerjaan Pasien")

        if "pekerjaan" in df.columns:
            pekerjaan_counts = df["pekerjaan"].value_counts()
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(y=pekerjaan_counts.index, x=pekerjaan_counts.values, ax=ax, palette="coolwarm")
            ax.set_xlabel("Jumlah Pasien")
            ax.set_ylabel("Pekerjaan")
            ax.set_title("Distribusi Pekerjaan Pasien")
            st.pyplot(fig)
        else:
            st.error("⚠️ Kolom 'pekerjaan' tidak ditemukan!")

    # 4️⃣ Gender Pasien
    elif option == "Gender Pasien":
        st.title("⚧️ Distribusi Gender Pasien")

        if "gender" in df.columns:
            gender_counts = df["gender"].value_counts()
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.barplot(y=gender_counts.index, x=gender_counts.values, ax=ax, palette="pastel")
            ax.set_xlabel("Jumlah Pasien")
            ax.set_ylabel("Gender")
            ax.set_title("Distribusi Gender Pasien")
            st.pyplot(fig)
        else:
            st.error("⚠️ Kolom 'gender' tidak ditemukan!")

    # 5️⃣ Presentase Rumah Layak & Tidak Layak
    elif option == "Presentase Rumah Layak & Tidak Layak":
        st.title("🏠 Presentase Rumah Layak & Tidak Layak")

        if "rumah_tidak_layak" in df.columns:
            labels = ["Layak", "Tidak Layak"]
            sizes = [1 - df["rumah_tidak_layak"].mean(), df["rumah_tidak_layak"].mean()]

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#4CAF50', '#E74C3C'], startangle=140)
            ax.set_title("Presentase Rumah Layak dan Tidak Layak")
            st.pyplot(fig)
        else:
            st.error("⚠️ Kolom 'rumah_tidak_layak' tidak ditemukan!")

    # 6️⃣ Presentase Sanitasi Layak & Tidak Layak
    elif option == "Presentase Sanitasi Layak & Tidak Layak":
        st.title("🚰 Presentase Sanitasi Layak & Tidak Layak")

        if "sanitasi_tidak_layak" in df.columns:
            labels = ["Layak", "Tidak Layak"]
            sizes = [1 - df["sanitasi_tidak_layak"].mean(), df["sanitasi_tidak_layak"].mean()]

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#3498DB', '#E74C3C'], startangle=140)
            ax.set_title("Presentase Sanitasi Layak dan Tidak Layak")
            st.pyplot(fig)
        else:
            st.error("⚠️ Kolom 'sanitasi_tidak_layak' tidak ditemukan!")

    # 7️⃣ Presentase Perilaku Baik & Tidak Baik
    elif option == "Presentase Perilaku Baik & Tidak Baik":
        st.title("🧑‍⚕️ Presentase Perilaku Baik & Tidak Baik")

        if "perilaku_tidak_baik" in df.columns:
            labels = ["Baik", "Tidak Baik"]
            values = [1 - df["perilaku_tidak_baik"].mean(), df["perilaku_tidak_baik"].mean()]

            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%', colors=['#2ECC71', '#E74C3C'], startangle=140)
            ax.set_title("Presentase Perilaku Baik vs Tidak Baik")
            st.pyplot(fig)
        else:
            st.error("⚠️ Kolom 'perilaku_tidak_baik' tidak ditemukan!")
