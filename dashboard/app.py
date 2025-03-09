import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import KNNImputer

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Analisis TBC", layout="wide")
st.title("📊 Dashboard Analisis TBC")
st.write("Aplikasi ini menganalisis hubungan antara sanitasi, perilaku, rumah, dan penyakit TBC.")

# **Fitur Upload File**
st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
        st.write("### 🔍 Data yang Diunggah")
        st.dataframe(df.head(10))

        # **Menampilkan Info Dataset**
        buffer = []
        df.info(buf=buffer.append)
        info_str = "\n".join(buffer)
        st.text_area("ℹ️ Info Dataset", info_str, height=200)
        
        # **Menampilkan Missing Values**
        missing_values = df.isnull().sum()
        missing_percentage = (missing_values / len(df)) * 100
        missing_data = pd.DataFrame({"Missing Values": missing_values, "Percentage": missing_percentage})
        missing_data = missing_data[missing_data["Missing Values"] > 0]
        st.write("### ❌ Missing Values")
        st.dataframe(missing_data.sort_values(by="Percentage", ascending=False))
        
        # **Imputasi Missing Values**
        kolom_numerik = df.select_dtypes(include=['number']).columns
        kolom_kategori = df.select_dtypes(include=['object']).columns
        
        # Imputasi untuk kolom kategori dengan mode
        df[kolom_kategori] = df[kolom_kategori].apply(lambda x: x.fillna(x.mode()[0]))
        
        # Imputasi untuk kolom numerik dengan KNN Imputer
        imputer = KNNImputer(n_neighbors=5)
        df[kolom_numerik] = imputer.fit_transform(df[kolom_numerik])
        
        st.success("Imputasi Missing Values selesai!")
        
        # **Visualisasi Distribusi Kolom**
        st.write("### 📈 Distribusi Data")
        selected_column = st.selectbox("Pilih kolom untuk histogram:", kolom_numerik)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(df[selected_column], bins=30, kde=True, ax=ax)
        ax.set_title(f'Distribusi {selected_column}')
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
else:
    st.info("Silakan upload file CSV untuk memulai analisis.")
