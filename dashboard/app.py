import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io as pio  
import geopandas as gpd
from streamlit_folium import folium_static
from datetime import datetime
from io import BytesIO, StringIO
import mysql.connector
import csv
from db_connector import get_connection, load_data_from_mysql
import json
from streamlit_folium import st_folium
import folium 
from folium.plugins import Search
from sqlalchemy import create_engine
from shapely.geometry import shape
from streamlit_folium import st_folium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

#  Atur tema Seaborn
sns.set_theme(style="whitegrid")

st.set_page_config(layout="wide")

# Inisialisasi session_state untuk menyimpan data CSV, data manual, dan data gabungan
# --- Selalu muat data dari MySQL setiap kali aplikasi dijalankan ---
# --- Inisialisasi session_state ---
if "csv_data" not in st.session_state:
    st.session_state["csv_data"] = pd.DataFrame()
if "manual_data" not in st.session_state:
    st.session_state["manual_data"] = pd.DataFrame()

# Selalu muat data dari MySQL setiap kali aplikasi dijalankan
st.session_state["data"] = load_data_from_mysql()

# Fungsi untuk menampilkan label kolom tanpa underscore
def display_label(col_name: str) -> str:
    return " ".join(word.capitalize() for word in col_name.split("_"))

def insert_mysql_data(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO tb_cases({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(data.values()))
        conn.commit()
    except Exception as e:
        st.error(f"Error saat menambahkan data: {e}")
    finally:
        cursor.close()
        conn.close()
        
        
# Tampilkan elemen di sidebar
logo_url = "https://raw.githubusercontent.com/lizyyaaa/tbc/main/dashboard/download%20(1).png" 
st.sidebar.image(logo_url, use_container_width=True)

# Title dan Subheader di sidebar
st.sidebar.title("Dashboard Analisis TBC")
st.sidebar.subheader("Bidang P2P")
st.sidebar.markdown("---")

# Contoh info box untuk menambah keterangan di sidebar
st.sidebar.info("Silakan pilih halaman di bawah ini.")

# 6) Navigasi menggunakan radio button di sidebar dengan emoji
# Gunakan tiga opsi navigasi: Home, Data, dan Visualisasi
nav = st.sidebar.radio("🔽 Pilih Halaman", ["🏠 Home", "📊 Data","📈 Visualisasi"])
# --- Global fields_order (pastikan konsisten) ---
fields_order = [
    "puskesmas", "pasien", "age", "gender", "faskes", "city", "regency",
    "kelurahan", "type_tb", "date_start", "tgl_kunjungan", "status_hamil",
    "penyakit", "pekerjaan", "tempat_kerja", "nama_kepala_keluarga",
    "pekerjaan_kepala_keluarga", "total_pendapatan_keluarga_per_bulan",
    "pola_asuh", "status_pernikahan", "status_pernikahan_orang_tua",
    "jumlah_anggota_keluarga", "kepemilikan_jkn", "perilaku_merokok",
    "anggota_keluarga_merokok", "mendapatkan_bantuan", "status_imunisasi",
    "status_gizi", "status_rumah", "luas_rumah", "tipe_rumah",
    "langit_langit", "lantai", "dinding", "jendela_kamar_tidur",
    "jendela_ruang_keluarga", "ventilasi", "lubang_asap_dapur",
    "pencahayaan", "sarana_air_bersih", "jamban",
    "sarana_pembuangan_air_limbah", "sarana_pembuangan_sampah", "sampah",
    "membuka_jendela_kamar_tidur", "membuka_jendela_ruang_keluarga",
    "membersihkan_rumah", "membuang_tinja", "membuang_sampah",
    "kebiasaan_ctps", "memiliki_hewan_ternak", "kandang_hewan"
]

option_dict = {
    "puskesmas": ['Puskesmas Kedungmundu', 'Puskesmas Sekaran', 'Puskesmas Karangdoro', 'Puskesmas Rowosari', 
                  'Puskesmas Bandarharjo', 'Puskesmas Pegandan', 'Puskesmas Mangkang', 'Puskesmas Candilama', 
                  'Puskesmas Karang Malang', 'Puskesmas Ngaliyan', 'Puskesmas Lebdosari', 'Plamongan Sari', 
                  'Puskesmas Purwoyoso', 'Puskesmas Bangetayu', 'Puskesmas Pandanaran', 'Puskesmas Mijen', 
                  'Puskesmas Ngesrep', 'Puskesmas Karangayu', 'Puskesmas Tambakaji', 'Puskesmas Padangsari', 
                  'Puskesmas Halmahera', 'Puskesmas Miroto', 'Puskesmas Genuk', 'bulusan', 'Puskesmas Bugangan', 
                  'Puskesmas Tlogosari Wetan', 'Puskesmas Poncol', 'Puskesmas Pudak Payung', 'Puskesmas Kagok', 
                  'Puskesmas Krobokan', 'Puskesmas Manyaran', 'Puskesmas Tlogosari Kulon', 'Puskesmas Karanganyar', 
                  'Puskesmas Gunungpati', 'Puskesmas Ngemplak Simongan', 'Puskesmas Srondol', 'Puskesmas Gayamsari', 
                  'Puskesmas Bulu Lor'],
    "gender": ['L', 'P'],
    "city": ['Semarang', 'Luar Kota'],
    "regency": ['Tembalang', 'Gunungpati', 'Semarang Timur', 'Semarang Utara', 'Gajahmungkur', 'Tugu', 'Candisari', 
                'Mijen', 'Ngaliyan', 'Semarang Barat', 'Pedurungan', 'Genuk', 'Semarang Selatan', 'Banyumanik', 
                'Luar Kota', 'Semarang Tengah', 'Gayamsari'],
    "kelurahan": ['Tandang', 'Sukorejo', 'Sendangmulyo', 'Sambiroto', 'Kemijen', 'Rejomulyo', 'Sendangguwo', 
                  'Meteseh', 'Dadapsari', 'Petompon', 'Karangrejo', 'Lempongsari', 'Bendungan', 'Mangkang Wetan', 
                  'Karanganyar Gunung', 'Sampangan', 'Tanjungmas', 'Kalisegoro', 'Karangmalang', 'Wates', 'Sekaran', 
                  'Jangli', 'Kalibanteng Kulon', 'Penggaron Kidul', 'Bandarharjo', 'Purwoyoso', 'Pedurungan Kidul', 
                  'Kedungmundu', 'Patemon', 'Sembungharjo', 'Bringin', 'Randusari', 'Wonoplumbon', 'Rowosari', 
                  'Ngesrep', 'Tinjomoyo', 'Karangayu', 'Podorejo', 'Karangroto', 'Kalipancur', 'Wonosari', 
                  'Sumurboto', 'Plamongansari', 'Padangsari', 'Bambankerep', 'Mangkang Kulon', 'Mangunharjo', 
                  'Pedalangan', 'Jomblang', 'Kedungpane', 'Ngadirgo', 'Cangkiran', 'Luar Kota', 'Rejosari', 
                  'Jatingaleh', 'Tambakaji', 'Mlatibaru', 'Ngaliyan', 'Gabahan', 'Miroto', 'Genuksari', 'Salamanmloyo', 
                  'Bulusan', 'Bugangan', 'Kebonagung', 'Bulustalan', 'Gisikdrono', 'Tambakharjo', 'Muktiharjo Lor', 
                  'Ngijo', 'Mijen', 'Wonolopo', 'Jabungan', 'Kuningan', 'Tlogomulyo', 'Banjardowo', 'Bubakan', 
                  'Gondoriyo', 'Bendan Duwur', 'Gajahmungkur', 'Bendan Ngisor', 'Purwodinatan', 'Kramas', 'Kudu', 
                  'Mugassari', 'Penggaron Lor', 'Bangetayu Wesan', 'Bangunharjo', 'Kembangsari', 'Pandansari', 
                  'Sekayu', 'Karangtempel', 'Gedawang', 'Karangkidul', 'Bojongsalaman', 'Trimulyo', 'Bangetayu Kulon', 
                  'Gebangsari', 'Jatibarang', 'Tambangan', 'Wonodri', 'Pudakpayung', 'Pedurungan Tengah', 'Candi', 
                  'Kranggan', 'Tlogosari Wetan', 'Tawangsari', 'Palebon', 'Mlatibaru', 'Tegalsari', 'Wonotingal', 
                  'Manyaran', 'Kembangarum', 'Barusari', 'Krapyak', 'Gemah', 'Tugurejo', 'Mangunsari', 'Nongkosawit', 
                  'Karangturi', 'Tlogosari Kulon', 'NgemplakSimongan', 'Krobokan', 'Srondol Wetan', 'Banyumanik', 
                  'Gunungpati', 'Jagalan', 'Pindrikan Lor', 'Jatisari', 'Srondol Kulon', 'Randugarut', 'Kaligawe', 
                  'Tawangmas', 'Brumbungan', 'Siwalan', 'Tambakrejo', 'Sadeng', 'Sawah Besar', 'Jatirejo', 'Plalangan', 
                  'Pakintelan', 'Kauman', 'Pandean Lamper', 'Gayamsari', 'Sambirejo', 'Sarirejo', 'Bongsari', 
                  'Pindrikan Kidul', 'Sumurejo', 'Terboyo Wetan', 'Muktiharjo Kidul', 'Pedurungan Lor', 'Kalicari', 
                  'Cabean', 'Karanganyar', 'Panggung Lor', 'Purwosari', 'Panggung Kidul', 'Bulu Lor', 'Plombokan', 
                  'Kaliwiru', 'Pangangan', 'Kalibanteng Kidul', 'Jrakah'],
    "type_tb": [' ', 1.0, 2.0],
    "status_hamil": ['Tidak', 'Ya'],
    "pekerjaan": ['Tidak Bekerja', 'Ibu Rumah Tangga', 'Pegawai Swasta', 'Lainnya', 'Pelajar / Mahasiswa', 
                  'Wiraswasta', 'Nelayan', 'Petani', 'Pensiunan', 'TNI / Polri'],
    "pekerjaan_kepala_keluarga": ['Lainnya', 'Tidak Bekerja', 'Pegawai Swasta', 'Wiraswasta', 'Pelajar / Mahasiswa', 
                                  'Nelayan', 'Ibu Rumah Tangga', 'Petani', 'Pensiunan', 'PNS', 'TNI / Polri'],
    "total_pendapatan_keluarga_per_bulan": ['1.000.000 - < 2.000.000', '2.000.000 - < 3.000.000', '< 1.000.000', '0', 
                                            '3.000.000 - < 4.000.000', '>= 4.000.000'],
    "pola_asuh": ['Orang Tua', 'Lainnya', 'Kakek / Nenek', 'Penitipan'],
    "status_pernikahan": ['Belum Kawin', 'Kawin', 'Cerai Mati', 'Cerai Hidup'],
    "status_pernikahan_orang_tua": ['Kawin', 'Cerai Mati', 'Belum Kawin', 'Cerai Hidup'],
    "kepemilikan_jkn": ['Ya', 'Tidak'],
    "perilaku_merokok": ['Tidak', 'Ya'],
    "anggota_keluarga_merokok": ['Ya', 'Tidak'],
    "mendapatkan_bantuan": ['Tidak', 'Ya'],
    "status_imunisasi": ['Tidak Lengkap', 'Lengkap'],
    "status_gizi": ['Underweight', 'Normal', 'Wasting', 'Kurang', 'Overweight', 'Obesitas'],
    "status_rumah": ['Lainnya', 'Pribadi', 'Orang Tua', 'Kontrak', 'Kost', 'Asrama'],
    "langit_langit": ['Tidak ada', 'Ada'],
    "lantai": ['Ubin/keramik/marmer', 'Tanah', 'Kurang Baik', 'Papan/anyaman bambu/plester retak berdebu', 'Baik'],
    "dinding": ['Permanen (tembok pasangan batu bata yang diplester)', 
                'Semi permanen bata/batu yang tidak diplester/papan kayu', 
                'Bukan tembok (papan kayu/bambu/ilalang)'],
    "jendela_kamar_tidur": ['Tidak ada', 'Ada'],
    "jendela_ruang_keluarga": ['Ada', 'Tidak ada'],
    "ventilasi": ['Kurang Baik', 'Ada,luas ventilasi < 10% dari luas lantai', 'Tidak Ada', 'Baik', 
                  'Ada, luas ventilasi > 10% dari luas lantai'],
    "lubang_asap_dapur": ['Ada, luas ventilasi < 10% dari luas lantai dapur', 'Tidak Ada', 
                          'Ada, luas ventilasi > 10% luas lantai dapur/exhaust vent'],
    "pencahayaan": ['Kurang Baik', 'Tidak terang', 'Baik', 'Terang', 'Kurang jelas untuk membaca normal', 
                    'Kurang terang', 'Dapat digunakan untuk membaca normal'],
    "sarana_air_bersih": ['Ada,bukan milik sendiri & memenuhi syarat kesehatan', 
                          'Ada,milik sendiri & tidak memenuhi syarat kesehatan', 
                          'Ada, bukan milik sendiri & tidak memenuhi syarat kesehatan', 
                          'Ada,milik sendiri & memenuhi syarat kesehatan', 'Tidak Ada'],
    "jamban": ['Ada tutup & septic tank', 'Ada, leher angsa', 'Ada,bukan leher angsa ada tutup & septic tank', 
               'Ada,bukan leher angsa ada tutup & dialirkan ke sungai', 'Tidak Ada'],
    "sarana_pembuangan_air_limbah": ['Ada, diresapkan ke selokan terbuka', 
                                     'Tidak ada, sehingga tergenang dan tidak teratur di halaman/belakang rumah', 
                                     'Ada, bukan milik sendiri & memenuhi syarat kesehatan', 
                                     'Ada, diresapkan tetapi mencemari sumber air (jarak <10m)', 
                                     'Ada, dialirkan ke selokan tertutup ("&"saluran kota) utk diolah lebih lanjut'],
    "sarana_pembuangan_sampah": ['Ada, tetapi tidak kedap air dan tidak tertutup', 'Tidak Ada', 
                                 'Ada, kedap air dan tidak tertutup', 'Ada, kedap air dan tertutup'],
    "sampah": ['Lainnya (Sungai)', 'Dikelola Sendiri (Pilah Sampah)', 'Bakar', 'Petugas', 'dll'],
    "membuka_jendela_kamar_tidur": ['Tidak pernah dibuka', 'Kadang-kadang dibuka', 'Setiap hari dibuka'],
    "membuka_jendela_ruang_keluarga": ['Tidak pernah dibuka', 'Kadang-kadang dibuka', 'Setiap hari dibuka'],
    "membersihkan_rumah": ['Tidak pernah dibersihkan', 'Kadang-kadang', 'Setiap hari dibersihkan'],
    "membuang_tinja": ['Setiap hari ke jamban', 'Dibuang ke sungai/kebun/kolam/sembarangan'],
    "membuang_sampah": ['Dibuang ke sungai/kebun/kolam/sembarangan / dibakar', 
                        'Kadang-kadang dibuang ke tempat sampah', 
                        'Dibuang ke tempat sampah/ada petugas sampah', 
                        'Dilakukan pilah sampah/dikelola dengan baik'],
    "kebiasaan_ctps": ['Tidak pernah CTPS', 'Kadang-kadang CTPS', 'CTPS setiap aktivitas'],
    "memiliki_hewan_ternak": ['Tidak', 'Ya'],
    "kandang_hewan": []  # Kosong, gunakan text_input
}

# ================================
# Halaman Home
# ================================
if nav == "🏠 Home":
    st.title("🏠 Home")

    # --------------------------------------------------
    # 1. Koneksi ke Database menggunakan SQLAlchemy
    # --------------------------------------------------
    DB_URI = "mysql+mysqlconnector://root:@127.0.0.1/tb_analisistbc"  # Ganti sesuai kredensial Anda
    engine = create_engine(DB_URI)


    # --------------------------------------------------
    # 2. Fungsi Memuat Data Pasien dari Database
    # --------------------------------------------------
    def load_data_from_mysql():
        query = "SELECT * FROM tb_cases"  # Pastikan tabel memiliki kolom 'kelurahan' dan 'gender'
        df = pd.read_sql(query, con=engine)
        if "kelurahan" in df.columns:
            df["kelurahan"] = df["kelurahan"].str.lower().str.strip()
        if "gender" in df.columns:
            df["gender"] = df["gender"].str.upper().str.strip()
        return df


    df_raw = load_data_from_mysql()
    if df_raw.empty:
        st.error("Data pasien tidak ditemukan di database.")
        st.stop()
    
    df = load_data_from_mysql()
    if df.empty:
        st.error("Data pasien tidak ditemukan di database.")
        st.stop()

    # --------------------------------------------------
    # 3. Hitung Total Pasien dan Breakdown Gender
    # --------------------------------------------------
    total_pasien = len(df)
    jumlah_laki = len(df[df["gender"] == "L"]) if "gender" in df.columns else 0
    jumlah_perempuan = len(df[df["gender"] == "P"]) if "gender" in df.columns else 0

    
    summary_html = f"""
    <font size="6"><b>Jumlah Pasien</b></font><br><br>
        <table width="100%" border="1" cellspacing="0" cellpadding="5" bgcolor="#F2F2F2">
    <tr bgcolor="#333333">
        <td align="center"><font color="white"><b>Total Pasien</b></font></td>
        <td align="center"><font color="white"><b>Laki-laki</b></font></td>
        <td align="center"><font color="white"><b>Perempuan</b></font></td>
    </tr>
    <tr>
        <td align="center"><font color="purple">{total_pasien}</font></td>
        <td align="center"><font color="blue">{jumlah_laki}</font></td>
        <td align="center"><font color="red">{jumlah_perempuan}</font></td>
    </tr>
    </table>
    """

    st.markdown(summary_html, unsafe_allow_html=True)

    # --------------------------------------------------
    # 4. Fungsi Menghitung Jumlah Pasien per Kelurahan
    # --------------------------------------------------
    def hitung_jumlah_pasien(df):
        df_count = df.groupby("kelurahan").size().reset_index(name="jumlah_pasien")
        return df_count

    df_pasien = hitung_jumlah_pasien(df)

    # --------------------------------------------------
    def load_geojson():
        geojson_path = "semarang_kelurahan.geojson"  # Pastikan file ini ada
        with open(geojson_path, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
        # Normalisasi properti "name" ke lowercase dan hilangkan spasi ekstra
        for feature in geojson_data["features"]:
            if "name" in feature["properties"]:
                feature["properties"]["name"] = feature["properties"]["name"].lower().strip()
        return geojson_data

    geojson_data = load_geojson()

    # --------------------------------------------------
    # 2. Gabungkan Data Pasien ke GeoJSON (menggunakan properti "name")
    # --------------------------------------------------
    # Pastikan df_pasien sudah didefinisikan dengan kolom "kelurahan" dan "jumlah_pasien"
    kelurahan_count = dict(zip(df_pasien["kelurahan"], df_pasien["jumlah_pasien"]))
    for feature in geojson_data["features"]:
        kel = feature["properties"].get("name", "")
        feature["properties"]["jumlah_pasien"] = kelurahan_count.get(kel, 0)

    # --------------------------------------------------
    # 3. Buat Peta dengan Basemap Tanpa Label dan Custom Panes
    # -------------------------------------------------
    # Gunakan basemap tanpa label
    m = folium.Map(
        location=[-6.9667, 110.4167],
        zoom_start=12,
        tiles="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png",
        attr="CartoDB Positron No Labels"
    )
    # Buat custom panes:
    # - Pane "choropleth" untuk layer poligon (z-index rendah)
    # - Pane "labels" untuk layer label (z-index tinggi)
    m.add_child(folium.map.CustomPane("choropleth", z_index=400))
    m.add_child(folium.map.CustomPane("labels", z_index=650))



    # --------------------------------------------------
    # 4. Tambahkan Layer Choropleth ke Pane "choropleth"
    # --------------------------------------------------
    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        name="Choropleth",
        data=df_pasien,
        columns=["kelurahan", "jumlah_pasien"],
        key_on="feature.properties.name",
        fill_color="RdYlGn_r",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Jumlah Pasien TBC per Kelurahan"
    ).add_to(m)
    # Pastikan layer choropleth berada di pane "choropleth"
    choropleth.geojson.options['pane'] = 'choropleth'

    # --------------------------------------------------
    # 5. Tambahkan Layer GeoJSON dengan Tooltip (untuk interaktivitas) ke Pane "choropleth"
    # --------------------------------------------------
    tooltip = folium.GeoJsonTooltip(
        fields=["name", "jumlah_pasien"],
        aliases=["Kelurahan:", "Jumlah Pasien:"],
        localize=True
    )
    geojson_layer = folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            "fillColor": "transparent",
            "color": "black",
            "fillOpacity": 0,
            "weight": 0.5
        },
        highlight_function=lambda feature: {
            "fillColor": "#000000",
            "color": "#000000",
            "fillOpacity": 0.7,
            "weight": 0.1
        },
        tooltip=tooltip,
        pane="choropleth"
    ).add_to(m)

    # Tambahkan plugin pencarian untuk memudahkan mencari kelurahan
    search = Search(
        layer=geojson_layer,
        search_label="name",
        placeholder="Cari kelurahan...",
        collapsed=False,
    )
    search.add_to(m)

    # --------------------------------------------------
    # 6. Tambahkan Layer Tile untuk Label ke Pane "labels"
    # --------------------------------------------------
    # Layer ini hanya berisi tulisan nama kelurahan dan akan selalu berada di atas layer choropleth
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png",
        attr="CartoDB",
        name="Labels",
        overlay=True,
        control=False,
        pane="labels"
    ).add_to(m)

    # --------------------------------------------------
    # 7. Tampilkan Peta pada Streamlit
    # --------------------------------------------------
    st.write("### Peta Persebaran Pasien TBC")
    st.markdown(
        """
        <style>
        /* Menargetkan container streamlit-folium */
        div.stFolium {
            width: 900px !important;
            height: 450px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st_folium(m, width=900, height=450)

    
    # --------------------------------------------------
    # 7. Tampilkan DataFrame Data Pasien di Bawah Peta
    # --------------------------------------------------
    st.write("### Data Pasien (Jumlah per Kelurahan)")
    st.dataframe(df_pasien)

# ================================
# Halaman Data: Input & Upload Data
# ================================
if nav == "📊 Data":
    st.title("📊 Data - Input & Upload Data")
    st.markdown("### Upload file CSV dan masukkan data baru secara manual. Data yang diinput akan digabungkan dan ditampilkan.")
    
    # --- Bagian Upload CSV ---
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            # Baca file sebagai string
            file_contents = uploaded_file.getvalue().decode("utf-8")
            
            # Baca CSV menggunakan StringIO dengan separator ';'
            df_csv = pd.read_csv(
                StringIO(file_contents),
                sep=';',
                engine='python',
                quoting=csv.QUOTE_NONE,
                escapechar='\\',
                skipinitialspace=True,
                encoding='utf-8'
            )

            # Bersihkan nama kolom
            df_csv.columns = [col.split(',')[0].strip() for col in df_csv.columns]

            # Hapus semua jenis kutip (single, double, backtick) di kolom string
            for col in df_csv.select_dtypes(include=["object"]).columns:
                # Hapus " , ' , dan ` 
                df_csv[col] = df_csv[col].str.replace(r'[\"\'`,]+', '', regex=True)
            
            # Simpan data CSV ke MySQL
            try:
                conn = get_connection()
                if conn is None:
                    st.error("Koneksi ke database gagal!")
                else:
                    cursor = conn.cursor()
                    
                    # Ambil kolom dari CSV yang juga ada di fields_order
                    columns = [col for col in fields_order if col in df_csv.columns]
                    df_csv = df_csv[columns]
                    
                    placeholders = ", ".join(["%s"] * len(df_csv.columns))
                    insert_query = f"INSERT INTO tb_cases ({', '.join(df_csv.columns)}) VALUES ({placeholders})"
                    
                    data_rows = [tuple(x) for x in df_csv.to_numpy()]
                    if data_rows:
                        cursor.executemany(insert_query, data_rows)
                        conn.commit()
                        st.success("Data CSV berhasil disimpan ke MySQL!")
                    else:
                        st.warning("Tidak ada baris yang valid untuk disimpan.")
            except Exception as e:
                st.error(f"Terjadi error saat menyimpan CSV ke MySQL: {e}")
            finally:
                if 'cursor' in locals() and cursor is not None:
                    cursor.close()
                if conn is not None:
                    conn.close()
            
            # Update session_state dengan data terbaru dari MySQL
            st.info("Memuat ulang data dari database...")
            st.session_state["data"] = load_data_from_mysql()
            st.success("Data dari database telah diperbarui.")
        except Exception as e:
            st.error(f"Error membaca file: {e}")
    
    # Pastikan "form_key" di session_state ada agar form dapat direfresh
    if "form_key" not in st.session_state:
        st.session_state["form_key"] = 0

    # Tampilkan data gabungan dari MySQL dan CSV (jika ada)
    st.subheader("📊 Data dari MySQL + CSV yang diunggah")
    st.dataframe(st.session_state["data"])

    st.markdown("## Form Input Data Manual Tambahan")

    # --- Form manual dengan key dinamis ---
    with st.form(key=f"manual_form_{st.session_state['form_key']}"):
        input_manual = {}
        for col in fields_order:
            label = col.replace("_", " ").title()
            # Gunakan key yang unik untuk tiap widget dengan menggabungkan form_key
            widget_key = f"{col}_{st.session_state['form_key']}"
            if col == "age":
                input_manual[col] = st.number_input(label, min_value=0, step=1, value=0, key=widget_key)
            elif col in ["date_start", "tgl_kunjungan"]:
                input_manual[col] = st.date_input(label, value=datetime.today(), key=widget_key)
            elif col in option_dict:
                options = option_dict[col]
                if options:
                    input_manual[col] = st.selectbox(label, options, key=widget_key)
                else:
                    input_manual[col] = st.text_input(label, value="", key=widget_key)
            else:
                input_manual[col] = st.text_input(label, value="", key=widget_key)
        submitted_manual = st.form_submit_button("Submit Data Manual Tambahan")

    if submitted_manual:
        df_manual = pd.DataFrame([input_manual])
        # Konversi tanggal ke string
        for col in df_manual.columns:
            if "date" in col or "tgl" in col:
                df_manual[col] = df_manual[col].astype(str)
        try:
            conn = get_connection()
            if conn is not None:
                cursor = conn.cursor()
                # Cek apakah pasien sudah ada
                pasien = df_manual["pasien"].values[0]
                cursor.execute("SELECT COUNT(*) FROM tb_cases WHERE pasien = %s", (pasien,))
                exists = cursor.fetchone()[0] > 0
                if exists:
                    st.warning(f"⚠ Pasien dengan ID {pasien} sudah ada di database. Data tidak disimpan.")
                    # Tampilkan peringatan selama 5 detik tanpa reset form
                    time.sleep(5)
                else:
                    columns = df_manual.columns.tolist()
                    placeholders = ", ".join(["%s"] * len(columns))
                    insert_query = f"INSERT INTO tb_cases ({', '.join(columns)}) VALUES ({placeholders})"
                    data_rows = [tuple(x) for x in df_manual.to_numpy()]
                    cursor.executemany(insert_query, data_rows)
                    conn.commit()
                    st.success("✅ Data berhasil disimpan ke MySQL! Form akan di-reset...")
                    # Reset input session_state dan naikkan form_key untuk reset form
                    for col in fields_order:
                        st.session_state[f"manual_{col}"] = 0 if col == "age" else "" if col not in ["date_start", "tgl_kunjungan"] else datetime.today()
                    st.session_state["data"] = load_data_from_mysql()  # Update data
                    st.session_state["form_key"] += 1
                    time.sleep(5)
                    st.rerun()
        except Exception as e:
            st.error(f"Terjadi error saat menyimpan ke MySQL: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if conn is not None:
                conn.close()
        
        st.info("Memuat ulang data dari database...")
        st.session_state["data"] = load_data_from_mysql()
        st.success("✅ Data dari database telah diperbarui.")

    
# ================================
# Halaman Visualisasi
# ================================
if nav == "📈 Visualisasi":
    st.title("📈 Visualisasi Data")
    
    # Sub-kategori visualisasi
    sub_menu = st.selectbox("Pilih Kategori", [
        "Analisis Faktor Risiko",
        "Statistik Pasien",
        "Hubungan Faktor Risiko & Pasien"
    ])

    # Opsi visualisasi berdasarkan kategori
    if sub_menu == "Analisis Faktor Risiko":
        pilihan = st.selectbox("Pilih Visualisasi", [
            "📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak",
            "🏠 Rumah Layak & Tidak Layak (Chart + Detail)",
            "🚰 Sanitasi Layak & Tidak Layak (Chart + Detail)",
            "🚩 Perilaku Baik & Tidak Sehat (Chart + Detail)"
        ])
        st.divider()  # **Menambahkan garis pemisah**
    
    elif sub_menu == "Statistik Pasien":
        pilihan = st.selectbox("Pilih Visualisasi", [
            "🩺 Jumlah Pasien per Puskesmas",
            "📅 Tren Date Start Pasien",
            "📊 Distribusi Usia",
            "🟢 Status Gizi dan Imunisasi",
            "🎯 Distribusi Pekerjaan"
        ])
        st.divider()  # **Menambahkan garis pemisah**
    
    elif sub_menu == "Hubungan Faktor Risiko & Pasien":
        pilihan = st.selectbox("Pilih Visualisasi", [
            "🏠 Tabel Crosstab Rumah Tidak Layak vs Pekerjaan",
            "🚰 Tabel Crosstab Sanitasi Tidak Layak vs Pekerjaan",
            "🚩 Tabel Crosstab Perilaku Tidak Baik vs Pekerjaan",
            "🦠 Jumlah Kasus TBC Berdasarkan Type TB",
            "🧮 Crosstab Kelurahan - Jumlah Kasus Tidak Layak"
        ])
        st.divider()  # **Menambahkan garis pemisah**

    st.subheader(f" {pilihan}")
    if st.session_state["data"].empty:
        st.warning("Data belum tersedia. Silakan upload file CSV atau input data manual di halaman Home.")
    else:
        # Buat salinan DataFrame untuk menghindari SettingWithCopyWarning
        df = st.session_state["data"].copy()
        
        # Pastikan kolom 'age' dikonversi ke numerik untuk menghindari Arrow conversion error
        if "age" in df.columns:
            df["age"] = pd.to_numeric(df["age"], errors="coerce")
        
        # Preprocessing dasar: imputasi, hapus duplikasi, konversi tanggal
        kolom_numerik = df.select_dtypes(include=['number']).columns
        kolom_kategori = df.select_dtypes(include=['object']).columns
        
        def fill_mode_or_mean(series):
            # Jika nama kolom adalah 'type_tb', biarkan tetap seperti itu
            if series.name == 'type_tb':
                return series

            # Jika kolom bertipe numerik, gunakan mean yang dibulatkan jika ada NaN
            if series.dtype in ['int64', 'float64']:
                return series.fillna(round(series.mean()))

            # Jika kolom bertipe kategori/objek, gunakan modus
            return series.fillna(series.mode()[0] if not series.mode().empty else series)

        # Terapkan fungsi ke semua kolom kategori
        df.loc[:, kolom_kategori] = df.loc[:, kolom_kategori].apply(fill_mode_or_mean)

        
        df = df.drop_duplicates()
        if "date_start" in df.columns:
            # Konversi kolom "date_start" ke datetime, kemudian format hanya tanggal (YYYY-MM-DD)
            df["date_start"] = pd.to_datetime(df["date_start"], errors="coerce").dt.strftime('%Y-%m-%d')
        
        
        # Definisi kategori untuk analisis skor
        kategori_rumah = [
            'langit_langit', 'lantai', 'dinding', 'jendela_kamar_tidur',
            'jendela_ruang_keluarga', 'ventilasi', 'lubang_asap_dapur', 'pencahayaan'
        ]
        kategori_sanitasi = [
            'sarana_air_bersih', 'jamban', 'sarana_pembuangan_air_limbah', 
            'sarana_pembuangan_sampah', 'sampah'
        ]
        kategori_perilaku = [
            'perilaku_merokok', 'anggota_keluarga_merokok', 'membuka_jendela_kamar_tidur',
            'membuka_jendela_ruang_keluarga', 'membersihkan_rumah', 'membuang_tinja',
            'membuang_sampah', 'kebiasaan_ctps'
        ]
        
        # Cek apakah kolom untuk analisis skor ada
        if all(col in df.columns for col in kategori_rumah + kategori_sanitasi + kategori_perilaku):
            df_rumah = df[kategori_rumah].dropna()
            df_sanitasi = df[kategori_sanitasi].dropna()
            df_perilaku = df[kategori_perilaku].dropna()

            def hitung_skor(df_sub, kategori, bobot):
                skor = []
                for _, row in df_sub.iterrows():
                    total_skor = 0
                    max_skor = 0
                    for kolom in kategori:
                        if kolom in bobot and row[kolom] in bobot[kolom]:
                            total_skor += bobot[kolom][row[kolom]]
                            max_skor += 5
                    skor.append((total_skor / max_skor) * 100 if max_skor else 0)
                df_sub["Skor Kelayakan"] = skor
                return df_sub

            bobot_rumah = {
                "langit_langit": {"Ada": 5, "Tidak ada": 1},
                "lantai": {"Ubin/keramik/marmer": 5, "Baik": 4, "Kurang Baik": 3, "Papan/Anyaman Bambu/Plester Retak": 2, "Tanah": 1},
                "dinding": {"Permanen (tembok pasangan batu bata yang diplester)": 5, "Semi permanen bata/batu yang tidak diplester/papan kayu": 3, "Bukan tembok (papan kayu/bambu/ilalang)": 1},
                "jendela_kamar_tidur": {"Ada": 5, "Tidak ada": 1},
                "jendela_ruang_keluarga": {"Ada": 5, "Tidak ada": 1},
                "ventilasi": {"Baik": 5, "Ada, luas ventilasi > 10% dari luas lantai": 4, "Ada, luas ventilasi < 10% dari luas lantai": 3, "Kurang Baik": 2, "Tidak Ada": 1},
                "lubang_asap_dapur": {"Ada, luas ventilasi > 10% luas lantai dapur/exhaust vent": 5, "Ada, luas ventilasi < 10% dari luas lantai dapur": 3, "Tidak Ada": 1},
                "pencahayaan": {"Terang/Dapat digunakan membaca normal": 5, "Baik": 4, "Kurang Baik": 3, "Kurang Terang": 2, "Tidak Terang/Kurang Jelas untuk membaca": 1}
            }
            bobot_sanitasi = {
                "sarana_air_bersih": {
                    "Ada,milik sendiri & memenuhi syarat kesehatan": 5,
                    "Ada,bukan milik sendiri & memenuhi syarat kesehatan": 4,
                    "Ada,milik sendiri & tidak memenuhi syarat kesehatan": 3,
                    "Ada, bukan milik sendiri & tidak memenuhi syarat kesehatan": 2,
                    "Tidak Ada": 1
                },
                "jamban": {
                    "Ada, leher angsa": 5,
                    "Ada tutup & septic tank": 4,
                    "Ada,bukan leher angsa ada tutup & septic tank": 3,
                    "Ada,bukan leher angsa ada tutup & dialirkan ke sungai": 2,
                    "Ada, bukan leher angsa tidak bertutup & dialirkan ke sungai": 2,
                    "Tidak Ada": 1
                },
                "sarana_pembuangan_air_limbah": {
                    'Ada, dialirkan ke selokan tertutup ("&"saluran kota) utk diolah lebih lanjut': 5,
                    "Ada, bukan milik sendiri & memenuhi syarat kesehatan": 4,
                    "Ada, diresapkan ke selokan terbuka": 3,
                    "Ada, diresapkan tetapi mencemari sumber air (jarak <10m)": 2,
                    "Tidak ada, sehingga tergenang dan tidak teratur di halaman/belakang rumah": 1
                },
                "sarana_pembuangan_sampah": {
                    "Ada, kedap air dan tertutup": 5,
                    "Ada, kedap air dan tidak tertutup": 4,
                    "Ada, tetapi tidak kedap air dan tidak tertutup": 3,
                    "Tidak Ada": 1
                },
                "sampah": {
                    "Petugas": 5,
                    "Dikelola Sendiri (Pilah Sampah)": 4,
                    "Bakar": 3,
                    "dll": 2,
                    "Lainnya (Sungai)": 1
                }
            }
            bobot_perilaku = {
                "perilaku_merokok": {"Tidak": 5, "Ya": 1},
                "anggota_keluarga_merokok": {"Tidak": 5, "Ya": 1},
                "membuka_jendela_kamar_tidur": {"Setiap hari dibuka": 5, "Kadang-kadang dibuka": 3, "Tidak pernah dibuka": 1},
                "membuka_jendela_ruang_keluarga": {"Setiap hari dibuka": 5, "Kadang-kadang dibuka": 3, "Tidak pernah dibuka": 1},
                "membersihkan_rumah": {"Setiap hari dibersihkan": 5, "Kadang-kadang": 3, "Tidak pernah dibersihkan": 1},
                "membuang_tinja": {"Setiap hari ke jamban": 5, "Dibuang ke sungai/kebun/kolam/sembarangan": 1},
                "membuang_sampah": {"Dibuang ke tempat sampah/ada petugas sampah": 5, 
                                    "Dilakukan pilah sampah/dikelola dengan baik": 4, 
                                    "Kadang-kadang dibuang ke tempat sampah": 3, 
                                    "Dibuang ke sungai/kebun/kolam/sembarangan / dibakar": 1},
                "kebiasaan_ctps": {"CTPS setiap aktivitas": 5, "Kadang-kadang CTPS": 3, "Tidak pernah CTPS": 1}
            }

            df_rumah = hitung_skor(df_rumah, kategori_rumah, bobot_rumah)
            df_sanitasi = hitung_skor(df_sanitasi, kategori_sanitasi, bobot_sanitasi)
            df_perilaku = hitung_skor(df_perilaku, kategori_perilaku, bobot_perilaku)

            threshold = 70
            def label_kelayakan(skor):
                return "Layak" if skor >= threshold else "Tidak Layak"

            df_rumah["Label"] = df_rumah["Skor Kelayakan"].apply(label_kelayakan)
            df_sanitasi["Label"] = df_sanitasi["Skor Kelayakan"].apply(label_kelayakan)
            df_perilaku["Label"] = df_perilaku["Skor Kelayakan"].apply(label_kelayakan)

            persentase_tidak_layak_rumah = (df_rumah[df_rumah["Label"] == "Tidak Layak"].shape[0] / df_rumah.shape[0]) * 100
            persentase_tidak_layak_sanitasi = (df_sanitasi[df_sanitasi["Label"] == "Tidak Layak"].shape[0] / df_sanitasi.shape[0]) * 100
            persentase_tidak_baik_perilaku = (df_perilaku[df_perilaku["Label"] == "Tidak Layak"].shape[0] / df_perilaku.shape[0]) * 100

            
            # Visualisasi berdasarkan pilihan
            if pilihan == "📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak":
            
                # Total data tiap kategori (misalnya, jumlah data yang masuk di masing-masing DataFrame)
                total_rumah = df_rumah.shape[0]
                total_sanitasi = df_sanitasi.shape[0]
                total_perilaku = df_perilaku.shape[0]

                count_rumah_tidak_layak = df_rumah[df_rumah["Label"] == "Tidak Layak"].shape[0]
                count_sanitasi_tidak_layak = df_sanitasi[df_sanitasi["Label"] == "Tidak Layak"].shape[0]
                count_perilaku_tidak_baik = df_perilaku[df_perilaku["Label"] == "Tidak Layak"].shape[0]

                # --- Membuat Grafik Bar ---
                # Daftar kategori, persentase, dan count
                kategori_overall = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
                persentase_overall = [persentase_tidak_layak_rumah, persentase_tidak_layak_sanitasi, persentase_tidak_baik_perilaku]
                counts_overall = [count_rumah_tidak_layak, count_sanitasi_tidak_layak, count_perilaku_tidak_baik]

                # Sorting berdasarkan persentase tertinggi (descending)
                sorted_idx = sorted(range(len(persentase_overall)), key=lambda i: persentase_overall[i], reverse=True)
                kategori_overall = [kategori_overall[i] for i in sorted_idx]
                persentase_overall = [persentase_overall[i] for i in sorted_idx]
                counts_overall = [counts_overall[i] for i in sorted_idx]

                # Buat grafik bar dengan Plotly Express
                import plotly.express as px
                fig = px.bar(
                    x=kategori_overall,
                    y=persentase_overall,
                    text=[f"{p:.2f}% ({c} rumah)" for p, c in zip(persentase_overall, counts_overall)],
                    labels={"x": "Kategori", "y": "Persentase (%)"},
                    title="Persentase dan Jumlah Rumah, Sanitasi, dan Perilaku Tidak Layak",
                    color=kategori_overall
                )

                fig.update_traces(texttemplate='%{text}', textposition='outside', cliponaxis=False)
                fig.update_layout(xaxis_tickangle=-45, margin=dict(t=80))
                # Tampilkan grafik pada Streamlit
                st.plotly_chart(fig, use_container_width=True)
                    
            elif pilihan == "🧮 Crosstab Kelurahan - Jumlah Kasus Tidak Layak":
                
                # Normalisasi nama kolom menjadi huruf kecil untuk konsistensi
                df.columns = df.columns.str.lower()
                df_rumah.columns = df_rumah.columns.str.lower()
                df_sanitasi.columns = df_sanitasi.columns.str.lower()
                df_perilaku.columns = df_perilaku.columns.str.lower()

                # Tambahkan kolom 'kelurahan' ke masing-masing dataframe sub berdasarkan index
                try:
                    df_rumah = df_rumah.copy()
                    df_sanitasi = df_sanitasi.copy()
                    df_perilaku = df_perilaku.copy()
                
                    df_rumah["kelurahan"] = df.loc[df_rumah.index, "kelurahan"].values
                    df_sanitasi["kelurahan"] = df.loc[df_sanitasi.index, "kelurahan"].values
                    df_perilaku["kelurahan"] = df.loc[df_perilaku.index, "kelurahan"].values
                except Exception as e:
                    st.error(f"Error saat menambahkan kolom kelurahan: {e}")

                # Pastikan nilai di kolom "label" sudah konsisten, misalnya dengan menghapus spasi dan mengubah ke huruf kecil
                df_rumah["label"] = df_rumah["label"].str.strip().str.lower()
                df_sanitasi["label"] = df_sanitasi["label"].str.strip().str.lower()
                df_perilaku["label"] = df_perilaku["label"].str.strip().str.lower()

                # Filter baris dengan label "tidak layak"
                df_rumah_ntl = df_rumah[df_rumah["label"] == "tidak layak"]
                df_sanitasi_ntl = df_sanitasi[df_sanitasi["label"] == "tidak layak"]
                df_perilaku_ntl = df_perilaku[df_perilaku["label"] == "tidak layak"]

                # Grouping berdasarkan 'kelurahan' untuk masing-masing kategori
                rumah_group = df_rumah_ntl.groupby("kelurahan").size().reset_index(name="Rumah Tidak Layak")
                sanitasi_group = df_sanitasi_ntl.groupby("kelurahan").size().reset_index(name="Sanitasi Tidak Layak")
                perilaku_group = df_perilaku_ntl.groupby("kelurahan").size().reset_index(name="Perilaku Tidak Baik")

                # Gabungkan hasil grouping berdasarkan kolom 'kelurahan'
                crosstab_kelurahan = (
                    rumah_group
                    .merge(sanitasi_group, on="kelurahan", how="outer")
                    .merge(perilaku_group, on="kelurahan", how="outer")
                )

                # Isi nilai NaN dengan 0 (jika ada kelurahan yang tidak muncul di salah satu kategori)
                crosstab_kelurahan.fillna(0, inplace=True)

                # Ubah tipe data kolom jumlah ke integer
                crosstab_kelurahan["Rumah Tidak Layak"] = crosstab_kelurahan["Rumah Tidak Layak"].astype(int)
                crosstab_kelurahan["Sanitasi Tidak Layak"] = crosstab_kelurahan["Sanitasi Tidak Layak"].astype(int)
                crosstab_kelurahan["Perilaku Tidak Baik"] = crosstab_kelurahan["Perilaku Tidak Baik"].astype(int)

                # Tambahkan kolom "Total" untuk memudahkan analisis
                crosstab_kelurahan["Total"] = (
                    crosstab_kelurahan["Rumah Tidak Layak"]
                    + crosstab_kelurahan["Sanitasi Tidak Layak"]
                    + crosstab_kelurahan["Perilaku Tidak Baik"]
                )

                # Urutkan berdasarkan Total (dari terbesar ke terkecil)
                crosstab_kelurahan = crosstab_kelurahan.sort_values(by="Total", ascending=False)

                # Tampilkan tabel crosstab
                df_display = crosstab_kelurahan.reset_index(drop=True)
                df_display = df_display[["kelurahan", "Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik", "Total"]]
                st.dataframe(df_display)
                             
                fig = px.bar(
                    crosstab_kelurahan,
                    x="kelurahan",
                    y="Total",
                    title="Total Kasus Tidak Layak per Kelurahan",
                    labels={"kelurahan": "Kelurahan", "Total": "Jumlah Kasus"},
                    text="Total",                       # Menampilkan nilai di atas batang
                    color="Total",                      # Pewarnaan batang berdasarkan nilai Total
                    color_continuous_scale="OrRd"       # Skema warna (merah-oranye)
                )

                # Mengatur posisi teks agar di luar batang
                fig.update_traces(textposition="outside", cliponaxis=False)

                # Mengatur tampilan layout
                fig.update_layout(
                    xaxis_tickangle=-45,               # Memiringkan label sumbu X agar terbaca
                    margin=dict(t=70, b=50),           # Menambahkan margin atas/bawah
                    coloraxis_showscale=True           # Menampilkan color scale di sisi grafik (opsional)
                )

                st.plotly_chart(fig, use_container_width=True)


            elif pilihan == "🦠 Jumlah Kasus TBC Berdasarkan Type TB":

                ## Konversi kolom type_tb ke string agar bisa menyimpan teks dan angka
                df["type_tb"] = df["type_tb"].astype(str)
                
                # Pastikan semua NaN diubah menjadi "None"
                df["type_tb"] = df["type_tb"].astype(str).fillna("None")

                # Pastikan semua nilai yang kosong benar-benar terisi
                df.loc[df["type_tb"].str.strip() == "", "type_tb"] = "None"
                df.loc[df["type_tb"].isin(["nan", "None"]), "type_tb"] = "None"
                tb_counts = df["type_tb"].value_counts(dropna=False).reset_index()
                tb_counts.columns = ["Type TB", "Jumlah"]
                
                # Ubah angka menjadi label teks yang lebih mudah dibaca
                tb_counts["Type TB"] = tb_counts["Type TB"].replace({"1.0": "TB SO", "2.0": "TB RO"})
                
                # **Pastikan "None" tetap ada dalam data**
                if "None" not in tb_counts["Type TB"].values:
                    tb_counts = pd.concat([tb_counts, pd.DataFrame([["None", 0]], columns=["Type TB", "Jumlah"])], ignore_index=True)
                
                # Sorting dari jumlah tertinggi
                tb_counts = tb_counts.sort_values(by="Jumlah", ascending=False)

                # **Cek apakah ada data setelah filtering**
                if tb_counts.empty:
                    st.warning("Tidak ada data Type TB yang tersedia.")
                else:
                    # Membuat grafik dengan Plotly
                    fig = px.bar(
                        tb_counts,
                        x="Type TB",
                        y="Jumlah",
                        text="Jumlah",
                        labels={"Type TB": "Tipe TB", "Jumlah": "Jumlah Kasus"},
                        title="Jumlah Kasus TBC Berdasarkan Type TB",
                        color="Type TB",
                        color_discrete_sequence=px.colors.qualitative.Set2  # Warna kategori
                    )

                    # Menampilkan teks di atas batang
                    fig.update_traces(texttemplate='%{text}', textposition='outside', cliponaxis=False)
                    fig.update_layout(xaxis_tickangle=-45, margin=dict(t=80))  # Tambah ruang atas

                    st.plotly_chart(fig, use_container_width=True)

            
            elif pilihan == "🏠 Tabel Crosstab Rumah Tidak Layak vs Pekerjaan":
        
                 # Ambil data 'pekerjaan' dari df untuk baris-baris yang terdapat di df_rumah (asumsi index cocok)
                df_rumah_with_pekerjaan = df.loc[df_rumah.index, ["pekerjaan"]].copy()
                
                # Tambahkan kolom indikator rumah (Label: Layak/Tidak Layak)
                df_rumah_with_pekerjaan["Rumah_Label"] = df_rumah["Label"].values

                # Buat tabel crosstab untuk menghitung frekuensi tiap kategori pekerjaan berdasarkan label rumah
                crosstab_counts = pd.crosstab(df_rumah_with_pekerjaan["pekerjaan"], df_rumah_with_pekerjaan["Rumah_Label"])

                # Hitung total tiap kategori pekerjaan dan persentase rumah "Tidak Layak"
                crosstab_counts["Total"] = crosstab_counts.sum(axis=1)
                if "Tidak Layak" in crosstab_counts.columns:
                    crosstab_counts["% Tidak Layak"] = (crosstab_counts["Tidak Layak"] / crosstab_counts["Total"]) * 100
                
                crosstab_counts = crosstab_counts.sort_values(by="Tidak Layak", ascending=False)
                
                # Tampilkan tabel Crosstab di Streamlit
                st.dataframe(crosstab_counts)

                # **Visualisasi dengan Plotly Express**
                if "Tidak Layak" in crosstab_counts.columns:
                    fig = px.bar(
                        crosstab_counts.reset_index(),
                        x="pekerjaan",
                        y="Tidak Layak",
                        title="Jumlah Rumah Tidak Layak per Pekerjaan",
                        labels={"pekerjaan": "Pekerjaan", "Tidak Layak": "Jumlah Rumah Tidak Layak"},
                        text="Tidak Layak",
                        color="Tidak Layak",
                        color_continuous_scale="Oranges"
                    )
                    # Perbaikan agar teks tidak terpotong
                    fig.update_traces(texttemplate='%{text}', textposition='outside', cliponaxis=False)
                    fig.update_layout(xaxis_tickangle=-45, margin=dict(t=80))  # Tambah ruang atas

                    st.plotly_chart(fig, use_container_width=True)
                    
            elif pilihan == "🚩 Tabel Crosstab Perilaku Tidak Baik vs Pekerjaan":

                # Ambil kolom "pekerjaan" dari df berdasarkan indeks df_perilaku
                df_perilaku_with_pekerjaan = df.loc[df_perilaku.index, ["pekerjaan"]].copy()

                # Pastikan label Perilaku menjadi "Baik" dan "Tidak Baik"
                df_perilaku_with_pekerjaan["Perilaku_Label"] = df_perilaku["Label"].replace({
                    "Layak": "Baik", 
                    "Tidak Layak": "Tidak Baik"
                })

                # Buat tabel crosstab
                crosstab_perilaku = pd.crosstab(
                    df_perilaku_with_pekerjaan["pekerjaan"],
                    df_perilaku_with_pekerjaan["Perilaku_Label"]
                )

                # Tambahkan kolom Total
                crosstab_perilaku["Total"] = crosstab_perilaku.sum(axis=1)

                # Pastikan ada kolom "Baik" dan "Tidak Baik" agar tidak error
                if "Baik" not in crosstab_perilaku.columns:
                    crosstab_perilaku["Baik"] = 0
                if "Tidak Baik" not in crosstab_perilaku.columns:
                    crosstab_perilaku["Tidak Baik"] = 0

                # Hitung persentase Perilaku Tidak Baik
                crosstab_perilaku["% Tidak Baik"] = (crosstab_perilaku["Tidak Baik"] / crosstab_perilaku["Total"]) * 100

                # **Tampilkan tabel di Streamlit (dengan Perilaku Baik tetap terlihat)**
                st.dataframe(crosstab_perilaku)
                # Urutkan data berdasarkan jumlah "Tidak Baik" dari terbesar ke terkecil
                crosstab_perilaku = crosstab_perilaku.sort_values(by="Tidak Baik", ascending=False)

                # **Visualisasi dengan Plotly (Hanya % Tidak Baik)**
                fig = px.bar(
                crosstab_perilaku.reset_index(),
                x="pekerjaan",
                y="Tidak Baik",
                title="Jumlah Perilaku Tidak Baik per Pekerjaan",
                labels={"pekerjaan": "Pekerjaan", "Tidak Baik": "Jumlah Perilaku Tidak Baik"},
                text="Tidak Baik",
                color="Tidak Baik",
                color_continuous_scale="Reds"
                )
                # Perbaikan agar teks tidak terpotong
                fig.update_traces(texttemplate='%{text}', textposition='outside', cliponaxis=False)
                fig.update_layout(xaxis_tickangle=-45, margin=dict(t=80))  # Tambah ruang atas

                st.plotly_chart(fig, use_container_width=True)


                                
            elif pilihan == "🚰 Tabel Crosstab Sanitasi Tidak Layak vs Pekerjaan":

                # Ambil kolom "pekerjaan" dari df berdasarkan indeks df_sanitasi
                df_sanitasi_with_pekerjaan = df.loc[df_sanitasi.index, ["pekerjaan"]].copy()
                
                # Tambahkan kolom "Sanitasi_Label" (Layak/Tidak Layak) dari df_sanitasi
                df_sanitasi_with_pekerjaan["Sanitasi_Label"] = df_sanitasi["Label"].values

                # Buat crosstab
                crosstab_sanitasi = pd.crosstab(
                    df_sanitasi_with_pekerjaan["pekerjaan"],
                    df_sanitasi_with_pekerjaan["Sanitasi_Label"]
                )

                # Tambahkan kolom Total dan persentase "Tidak Layak"
                crosstab_sanitasi["Total"] = crosstab_sanitasi.sum(axis=1)
                if "Tidak Layak" in crosstab_sanitasi.columns:
                    crosstab_sanitasi = crosstab_sanitasi.sort_values(by="Tidak Layak", ascending=False)

                    fig = px.bar(
                        crosstab_sanitasi.reset_index(),
                        x="pekerjaan",
                        y="Tidak Layak",
                        title="Jumlah Sanitasi Tidak Layak per Pekerjaan",
                        labels={"pekerjaan": "Pekerjaan", "Tidak Layak": "Jumlah Sanitasi Tidak Layak"},
                        text="Tidak Layak",
                        color="Tidak Layak",
                        color_continuous_scale="Blues"
                    )

                    # Perbaikan agar teks tidak terpotong
                    fig.update_traces(texttemplate='%{text}', textposition='outside', cliponaxis=False)
                    fig.update_layout(xaxis_tickangle=-45, margin=dict(t=80))  # Tambah ruang atas

                    st.plotly_chart(fig, use_container_width=True)
                        
                
            elif pilihan == "🏠 Rumah Layak & Tidak Layak (Chart + Detail)":
                
                # --- Pie Chart Rumah Layak vs Tidak Layak ---
                # Pastikan variabel persentase_tidak_layak_rumah sudah didefinisikan sebelumnya
                labels = ["Layak", "Tidak Layak"]
                sizes = [100 - persentase_tidak_layak_rumah, persentase_tidak_layak_rumah]
                # Warna khusus untuk masing-masing kategori
                color_map = {"Layak": "#4CAF50", "Tidak Layak": "#E74C3C"}
                # Untuk memberikan efek 'explode' pada slice "Tidak Layak"
                pull = [0, 0.1]
                
                fig_pie = px.pie(
                    names=labels,
                    values=sizes,
                    color=labels,
                    color_discrete_map=color_map,
                    title="Persentase Rumah Layak dan Tidak Layak"
                )
                fig_pie.update_traces(textinfo="percent+label", pull=pull)
                
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # --- Detail: Bar Chart Kategori Rumah Tidak Layak ---
                st.markdown("#### Detail Kategori Rumah Tidak Layak")
                total_rumah = len(df)
                
                # Hitung jumlah rumah per sub kategori dari kolom terkait
                kategori_rumah_detail = {
                    "Luas ventilasi ≤ 10% dari luas lantai": df['ventilasi'].str.contains('luas ventilasi < 10%', case=False, na=False).sum(),
                    "Pencahayaan kurang terang, kurang jelas untuk membaca normal": df['pencahayaan'].str.contains('kurang terang', case=False, na=False).sum(),
                    "Lubang asap dapur dengan luas ventilasi < 10% dari luas lantai dapur": df['lubang_asap_dapur'].str.contains('luas ventilasi < 10%', case=False, na=False).sum(),
                    "Tidak Ada Jendela di Rumah": df['ventilasi'].str.contains('tidak ada', case=False, na=False).sum(),
                    "Tidak Ada Langit-Langit": df['langit_langit'].str.contains('tidak ada', case=False, na=False).sum(),
                    "Lantai Papan/anyaman bambu/plester retak berdebu": df['lantai'].str.contains('papan|anyaman bambu|plester retak', case=False, na=False).sum(),
                    "Tidak ada lubang asap dapur": df['lubang_asap_dapur'].str.contains('tidak ada', case=False, na=False).sum(),
                    "Lantai Tanah": df['lantai'].str.contains('tanah', case=False, na=False).sum(),
                }
                kategori_rumah_detail = {k: v for k, v in kategori_rumah_detail.items() if v > 0}
                df_detail = pd.DataFrame(list(kategori_rumah_detail.items()), columns=['Kategori', 'Jumlah'])
                df_detail['Persentase'] = (df_detail['Jumlah'] / total_rumah) * 100
                df_detail = df_detail.sort_values(by='Jumlah', ascending=False)
            
                df_detail["Teks"] = df_detail["Persentase"].apply(lambda x: f"{x:.1f}%")
                # Buat bar chart horizontal dengan sumbu x = Persentase
                # Buat bar chart horizontal dengan sumbu x = Persentase
                fig_bar = px.bar(
                    df_detail,
                    x="Persentase",                  # gunakan kolom persentase untuk sumbu X
                    y="Kategori",
                    orientation="h",
                    text="Teks",                     # hanya menampilkan persentase di batang
                    title="Kategori Rumah Tidak Layak (Berbasis Persentase)",
                    labels={
                        "Persentase": "Persentase (%)", 
                        "Kategori": "Kategori Rumah Tidak Layak"
                    },
                    color="Persentase",              # gunakan persentase untuk pewarnaan
                    color_continuous_scale="Viridis",
                    # Menampilkan Jumlah di tooltip saat kursor diarahkan
                    hover_data={
                        "Jumlah": True,          # Tampilkan jumlah
                        "Persentase": ":.1f"     # Format persentase 1 desimal
                    }
                )

                # Tampilkan teks di luar batang
                fig_bar.update_traces(textposition="outside")

                # Pengaturan layout
                fig_bar.update_layout(
                    yaxis=dict(categoryorder="total ascending"),
                    margin=dict(l=200, r=50, t=50, b=50),
                    autosize=False,
                    width=900,
                    height=600
                )

                # Jika ingin sembunyikan color scale, gunakan:
                # fig_bar.update_layout(coloraxis_showscale=False)

                st.plotly_chart(fig_bar, use_container_width=True)

            elif pilihan == "🚰 Sanitasi Layak & Tidak Layak (Chart + Detail)":
                
                # --- Pie Chart Sanitasi Layak vs Tidak Layak ---
                persentase_layak_sanitasi = 100 - persentase_tidak_layak_sanitasi  # pastikan variabel ini sudah didefinisikan
                labels_sanitasi = ["Layak", "Tidak Layak"]
                sizes_sanitasi = [persentase_layak_sanitasi, persentase_tidak_layak_sanitasi]
                
                # Buat pie chart dengan Plotly Express
                fig_pie = px.pie(
                    names=labels_sanitasi,
                    values=sizes_sanitasi,
                    color=labels_sanitasi,
                    color_discrete_map={"Layak": "#3498DB", "Tidak Layak": "#E74C3C"},
                    title="Persentase Sanitasi Layak dan Tidak Layak"
                )
                # Mengatur agar slice "Tidak Layak" terlihat 'meledak'
                fig_pie.update_traces(textinfo="percent+label", pull=[0, 0.1])
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # --- Detail: Bar Chart Detail Kategori Sanitasi Tidak Layak ---
                st.markdown("#### Detail Kategori Sanitasi Tidak Layak")
                total_rumah = len(df)
                
                # Hitung jumlah rumah per kategori dari kolom terkait
                kategori_sanitasi_detail = {
                    "Jamban bukan leher angsa, tidak bertutup & dialirkan ke sungai": df['jamban'].apply(lambda x: 'tidak bertutup' in str(x).lower() and 'sungai' in str(x).lower()).sum(),
                    "Sarana air bersih bukan milik sendiri & tidak memenuhi syarat kesehatan": df['sarana_air_bersih'].apply(lambda x: 'bukan milik sendiri' in str(x).lower() and 'tidak memenuhi' in str(x).lower()).sum(),
                    "Tidak ada Sarana Air Bersih": df['sarana_air_bersih'].apply(lambda x: 'tidak ada' in str(x).lower()).sum(),
                    "SPAL diresapkan tetapi mencemari sumber air (jarak <10m)": df['sarana_pembuangan_air_limbah'].apply(lambda x: 'diresapkan' in str(x).lower() and 'mencemari' in str(x).lower()).sum(),
                    "Tidak ada jamban": df['jamban'].apply(lambda x: 'tidak ada' in str(x).lower()).sum(),
                    "Jamban bukan leher angsa, ada tutup & dialirkan ke sungai": df['jamban'].apply(lambda x: 'bukan leher angsa' in str(x).lower() and 'tutup' in str(x).lower() and 'sungai' in str(x).lower()).sum(),
                    "Tidak ada Sarana Pembuangan Sampah": df['sarana_pembuangan_sampah'].apply(lambda x: 'tidak ada' in str(x).lower()).sum(),
                    "Tidak ada SPAL": df['sarana_pembuangan_air_limbah'].apply(lambda x: 'tidak ada' in str(x).lower()).sum(),
                    "Sarana air bersih milik sendiri & tidak memenuhi syarat kesehatan": df['sarana_air_bersih'].apply(lambda x: 'milik sendiri' in str(x).lower() and 'tidak memenuhi' in str(x).lower()).sum(),
                    "Jamban bukan leher angsa, ada tutup & septic tank": df['jamban'].apply(lambda x: 'bukan leher angsa' in str(x).lower() and 'tutup' in str(x).lower() and 'septic tank' in str(x).lower()).sum(),
                    "Sarana Pembuangan Sampah tidak kedap air dan tidak tertutup": df['sarana_pembuangan_sampah'].apply(lambda x: 'tidak kedap' in str(x).lower() and 'tidak tertutup' in str(x).lower()).sum(),
                    "SPAL bukan milik sendiri & memenuhi syarat kesehatan": df['sarana_pembuangan_air_limbah'].apply(lambda x: 'bukan milik sendiri' in str(x).lower() and 'memenuhi' in str(x).lower()).sum(),
                    "SPAL diresapkan ke selokan terbuka": df['sarana_pembuangan_air_limbah'].apply(lambda x: 'diresapkan' in str(x).lower() and 'selokan terbuka' in str(x).lower()).sum(),
                    "Sarana air bersih bukan milik sendiri & memenuhi syarat kesehatan": df['sarana_air_bersih'].apply(lambda x: 'bukan milik sendiri' in str(x).lower() and 'memenuhi' in str(x).lower()).sum(),
                    "Sarana Pembuangan Sampah kedap air dan tidak tertutup": df['sarana_pembuangan_sampah'].apply(lambda x: 'kedap air' in str(x).lower() and 'tidak tertutup' in str(x).lower()).sum()
                }
                # Hapus kategori dengan nilai 0
                kategori_sanitasi_detail = {k: v for k, v in kategori_sanitasi_detail.items() if v > 0}
                df_sanitasi_detail = pd.DataFrame(list(kategori_sanitasi_detail.items()), columns=['Kategori', 'Jumlah'])
                df_sanitasi_detail['Persentase'] = (df_sanitasi_detail['Jumlah'] / total_rumah) * 100
                df_sanitasi_detail = df_sanitasi_detail.sort_values(by='Jumlah', ascending=False)
                
                height_chart = max(700, len(df_sanitasi_detail) * 30)
                
                # Buat bar chart dengan Plotly Express (horizontal)
                fig_bar_sanitasi = px.bar(
                    df_sanitasi_detail,
                    x="Persentase",               # sumbu X menampilkan nilai persentase
                    y="Kategori",
                    orientation="h",
                    text=df_sanitasi_detail["Persentase"].apply(lambda x: f"{x:.1f}%"),
                    title="Kategori Sanitasi Tidak Layak",
                    labels={"Persentase": "Persentase (%)", "Kategori": "Kategori Sanitasi Tidak Layak"},
                    color="Persentase",
                    color_continuous_scale="Cividis",
                    hover_data={
                        "Jumlah": True,           # tampilkan jumlah di tooltip
                        "Persentase": ":.1f"       # tampilkan persentase dengan 1 desimal
                    }
                )
                
                fig_bar_sanitasi.update_traces(textposition="outside")
                fig_bar_sanitasi.update_layout(
                    yaxis=dict(categoryorder="total ascending"),
                    margin=dict(l=300, r=50, t=50, b=50),
                    autosize=False,
                    width=1400,
                    height=height_chart
    )
                st.plotly_chart(fig_bar_sanitasi, use_container_width=True)

            
            elif pilihan == "🚩 Perilaku Baik & Tidak Sehat (Chart + Detail)":
                
                # --- Pie Chart Perilaku Baik vs Tidak Baik ---
                # Pastikan variabel persentase_tidak_baik_perilaku sudah didefinisikan
                persentase_baik_perilaku = 100 - persentase_tidak_baik_perilaku  
                labels_perilaku = ["Baik", "Tidak Baik"]
                sizes_perilaku = [persentase_baik_perilaku, persentase_tidak_baik_perilaku]
                colors_perilaku = {'Baik': '#1F77B4', 'Tidak Baik': '#FF7F0E'}
                pull_perilaku = [0, 0.1]  # slice "Tidak Baik" di-'explode'
                
                fig_pie = px.pie(
                    names=labels_perilaku,
                    values=sizes_perilaku,
                    color=labels_perilaku,
                    color_discrete_map=colors_perilaku,
                    title="Persentase Perilaku Baik dan Tidak Baik"
                )
                fig_pie.update_traces(textinfo="percent+label", pull=pull_perilaku)
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # --- Detail: Bar Chart Kategori Perilaku Tidak Sehat ---
                st.markdown("#### Detail Kategori Perilaku Tidak Sehat")
                total_rumah = len(df)
                
                # Hitung jumlah rumah untuk setiap kategori perilaku tidak sehat
                kategori_perilaku_detail = {
                    "BAB di sungai / kebun / kolam / sembarangan": df['membuang_tinja'].apply(lambda x: any(word in str(x).lower() for word in ['sungai', 'kebun', 'kolam', 'sembarangan'])).sum(),
                    "Tidak CTPS": df['kebiasaan_ctps'].apply(lambda x: 'tidak' in str(x).lower()).sum(),
                    "Tidak pernah membersihkan rumah dan halaman": df['membersihkan_rumah'].apply(lambda x: 'tidak pernah' in str(x).lower()).sum(),
                    "Buang sampah ke sungai / kebun / kolam / sembarangan / dibakar": df['membuang_sampah'].apply(lambda x: any(word in str(x).lower() for word in ['sungai', 'kebun', 'kolam', 'sembarangan', 'dibakar'])).sum(),
                    "Tidak pernah buka jendela ruang keluarga": df['membuka_jendela_ruang_keluarga'].apply(lambda x: 'tidak pernah' in str(x).lower()).sum(),
                    "Tidak pernah buka jendela kamar tidur": df['membuka_jendela_kamar_tidur'].apply(lambda x: 'tidak pernah' in str(x).lower()).sum(),
                }
                # Hapus kategori dengan nilai 0
                kategori_perilaku_detail = {k: v for k, v in kategori_perilaku_detail.items() if v > 0}
                df_perilaku_detail = pd.DataFrame(list(kategori_perilaku_detail.items()), columns=['Kategori', 'Jumlah'])
                df_perilaku_detail['Persentase'] = (df_perilaku_detail['Jumlah'] / total_rumah) * 100
                df_perilaku_detail = df_perilaku_detail.sort_values(by='Jumlah', ascending=False)
                
                # Buat kolom label untuk teks pada batang
                df_perilaku_detail['Label'] = df_perilaku_detail.apply(
                    lambda row: f"{row['Jumlah']} ({row['Persentase']:.1f}%)", axis=1
                )
                
                # Buat kolom teks yang hanya menampilkan persentase pada batang
                df_perilaku_detail["Teks"] = df_perilaku_detail["Persentase"].apply(lambda x: f"{x:.1f}%")
                
                # Buat bar chart horizontal dengan sumbu X = Persentase
                fig_bar = px.bar(
                    df_perilaku_detail,
                    x="Persentase",
                    y="Kategori",
                    orientation="h",
                    text="Teks",  # hanya menampilkan persentase pada batang
                    title="Kategori Perilaku Tidak Sehat",
                    labels={"Persentase": "Persentase (%)", "Kategori": "Kategori Perilaku Tidak Sehat"},
                    color="Persentase",
                    color_continuous_scale="Blues",
                    hover_data={
                        "Jumlah": True,         # Tampilkan jumlah di tooltip
                        "Persentase": ":.1f"     # Format persentase di tooltip
                    }
                )
                
                fig_bar.update_traces(textposition="outside", textfont=dict(size=11))
                fig_bar.update_layout(
                    yaxis=dict(categoryorder="total ascending"),
                    margin=dict(l=200, r=50, t=50, b=50),
                    autosize=False,
                    width=900,
                    height= max(600, len(df_perilaku_detail)*30)
                )
                st.plotly_chart(fig_bar, use_container_width=True)
    
            elif pilihan == "🩺 Jumlah Pasien per Puskesmas":
                
                # Hitung jumlah pasien berdasarkan puskesmas
                puskesmas_counts = df.groupby("puskesmas")["pasien"].count().reset_index()
                puskesmas_counts.columns = ["puskesmas", "jumlah_pasien"]
            
                # Hitung persentase
                total_pasien = puskesmas_counts["jumlah_pasien"].sum()
                puskesmas_counts["persentase"] = (puskesmas_counts["jumlah_pasien"] / total_pasien) * 100
            
                # Urutkan dari terbanyak
                puskesmas_counts = puskesmas_counts.sort_values(by="jumlah_pasien", ascending=False)
                
                # Buat plot horizontal dengan Plotly Express
                fig = px.bar(
                    puskesmas_counts,
                    x="jumlah_pasien",
                    y="puskesmas",
                    orientation="h",
                    text=puskesmas_counts.apply(
                        lambda row: f"{row['jumlah_pasien']} ({row['persentase']:.1f}%)", axis=1
                    ),
                    labels={"jumlah_pasien": "Jumlah Pasien", "puskesmas": "Puskesmas"},
                    title="Jumlah Pasien per Puskesmas",
                    color="jumlah_pasien",
                    color_continuous_scale="magma"
                )
                fig.update_traces(textposition="outside")
                fig.update_layout(yaxis=dict(categoryorder="total ascending"))
                
                # Tampilkan grafik Plotly (toolbar interaktif sudah otomatis termasuk opsi download)
                st.plotly_chart(fig, use_container_width=True)
            
            elif pilihan == "📅 Tren Date Start Pasien":
                # **Cek apakah data tersedia**
                # **Load Data dari MySQL**          
                df = load_data_from_mysql()
                if df.empty:
                    st.warning("⚠️ Data tidak ditemukan dalam database.")
                else:
                    # **Konversi date_start ke datetime**
                    df = df.copy()  # Buat salinan agar aman
                    # Pastikan 'df' sudah ada dan kolom 'date_start' dalam format datetime
                    # **Pastikan date_start dalam format datetime**
                    df["date_start"] = pd.to_datetime(df["date_start"], errors="coerce")

                    # **Ambil semua bulan dengan format 'M'**
                    df["Bulan"] = df["date_start"].dt.to_period("M").astype(str)
                    all_months = sorted(df["Bulan"].unique())  # Urutkan bulan

                    # **Widget pemilihan bulan**
                    start_month = st.selectbox("Pilih bulan awal", all_months, index=0)
                    end_month = st.selectbox("Pilih bulan akhir", all_months, index=len(all_months)-1)

                    # **Buat rentang bulan lengkap**
                    date_range = pd.period_range(start=start_month, end=end_month, freq="M").strftime("%Y-%m").tolist()

                    # **Filter dataset sesuai pilihan**
                    df_filtered = df.loc[(df["Bulan"] >= start_month) & (df["Bulan"] <= end_month)].copy()

                    # **Hitung jumlah pasien per bulan**
                    date_counts = df_filtered.groupby("Bulan", as_index=False, observed=False)["pasien"].count()
                    date_counts.columns = ["Bulan", "Jumlah Pasien"]

                    # **Gabungkan dengan daftar lengkap bulan yang dipilih**
                    date_counts = pd.DataFrame({"Bulan": date_range}).merge(date_counts, on="Bulan", how="left").fillna(0)

                    # **Format sumbu X agar rapi**
                    date_counts["Bulan"] = pd.to_datetime(date_counts["Bulan"], format="%Y-%m")
                    date_counts = date_counts.sort_values("Bulan")
                    date_counts["Bulan"] = date_counts["Bulan"].dt.strftime("%b %Y")  # Format 'Mar 2025'

                    # **Buat grafik**
                    fig = px.line(
                        date_counts,
                        x="Bulan",
                        y="Jumlah Pasien",
                        markers=True,
                        labels={"Bulan": "Bulan", "Jumlah Pasien": "Jumlah Pasien"},
                        title="📈 Tren Pasien Per Bulan",
                        color_discrete_sequence=["#2CA02C"]
                    )

                    # **Pastikan semua bulan muncul di sumbu X**
                    fig.update_xaxes(type="category", tickmode="array", tickvals=date_counts["Bulan"])

                    st.plotly_chart(fig, use_container_width=True)
                    
            elif pilihan == "📊 Distribusi Usia":
            
                # Pastikan kolom "age" ada dan bersifat numerik
                if "age" not in df.columns:
                    st.warning("Kolom 'age' tidak ditemukan di data.")
                else:
                    df["age"] = pd.to_numeric(df["age"], errors="coerce")
                    usia = df["age"].dropna()
                    if usia.empty:
                        st.warning("Data usia kosong.")
                    else:
                        # Definisikan rentang usia (bins) dan labelnya
                        bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 100]
                        labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins)-1)]
                        df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)
            
                        # Grouping berdasarkan age_group dan gender
                        age_gender = df.groupby(["age_group", "gender"], observed=False).size().reset_index(name="count")
            
                        # Plot menggunakan Plotly
                        fig = px.bar(
                            age_gender,
                            x="age_group",
                            y="count",
                            color="gender",
                            barmode="group",
                            labels={"age_group": "Rentang Usia", "count": "Jumlah", "gender": "Jenis Kelamin"},
                            title="Distribusi Usia per Gender"
                        )

                        fig.update_traces(textposition="outside")
                        fig.update_layout(yaxis=dict(categoryorder="total ascending"))
                
                        # Tampilkan grafik Plotly (toolbar interaktif sudah otomatis termasuk opsi download)
                        st.plotly_chart(fig, use_container_width=True)
                        
            elif pilihan == "🟢 Status Gizi dan Imunisasi":
            
                # 🔹 Pastikan kolom tersedia
                if "status_imunisasi" not in df.columns:
                    st.warning("Kolom 'status_imunisasi' tidak ditemukan di data.")
                elif "status_gizi" not in df.columns:
                    st.warning("Kolom 'status_gizi' tidak ditemukan di data.")
                else:
                    # 🔹 Definisikan kategori yang valid
                    valid_status_gizi = ['Underweight', 'Normal', 'Wasting', 'Kurang', 'Overweight', 'Obesitas']

                    # 🔹 Filter data hanya untuk kategori yang valid
                    df_filtered = df[df["status_gizi"].isin(valid_status_gizi)]

                    # 🔹 Cek apakah data kosong setelah filter
                    if df_filtered.empty:
                        st.warning("Data tidak tersedia untuk status gizi dan imunisasi.")
                    else:
                        # 🔹 Grouping data setelah filtering
                        imunisasi_gizi = df_filtered.groupby(["status_gizi", "status_imunisasi"], observed=False).size().reset_index(name="count")


                        # 🔹 Membuat grafik dengan Plotly
                        fig = px.bar(
                            imunisasi_gizi,
                            x="status_gizi",
                            y="count",
                            color="status_imunisasi",
                            barmode="group",
                            labels={"count": "Jumlah", "status_gizi": "Status Gizi", "status_imunisasi": "Status Imunisasi"},
                            title="Distribusi Status Gizi berdasarkan Status Imunisasi"
                        )

                        # 🔹 Menampilkan grafik di Streamlit
                        fig.update_traces(textposition="outside")
                        fig.update_layout(yaxis=dict(categoryorder="total ascending"))
                
                        # Tampilkan grafik Plotly (toolbar interaktif sudah otomatis termasuk opsi download)
                        st.plotly_chart(fig, use_container_width=True)
                        
            elif pilihan == "🎯 Distribusi Pekerjaan":
                
                # Grup data berdasarkan kolom 'pekerjaan'
                data = df.groupby("pekerjaan")["pasien"].count().reset_index()
                data.columns = ["pekerjaan", "jumlah_pasien"]
                
                # Hitung persentase
                total_pasien = data["jumlah_pasien"].sum()
                data["persentase"] = (data["jumlah_pasien"] / total_pasien) * 100
                
                # Urutkan berdasarkan jumlah pasien terbanyak
                data = data.sort_values(by="jumlah_pasien", ascending=False)
                
                # Buat label untuk setiap bar
                data["label"] = data.apply(lambda row: f"{row['jumlah_pasien']} ({row['persentase']:.1f}%)", axis=1)
                
                # Buat grafik bar horizontal dengan Plotly Express
                fig = px.bar(
                    data,
                    x="jumlah_pasien",
                    y="pekerjaan",
                    orientation="h",
                    text="label",
                    color="jumlah_pasien",
                    color_continuous_scale="viridis",
                    title="🎯 Distribusi Pekerjaan"
                )
                fig.update_traces(textposition="outside")
                fig.update_layout(
                    xaxis_title="Jumlah Pasien",
                    yaxis_title="Pekerjaan",
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                        

            
            st.sidebar.success("Visualisasi selesai ditampilkan!")
            
