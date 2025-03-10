import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk membaca file CSV dengan fleksibilitas tinggi
def load_uploaded_file(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)  # Baca CSV dengan format default
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
        "Sebaran Usia Pasien",
        "Distribusi Geografis (Kecamatan)",
        "Hubungan Faktor Risiko & Pasien",
    ])

    # 1️⃣ Presentase Rumah, Sanitasi, dan Perilaku Tidak Layak
    if option == "Presentase Rumah, Sanitasi, dan Perilaku Tidak Layak":
        st.title("🏡 Presentase Rumah, Sanitasi, dan Perilaku Tidak Layak")

        required_columns = ["rumah_tidak_layak", "sanitasi_tidak_layak", "perilaku_tidak_baik"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error(f"⚠️ Kolom tidak ditemukan: {missing_columns}")
        else:
            labels = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
            values = [df["rumah_tidak_layak"].mean(), df["sanitasi_tidak_layak"].mean(), df["perilaku_tidak_baik"].mean()]
            
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%', colors=['#E74C3C', '#3498DB', '#FF7F0E'], startangle=140)
            ax.set_title("Distribusi Faktor Tidak Layak")
            st.pyplot(fig)

    # 2️⃣ Jumlah Pasien per Puskesmas
    elif option == "Jumlah Pasien per Puskesmas":
        st.title("🏥 Jumlah Pasien per Puskesmas")

        if "puskesmas" not in df.columns:
            st.error("⚠️ Kolom 'puskesmas' tidak ditemukan dalam file CSV.")
        else:
            puskesmas_counts = df['puskesmas'].value_counts()
            
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x=puskesmas_counts.values, y=puskesmas_counts.index, ax=ax, palette="viridis")
            ax.set_xlabel("Jumlah Pasien")
            ax.set_ylabel("Puskesmas")
            ax.set_title("Jumlah Pasien per Puskesmas")
            st.pyplot(fig)

    # 3️⃣ Tren Kunjungan Pasien
    elif option == "Tren Kunjungan Pasien":
        st.title("📅 Tren Kunjungan Pasien")

        if "tanggal" not in df.columns:
            st.error("⚠️ Kolom 'tanggal' tidak ditemukan dalam file CSV.")
        else:
            df['tanggal'] = pd.to_datetime(df['tanggal'], errors='coerce')
            df = df.dropna(subset=['tanggal'])
            daily_visits = df.groupby(df['tanggal'].dt.date).size()
            
            fig, ax = plt.subplots()
            ax.plot(daily_visits.index, daily_visits.values, marker='o', linestyle='-')
            ax.set_xlabel("Tanggal")
            ax.set_ylabel("Jumlah Pasien")
            ax.set_title("Tren Kunjungan Pasien")
            plt.xticks(rotation=45)
            st.pyplot(fig)

    # 4️⃣ Pekerjaan Pasien
    elif option == "Pekerjaan Pasien":
        st.title("💼 Distribusi Pekerjaan Pasien")

        if "pekerjaan" not in df.columns:
            st.error("⚠️ Kolom 'pekerjaan' tidak ditemukan dalam file CSV.")
        else:
            pekerjaan_counts = df['pekerjaan'].value_counts()
            
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(y=pekerjaan_counts.index, x=pekerjaan_counts.values, ax=ax, palette="coolwarm")
            ax.set_xlabel("Jumlah Pasien")
            ax.set_ylabel("Pekerjaan")
            ax.set_title("Distribusi Pekerjaan Pasien")
            st.pyplot(fig)

    # 5️⃣ Gender Pasien
    elif option == "Gender Pasien":
        st.title("🚻 Distribusi Gender Pasien")

        if "gender" not in df.columns:
            st.error("⚠️ Kolom 'gender' tidak ditemukan dalam file CSV.")
        else:
            gender_counts = df['gender'].value_counts()
            
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.barplot(y=gender_counts.index, x=gender_counts.values, ax=ax, palette="pastel")
            ax.set_xlabel("Jumlah Pasien")
            ax.set_ylabel("Gender")
            ax.set_title("Distribusi Gender Pasien")
            st.pyplot(fig)

    # 6️⃣ Sebaran Usia Pasien
    elif option == "Sebaran Usia Pasien":
        st.title("📊 Sebaran Usia Pasien")

        if "usia" not in df.columns:
            st.error("⚠️ Kolom 'usia' tidak ditemukan dalam file CSV.")
        else:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.histplot(df["usia"], bins=20, kde=True, ax=ax, color="purple")
            ax.set_xlabel("Usia")
            ax.set_ylabel("Frekuensi")
            ax.set_title("Sebaran Usia Pasien")
            st.pyplot(fig)

    # 7️⃣ Distribusi Geografis (Kecamatan)
    elif option == "Distribusi Geografis (Kecamatan)":
        st.title("🗺️ Distribusi Pasien per Kecamatan")

        if "kecamatan" not in df.columns:
            st.error("⚠️ Kolom 'kecamatan' tidak ditemukan dalam file CSV.")
        else:
            kecamatan_counts = df["kecamatan"].value_counts()
            
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x=kecamatan_counts.values, y=kecamatan_counts.index, ax=ax, palette="muted")
            ax.set_xlabel("Jumlah Pasien")
            ax.set_ylabel("Kecamatan")
            ax.set_title("Distribusi Pasien per Kecamatan")
            st.pyplot(fig)

    # 8️⃣ Hubungan Faktor Risiko & Pasien
    elif option == "Hubungan Faktor Risiko & Pasien":
        st.title("🔍 Korelasi Faktor Risiko & Pasien")

        numeric_df = df.select_dtypes(include=['number'])
        corr_matrix = numeric_df.corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        ax.set_title("Korelasi Antar Faktor")
        st.pyplot(fig)

else:
    st.warning("⚠️ Silakan unggah file CSV yang valid.")
