import mysql.connector

def get_connection():
    """
    Fungsi ini mencoba membuat koneksi ke database MySQL dan
    mengembalikan tuple (connection, error). Jika koneksi berhasil,
    error bernilai None; jika gagal, connection bernilai None.
    """
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",   # Gunakan 127.0.0.1 untuk koneksi TCP/IP
            port=3306,          # Port default MySQL
            user="root",        # Sesuaikan dengan user XAMPP
            password="",        # Kosong jika belum diatur password
            database="dashboard_db"  # Ganti dengan nama database Anda
        )
        return conn, None
    except mysql.connector.Error as err:
        return None, err
