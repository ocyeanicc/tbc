import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from io import BytesIO
import plotly.express as px
import plotly.io as pio  
from PIL import Image
import io

# 2) Atur tema Seaborn
sns.set_theme(style="whitegrid")

# 2) Inisialisasi session_state untuk menyimpan data CSV, data manual, dan data gabungan
if "csv_data" not in st.session_state:
    st.session_state["csv_data"] = pd.DataFrame()

if "manual_data" not in st.session_state:
    st.session_state["manual_data"] = pd.DataFrame()

if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame()  # Inisialisasi dengan DataFrame kosong
else:
    st.session_state["data"] = st.session_state["data"].sort_index()


# 3) Fungsi untuk menampilkan label kolom tanpa underscore
def display_label(col_name: str) -> str:
    return " ".join(word.capitalize() for word in col_name.split("_"))

# 5) Tampilkan elemen di sidebar
logo_url = "https://raw.githubusercontent.com/lizyyaaa/tbc/main/dashboard/download%20(1).png" 
st.sidebar.image(logo_url, use_container_width=True)

# Title dan Subheader di sidebar
st.sidebar.title("🏥 Dinas Kesehatan Kota Semarang")
st.sidebar.subheader("Bidang P2P")
st.sidebar.markdown("---")

# Contoh info box untuk menambah keterangan di sidebar
st.sidebar.info("Silakan pilih halaman di bawah ini.")

# 6) Navigasi menggunakan radio button di sidebar dengan emoji
nav = st.sidebar.radio(
     "🔽 Pilih Halaman", 
    ["🏠 Home", "📈 Visualisasi"]
)

def download_chart(fig):
    # Simpan gambar sebagai PNG langsung dari Plotly
    buffer = fig.to_image(format="png", engine="kaleido")

    # Buat stream buffer dari bytes
    image_stream = io.BytesIO(buffer)

    # Tombol download
    st.download_button(
        label="⬇️ Download Gambar",
        data=image_stream,
        file_name="chart.png",
        mime="image/png",
        key=f"download_chart_{datetime.now().timestamp()}"
    )

    # Tombol download
    st.download_button(
        label="⬇️ Download Gambar",
        data=png_buffer,
        file_name="chart.png",
        mime="image/png",
        key=f"download_chart_{datetime.now().timestamp()}"
    )

# Fungsi untuk menampilkan chart dan download
def tampilkan_dan_download(fig):
    st.plotly_chart(fig)  # Tampilkan grafik Plotly
    download_chart(fig)   # Tambahkan tombol download
    
