import streamlit as st
import nbformat
import pandas as pd
import matplotlib.pyplot as plt

# Load Jupyter Notebook file
NOTEBOOK_FILE = "/mnt/data/analisis tbc.ipynb"

def load_notebook(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return nbformat.read(f, as_version=4)

def extract_code_cells(nb):
    """Extracts code cells from a Jupyter Notebook"""
    return [cell['source'] for cell in nb.cells if cell.cell_type == 'code']

def extract_markdown_cells(nb):
    """Extracts markdown cells from a Jupyter Notebook"""
    return [cell['source'] for cell in nb.cells if cell.cell_type == 'markdown']

# Streamlit UI
st.title("Dashboard Analisis TBC")
st.write("Berikut adalah tampilan dari file notebook yang telah diunggah.")

notebook = load_notebook(NOTEBOOK_FILE)

# Menampilkan Markdown dari Notebook
st.subheader("Deskripsi Analisis")
markdown_cells = extract_markdown_cells(notebook)
for md in markdown_cells:
    st.markdown(md)

# Menampilkan kode dari Notebook
st.subheader("Kode yang digunakan")
code_cells = extract_code_cells(notebook)
for code in code_cells:
    with st.expander("Lihat Kode"):
        st.code(code, language='python')

# Visualisasi Data (Jika ada DataFrame yang bisa diolah)
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
