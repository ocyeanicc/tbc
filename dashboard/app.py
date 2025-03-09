from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from sklearn.impute import KNNImputer

app = Flask(__name__)

def preprocess_data(df):
    required_columns = {"status_rumah", "sarana_air_bersih", "jamban", "perilaku_merokok", "membersihkan_rumah"}
    if not required_columns.issubset(df.columns):
        return None, "Kolom yang diperlukan tidak ditemukan dalam dataset."
    
    # Identifikasi kolom numerik dan kategori
    kolom_numerik = df.select_dtypes(include=['number']).columns
    kolom_kategori = df.select_dtypes(include=['object']).columns
    
    # Mengisi missing values untuk kolom kategori dengan mode
    df[kolom_kategori] = df[kolom_kategori].apply(lambda x: x.fillna(x.mode()[0]))
    
    # Menggunakan KNN Imputer untuk kolom numerik
    imputer = KNNImputer(n_neighbors=5)
    df[kolom_numerik] = pd.DataFrame(imputer.fit_transform(df[kolom_numerik]), columns=kolom_numerik)
    
    return df, None

def calculate_percentage(df, column, condition):
    total = len(df)
    tidak_layak = df[df[column].str.strip().str.lower() == condition.lower()].shape[0]
    persentase = (tidak_layak / total * 100) if total > 0 else 0
    return tidak_layak, persentase

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_csv(file, sep=';', encoding='utf-8')
            df_clean, error = preprocess_data(df)
            if error:
                return render_template('index.html', error=error)
            
            # Perhitungan jumlah dan persentase berdasarkan dataset
            jumlah_rumah_tidak_layak, persentase_tidak_layak_rumah = calculate_percentage(df_clean, "status_rumah", "Tidak Layak")
            jumlah_sanitasi_tidak_layak = df_clean[(df_clean["sarana_air_bersih"].str.strip().str.lower() == "tidak layak") | 
                                                   (df_clean["jamban"].str.strip().str.lower() == "tidak layak")].shape[0]
            persentase_tidak_layak_sanitasi = (jumlah_sanitasi_tidak_layak / len(df_clean) * 100) if len(df_clean) > 0 else 0
            
            jumlah_perilaku_tidak_baik = df_clean[(df_clean["perilaku_merokok"].str.strip().str.lower() == "ya") | 
                                                  (df_clean["membersihkan_rumah"].str.strip().str.lower() == "jarang")].shape[0]
            persentase_tidak_baik_perilaku = (jumlah_perilaku_tidak_baik / len(df_clean) * 100) if len(df_clean) > 0 else 0
            
            kategori = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
            persentase = [persentase_tidak_layak_rumah, persentase_tidak_layak_sanitasi, persentase_tidak_baik_perilaku]
            jumlah = [jumlah_rumah_tidak_layak, jumlah_sanitasi_tidak_layak, jumlah_perilaku_tidak_baik]
            
            # Membuat grafik
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(kategori, persentase, color=['red', 'orange', 'blue'])
            ax.set_xlabel("Kategori")
            ax.set_ylabel("Persentase (%)")
            ax.set_title("Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
            ax.set_ylim(0, 100)
            ax.grid(axis="y", linestyle="--", alpha=0.7)
            for i, v in enumerate(persentase):
                ax.text(i, v + 2, f"{v:.2f}%", ha="center", fontsize=10)
            
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            
            return render_template('result.html', tables=[df_clean.head(10).to_html()], titles=[''], 
                                   image=img.getvalue().decode('latin1'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