# ================================
# Halaman Home: Input & Upload Data
# ================================
if nav == "🏠 Home":
    st.title("🏠 Home - Input & Upload Data")
    st.markdown("### Upload file CSV dan masukkan data baru secara manual. Data yang diinput akan digabungkan dan ditampilkan.")
    
     # --- Bagian Upload CSV ---
    uploaded_file = st.file_uploader("📂 Upload file CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            # Membaca CSV dengan separator ';'
            df_csv = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
            st.success("File CSV berhasil diupload!")
            # Update session_state csv_data dan gabungkan dengan manual_data
            st.session_state["csv_data"] = df_csv.copy()
            st.session_state["data"] = pd.concat([st.session_state["csv_data"], st.session_state["manual_data"]], ignore_index=True)
            st.info("Data CSV telah disimpan dan digabungkan dengan data manual yang ada.")
        except Exception as e:
            st.error(f"Error membaca file: {e}")
   

    # Urutan field yang diinginkan
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
    
    # Option dictionary untuk field yang memiliki pilihan
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
        "type_tb": [1.0, 2.0],
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
    
    st.markdown("## Form Input Data Manual Tambahan")
    with st.form(key="manual_form"):
        input_manual = {}
        for col in fields_order:
            label = col.replace("_", " ").title()  # Ganti dengan fungsi display_label jika ada
            
            # Kolom dengan tipe khusus
            if col == "pasien":
                input_manual[col] = st.text_input(label, value="")
            elif col == "age":
                input_manual[col] = st.number_input(label, min_value=0, step=1, value=0)
            elif col in ["date_start", "tgl_kunjungan"]:
                input_manual[col] = st.date_input(label, value=datetime.today())
            # Kolom yang memiliki opsi di option_dict
            elif col in option_dict:
                options = option_dict[col]
                if options:
                    input_manual[col] = st.selectbox(label, options)
                else:
                    input_manual[col] = st.text_input(label, value="")
            else:
                # Kolom lainnya default ke text_input
                input_manual[col] = st.text_input(label, value="")
        
        submitted_manual = st.form_submit_button("Submit Data Manual Tambahan")
    
    if submitted_manual:
        # Ubah nilai date_input menjadi pd.Timestamp, lalu format menjadi string "YYYY-MM-DD"
        df_manual = pd.DataFrame([input_manual])
        df_manual["date_start"] = pd.to_datetime(df_manual["date_start"]).dt.strftime('%Y-%m-%d')
        df_manual["tgl_kunjungan"] = pd.to_datetime(df_manual["tgl_kunjungan"]).dt.strftime('%Y-%m-%d')

        
        df_manual = pd.DataFrame([input_manual])
        st.success("Data manual tambahan berhasil ditambahkan!")
        st.dataframe(df_manual)
        
        # Update session_state manual_data dengan menambahkan data baru
        st.session_state["manual_data"] = pd.concat([st.session_state["manual_data"], df_manual], ignore_index=True)
        # Gabungkan data CSV dan data manual menjadi data gabungan
        st.session_state["data"] = pd.concat([st.session_state["csv_data"], st.session_state["manual_data"]], ignore_index=True)
        st.info("Data gabungan telah disimpan. Buka halaman Visualisasi untuk melihat chart.")
    
    # Tampilkan data gabungan jika sudah ada
    if not st.session_state["data"].empty:
        st.markdown("### Data Gabungan Saat Ini")
        st.dataframe(st.session_state["data"])


# ================================
# Halaman Visualisasi
# ================================
elif nav == "📈 Visualisasi":
    st.title("📈 Visualisasi Data")
    if st.session_state["data"].empty:
        st.warning("Data belum tersedia. Silakan upload file CSV atau input data manual di halaman Home.")
    else:
        df = st.session_state["data"]
        st.subheader("Data yang Digunakan")
        st.dataframe(df)
        
        # Preprocessing dasar: imputasi, hapus duplikasi, konversi tanggal
        kolom_numerik = df.select_dtypes(include=['number']).columns
        kolom_kategori = df.select_dtypes(include=['object']).columns
        df[kolom_kategori] = df[kolom_kategori].apply(lambda x: x.fillna(x.mode()[0]))
        df[kolom_numerik] = df[kolom_numerik].apply(lambda x: x.fillna(x.mean()))
        df = df.drop_duplicates()
        if "date_start" in df.columns:
            df["date_start"] = pd.to_datetime(df["date_start"], errors="coerce")
            df["year_month"] = df["date_start"].dt.to_period("M").astype(str)
        
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

            st.markdown(
                f"""
                **Persentase Rumah Tidak Layak**: {persentase_tidak_layak_rumah:.2f}%  
                **Persentase Sanitasi Tidak Layak**: {persentase_tidak_layak_sanitasi:.2f}%  
                **Persentase Perilaku Tidak Baik**: {persentase_tidak_baik_perilaku:.2f}%  
                """
            )

            # Mendefinisikan opsi visualisasi baru
            visualisasi_list = [
                "📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak",
                "📈 Kebiasaan CTPS",
                "🐑 Memiliki Hewan Ternak",
                "🏠 Rumah Layak & Tidak Layak (Chart + Detail)",
                "🚰 Sanitasi Layak & Tidak Layak (Chart + Detail)",
                "🚩 Perilaku Baik & Tidak Sehat (Chart + Detail)",
                "🩺 Jumlah Pasien per Puskesmas",
                "📅 Tren Date Start Pasien",
                "📊 Distribusi Usia",
                "🟢 Status Gizi dan Imunisasi",
                "🎯 Distribusi Pekerjaan"
            ]
            pilihan = st.selectbox("Pilih Visualisasi", visualisasi_list)
            
            # Visualisasi berdasarkan pilihan
            if pilihan == "📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak":
                st.subheader("📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
            
                kategori_overall = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
                persentase_overall = [persentase_tidak_layak_rumah, persentase_tidak_layak_sanitasi, persentase_tidak_baik_perilaku]
            
                # Sorting berdasarkan persentase tertinggi
                sorted_idx = sorted(range(len(persentase_overall)), key=lambda i: persentase_overall[i], reverse=True)
                kategori_overall = [kategori_overall[i] for i in sorted_idx]
                persentase_overall = [persentase_overall[i] for i in sorted_idx]
            
                # Membuat grafik dengan Plotly
                fig = px.bar(
                    x=kategori_overall,
                    y=persentase_overall,
                    text=[f"{x:.2f}%" for x in persentase_overall],
                    labels={"x": "Kategori", "y": "Persentase (%)"},
                    title="Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak",
                    color=kategori_overall
                )
                fig.update_traces(textposition="outside")
            
                st.plotly_chart(fig)
            
            elif pilihan == "📈 Kebiasaan CTPS":
                st.subheader("📈 Kebiasaan CTPS vs Jumlah Pasien")
                
                # Grup data berdasarkan kebiasaan CTPS
                data_ctps = df.groupby("kebiasaan_ctps")["pasien"].count().reset_index()
                data_ctps.columns = ["kebiasaan_ctps", "jumlah_pasien"]
                data_ctps = data_ctps.sort_values(by="jumlah_pasien", ascending=False)
                
                # Hitung persentase
                total_pasien_ctps = data_ctps["jumlah_pasien"].sum()
                data_ctps["persentase"] = (data_ctps["jumlah_pasien"] / total_pasien_ctps) * 100
            
                # Buat plot dengan Plotly
                fig = px.bar(
                    data_ctps, 
                    x="jumlah_pasien", 
                    y="kebiasaan_ctps", 
                    orientation="h",
                    text=data_ctps["jumlah_pasien"].astype(str) + " (" + data_ctps["persentase"].round(1).astype(str) + "%)",
                    labels={"jumlah_pasien": "Jumlah Pasien", "kebiasaan_ctps": "Kebiasaan CTPS"},
                    title="📈 Kebiasaan CTPS vs Jumlah Pasien",
                    color="jumlah_pasien", 
                    color_continuous_scale="Blues"
                )

                # Sesuaikan tampilan teks label
                fig.update_traces(textposition="outside")
                fig.update_layout(yaxis=dict(categoryorder="total ascending"))
            
                # Tampilkan di Streamlit dengan fitur zoom, pan, download otomatis
                st.plotly_chart(fig, use_container_width=True)
            
            elif pilihan == "🐑 Memiliki Hewan Ternak":
                st.subheader("🐑 Memiliki Hewan Ternak vs Jumlah Pasien")
                
                # Grup data berdasarkan kepemilikan hewan ternak
                data_ternak = df.groupby("memiliki_hewan_ternak")["pasien"].count().reset_index()
                data_ternak.columns = ["memiliki_hewan_ternak", "jumlah_pasien"]
                data_ternak = data_ternak.sort_values(by="jumlah_pasien", ascending=False)
            
                # Hitung persentase
                total_pasien_ternak = data_ternak["jumlah_pasien"].sum()
                data_ternak["persentase"] = (data_ternak["jumlah_pasien"] / total_pasien_ternak) * 100
            
                # Buat plot dengan Plotly
                fig = px.bar(
                    data_ternak, 
                    x="jumlah_pasien", 
                    y="memiliki_hewan_ternak", 
                    orientation="h",
                    text=data_ternak["jumlah_pasien"].astype(str) + " (" + data_ternak["persentase"].round(1).astype(str) + "%)",
                    labels={"jumlah_pasien": "Jumlah Pasien", "memiliki_hewan_ternak": "Memiliki Hewan Ternak"},
                    title="🐑 Memiliki Hewan Ternak vs Jumlah Pasien",
                    color="jumlah_pasien", 
                    color_continuous_scale="magma_r"
                )

                # Sesuaikan tampilan teks label
                fig.update_traces(textposition="outside")
                fig.update_layout(yaxis=dict(categoryorder="total ascending"))

                # Tampilkan di Streamlit dengan fitur zoom, pan, dan download otomatis
                st.plotly_chart(fig, use_container_width=True)
                
            elif pilihan == "🏠 Rumah Layak & Tidak Layak (Chart + Detail)":
                st.subheader("🏠 Rumah Layak & Tidak Layak")
                
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
                
                # Buat bar chart dengan Plotly
                fig_bar = px.bar(
                    df_detail,
                    x="Jumlah",
                    y="Kategori",
                    orientation="h",
                    text=df_detail.apply(lambda row: f"{row['Jumlah']} rumah ({row['Persentase']:.1f}%)", axis=1),
                    title="Kategori Rumah Tidak Layak",
                    labels={"Jumlah": "Jumlah Rumah", "Kategori": "Kategori Rumah Tidak Layak"},
                    color="Jumlah",
                    color_continuous_scale="Viridis"
                )
                
                # Sesuaikan tampilan teks dan margin agar tidak terpotong
                fig_bar.update_traces(textposition="outside", textfont=dict(size=10))
                fig_bar.update_layout(
                    xaxis_range=[0, df_detail["Jumlah"].max() + 5],
                    margin=dict(l=150, r=50, t=50, b=50)
                )
                
                st.plotly_chart(fig_bar, use_container_width=True)

            elif pilihan == "🚰 Sanitasi Layak & Tidak Layak (Chart + Detail)":
                st.subheader("🚰 Sanitasi Layak & Tidak Layak")
                
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
                
                # Buat bar chart dengan Plotly Express (horizontal)
                fig_bar = px.bar(
                    df_sanitasi_detail,
                    x="Jumlah",
                    y="Kategori",
                    orientation="h",
                    text=df_sanitasi_detail.apply(lambda row: f"{row['Jumlah']} rumah ({row['Persentase']:.1f}%)", axis=1),
                    title="Kategori Sanitasi Tidak Layak",
                    labels={"Jumlah": "Jumlah Rumah", "Kategori": "Kategori Sanitasi Tidak Layak"},
                    color="Jumlah",
                    color_continuous_scale="Cividis"
                )
                fig_bar.update_traces(textposition="outside", textfont=dict(size=12))
                fig_bar.update_layout(
                    xaxis_title="Jumlah Rumah",
                    yaxis_title="Kategori Sanitasi Tidak Layak",
                    margin=dict(l=150, r=50, t=50, b=50)
                )
                
                st.plotly_chart(fig_bar, use_container_width=True)

            
            elif pilihan == "🚩 Perilaku Baik & Tidak Sehat (Chart + Detail)":
                st.subheader("🚩 Perilaku Baik & Tidak Sehat")
                
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
                
                fig_bar = px.bar(
                    df_perilaku_detail,
                    x="Jumlah",
                    y="Kategori",
                    orientation="h",
                    text="Label",
                    title="Kategori Perilaku Tidak Sehat",
                    labels={"Jumlah": "Jumlah Rumah", "Kategori": "Kategori Perilaku Tidak Sehat"},
                    color="Jumlah",
                    color_continuous_scale="Blues"
                )
                fig_bar.update_traces(textposition="outside", textfont=dict(size=11))
                fig_bar.update_layout(
                    xaxis_title="Jumlah Rumah",
                    yaxis_title="Kategori Perilaku Tidak Sehat",
                    margin=dict(l=150, r=50, t=50, b=50)
                )
                
                st.plotly_chart(fig_bar, use_container_width=True)

            elif pilihan == "🩺 Jumlah Pasien per Puskesmas":
                st.subheader("🩺 Jumlah Pasien per Puskesmas")
                
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
                st.subheader("📅 Tren Date Start Pasien")
                
                # Pastikan kolom date_start dalam format datetime
                df["date_start"] = pd.to_datetime(df["date_start"], errors="coerce")
                
                # Resampling data per bulan agar lebih rapi
                df["year_month"] = df["date_start"].dt.to_period("M")  # Format YYYY-MM
                date_counts = df.groupby("year_month")["pasien"].count().reset_index()
                date_counts["year_month"] = date_counts["year_month"].astype(str)  # Konversi ke string untuk sumbu X
            
                # Membuat grafik dengan Plotly
                fig = px.line(
                    date_counts,
                    x="year_month",
                    y="pasien",
                    markers=True,
                    labels={"year_month": "Bulan", "pasien": "Jumlah Pasien"},
                    title="Tren Date Start Pasien"
                )
                fig.update_traces(line=dict(width=3))
            
                st.plotly_chart(fig)
                
            elif pilihan == "📊 Distribusi Usia":
                st.subheader("📊 Distribusi Usia")
            
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
                        age_gender = df.groupby(["age_group", "gender"]).size().reset_index(name="count")
            
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

                        st.plotly_chart(fig)
                        
            elif pilihan == "🟢 Status Gizi dan Imunisasi":
                st.subheader("🟢 Distribusi Status Gizi dan Imunisasi (Gabungan)")
            
                # Pastikan kolom tersedia
                if "status_imunisasi" not in df.columns:
                    st.warning("Kolom 'status_imunisasi' tidak ditemukan di data.")
                elif "status_gizi" not in df.columns:
                    st.warning("Kolom 'status_gizi' tidak ditemukan di data.")
                else:
                    # Grouping data dengan size(), bukan sum()
                    imunisasi_gizi = df.groupby(["status_gizi", "status_imunisasi"]).size().reset_index(name="count")
            
                    # Cek apakah data kosong
                    if imunisasi_gizi.empty:
                        st.warning("Data tidak tersedia untuk status gizi dan imunisasi.")
                    else:
                        # Membuat grafik dengan Plotly
                        fig = px.bar(
                            imunisasi_gizi,
                            x="status_gizi",
                            y="count",
                            color="status_imunisasi",
                            barmode="group",
                            labels={"count": "Jumlah", "status_gizi": "Status Gizi", "status_imunisasi": "Status Imunisasi"},
                            title="Distribusi Status Gizi berdasarkan Status Imunisasi"
                        )
            
                        # Menampilkan grafik langsung tanpa fungsi tambahan
                        st.plotly_chart(fig)
                        
            elif pilihan == "🎯 Distribusi Pekerjaan":
                st.subheader("🎯 Distribusi Pekerjaan")
                
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
