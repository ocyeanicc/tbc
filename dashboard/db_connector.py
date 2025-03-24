import mysql.connector
import pandas as pd
import streamlit as st

# Fungsi untuk mendapatkan koneksi ke MySQL
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="tb_analisistbc"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Koneksi database gagal: {err}")
        return None

# Fungsi untuk load data dari MySQL
def load_data_from_mysql():
    conn = get_connection()
    if conn:
        try:
            query = "SELECT * FROM tb_cases"
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return pd.DataFrame(data) if data else pd.DataFrame()
        except mysql.connector.Error as err:
            st.error(f"Error mengambil data: {err}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()

