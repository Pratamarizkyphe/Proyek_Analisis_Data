# Import semua library yang dibutuhkan
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title('Dashboard Analisis Polusi Udara dan Cuaca')

# Gathering Data - Mengupload file CSV
st.header("1. Upload Dataset")
uploaded_file = st.file_uploader("Pilih file CSV", type="csv")

if uploaded_file is not None:
    # Membaca dataset
    air_data = pd.read_csv(uploaded_file)

    # Menampilkan preview dataset
    st.subheader("Preview Dataset")
    st.write(air_data.head())

    # Assessing Data - Memeriksa Missing Values, Duplicate dan Tipe Data
    st.header("2. Assessing Data")
    
    # Missing values
    st.subheader("a. Missing Values")
    missing_value = air_data.isnull().sum()
    st.write(missing_value)

    # Duplikasi data
    st.subheader("b. Data Duplikasi")
    duplicates = air_data.duplicated().sum()
    st.write(f"Jumlah Data yang Duplikasi: {duplicates}")

    # Tipe data
    st.subheader("c. Tipe Data dari Masing-masing Kolom")
    st.write(air_data.dtypes)

    # Cleaning Data - Menghilangkan Missing Values
    st.header("3. Cleaning Data")
    st.markdown("""
    - **Metode yang digunakan untuk membersihkan data:**
    - Kolom numerik: Interpolasi Linear.
    - Kolom kategori: Forward Fill.
    """)

    # Membersihkan Missing Values dengan interpolasi pada kolom numerik
    numeric_cols = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    for col in numeric_cols:
        air_data[col] = air_data[col].interpolate(method='linear', limit_direction='forward')
    
    # Forward fill untuk kolom kategori
    air_data['wd'] = air_data['wd'].ffill()

    # Memeriksa kembali Missing Values setelah cleaning
    st.subheader("Hasil Setelah Cleaning")
    missing_value_cleaned = air_data.isnull().sum()
    st.write(missing_value_cleaned)

    # Visualisasi dan Analisis Data
    st.header("4. Exploratory Data Analysis (EDA)")

    st.subheader("a. Pengaruh Cuaca terhadap Polusi Udara")
    st.markdown("**Pengaruh Curah Hujan terhadap PM2.5, NO2, dan CO**")

    # Visualisasi 1: Pengaruh RAIN terhadap PM2.5, NO2, CO
    plt.figure(figsize=(18, 6))

    # Subplot untuk PM2.5
    plt.subplot(1, 3, 1)
    sns.scatterplot(x='RAIN', y='PM2.5', data=air_data)
    plt.title('Pengaruh Curah Hujan terhadap PM2.5')

    # Subplot untuk NO2
    plt.subplot(1, 3, 2)
    sns.scatterplot(x='RAIN', y='NO2', data=air_data)
    plt.title('Pengaruh Curah Hujan terhadap NO2')

    # Subplot untuk CO
    plt.subplot(1, 3, 3)
    sns.scatterplot(x='RAIN', y='CO', data=air_data)
    plt.title('Pengaruh Curah Hujan terhadap CO')

    st.pyplot(plt.gcf())

    # Analisis Karakteristik Polusi berdasarkan waktu
    st.subheader("b. Karakteristik Polusi Berdasarkan Waktu (Tahun, Bulan, Jam)")
    
    plt.figure(figsize=(18, 18))

    # Subplot untuk PM2.5 berdasarkan jam
    plt.subplot(3, 1, 1)
    sns.lineplot(x='hour', y='PM2.5', hue='day', data=air_data)
    plt.title('Karakteristik Harian PM2.5 pada Berbagai Jam')

    # Subplot untuk PM2.5 berdasarkan bulan
    plt.subplot(3, 1, 2)
    sns.lineplot(x='hour', y='PM2.5', hue='month', data=air_data)
    plt.title('Karakteristik Jam PM2.5 Berdasarkan Bulan')

    # Subplot untuk PM2.5 berdasarkan tahun
    plt.subplot(3, 1, 3)
    sns.lineplot(x='month', y='PM2.5', hue='year', data=air_data)
    plt.title('Karakteristik Bulanan PM2.5 Berdasarkan Tahun')

    st.pyplot(plt.gcf())

    # Korelasi Antar Polutan
    st.subheader("c. Korelasi Antar Polutan")
    
    corr_matrix = air_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr()

    plt.figure(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Korelasi Antar Polutan')
    st.pyplot(plt.gcf())

## Conclusion Section
    st.header("5. Kesimpulan dari Analisis")
    st.markdown("""
### 1. **Pengaruh Curah Hujan terhadap Polusi Udara**:
- **Hubungan Curah Hujan dengan Polutan PM2.5, NO2, dan CO**:
    - Dari scatter plot, kita melihat bahwa saat **curah hujan rendah (0-10 mm)**, konsentrasi polutan seperti PM2.5, NO2, dan CO mengalami penurunan yang signifikan.
    - Pada **curah hujan sedang hingga tinggi**, penurunan konsentrasi polusi tidak lagi sejalan dengan kenaikan intensitas hujan, menunjukkan adanya **ambang batas** di mana hujan tidak lagi mampu membersihkan polusi secara efektif.
    - **Hujan** dapat membantu mengurangi partikel di udara, terutama **PM2.5** yang dapat diikat oleh butir air hujan dan diturunkan ke permukaan tanah.

### 2. **Karakteristik Polusi Berdasarkan Waktu**:
- **Jam Harian**:
    - PM2.5 memiliki pola fluktuatif sepanjang hari dengan **puncak di sore hari** (sekitar pukul 15:00-17:00), mungkin terkait dengan meningkatnya aktivitas kendaraan bermotor saat jam pulang kerja.
    - Konsentrasi polutan menurun di malam hari, terutama setelah pukul 22:00, sejalan dengan **penurunan aktivitas industri** dan **lalu lintas**.
  
- **Polusi Berdasarkan Bulan**:
    - Secara musiman, PM2.5 menunjukkan **konsentrasi tertinggi selama musim dingin** (Desember-Februari). Hal ini bisa dikaitkan dengan cuaca yang lebih dingin dan **inversi suhu** yang menjebak polusi di dekat permukaan tanah.
    - Polutan seperti NO2 dan CO juga menunjukkan peningkatan di musim dingin, mengindikasikan adanya peningkatan pembakaran bahan bakar untuk pemanasan.

- **Polusi Berdasarkan Tahun**:
    - Ada **peningkatan konsentrasi polusi** di tahun-tahun belakangan, kemungkinan akibat peningkatan urbanisasi dan aktivitas industri. Namun, tren ini perlu diteliti lebih lanjut untuk mengidentifikasi faktor penyebab utamanya.
""")


else:
    st.warning("Silakan upload file dataset untuk memulai analisis.")
