import streamlit as st
import nbformat
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit UI
st.title("Dashboard Analisis TBC")
st.write("Unggah file Jupyter Notebook untuk dianalisis.")

# File uploader
uploaded_file = st.file_uploader("Unggah file Jupyter Notebook", type=["ipynb"])

if uploaded_file is not None:
    try:
        # Membaca file notebook
        notebook = nbformat.read(uploaded_file, as_version=4)
        st.success("File berhasil dibaca!")
        
        # Fungsi untuk mengekstrak sel dari notebook
        def extract_cells(nb, cell_type):
            return [cell['source'] for cell in nb.cells if cell.cell_type == cell_type]

        # Menampilkan Markdown dari Notebook
        st.subheader("Deskripsi Analisis")
        markdown_cells = extract_cells(notebook, "markdown")
        for md in markdown_cells:
            st.markdown(md)

        # Menampilkan kode dari Notebook
        st.subheader("Kode yang digunakan")
        code_cells = extract_cells(notebook, "code")
        for code in code_cells:
            with st.expander("Lihat Kode"):
                st.code(code, language='python')

        # Mencari dan menampilkan DataFrame jika ada
        st.subheader("Visualisasi Data")
        
        def load_dataframe():
            for cell in code_cells:
                if "pd.read" in cell:
                    try:
                        exec_globals = {}
                        exec(cell, exec_globals)
                        for var in exec_globals.values():
                            if isinstance(var, pd.DataFrame):
                                return var
                    except Exception as e:
                        st.error(f"Gagal mengeksekusi kode: {e}")
            return None

        df = load_dataframe()
        if df is not None:
            st.write("Data yang ditemukan:")
            st.dataframe(df.head())

            # Membuat visualisasi sederhana
            st.write("Distribusi Data")
            fig, ax = plt.subplots()
            df.hist(figsize=(8, 6), ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Tidak ditemukan DataFrame dalam notebook.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca notebook: {e}")
