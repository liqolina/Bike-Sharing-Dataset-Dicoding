
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Mendefinisikan Weather_condition
def create_weather_df(df):
    weather_df = df.groupby(by=["weather_cond","year"]).agg({
        "count": "sum"
    }).reset_index() 
    return weather_df

# Mendefinisikan Suhu Lingkungan
def create_temp_df(df):
    temp_df =  df.groupby(by='temp')[['count']].sum().reset_index() 
    return temp_df

# Mendefinisikan Suhu yang dirasakan Tubuh
def create_atemp_df(df):
    atemp_df =  df.groupby(by='atemp')[['count']].sum().reset_index() 
    return atemp_df

# Mendefinisikan Casual
def create_casual_df(df):
    casual_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return casual_df

# Mendefinisikan Season
def create_season_df(df):
    season_df = df.groupby(by=["season","year"]).agg({
    "count": "sum"
    }).reset_index()
    return season_df

# Mendefinisikan Registered
def create_registered_df(df):
    registered_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_df

# Mendefinisikan Count
def create_count_df(df):
    count_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return count_df

# Mendefinisikan Month and Year
def create_monthly_df(df):
    monthly_df = df.groupby(by=["month","year"]).agg({
        "count": "sum"
    }).reset_index() 
    return monthly_df

# Mendefinisikan Hour
def create_grouped_df(df):
    grouped_df = df.groupby('hr').agg({
        'count': 'mean',      # Jumlah rata rata penyewaan sepeda
        'temp': 'mean',       # Temperatur lingkungan rata - rata per season
        'hum': 'mean',        # Kelembapan rata - rata per season
        'windspeed': 'mean'   # Kecepatan angin rata -rata
    }).reset_index()
    return grouped_df

# Menyiapkan cleaned data
day_clean_df = pd.read_csv("dashboard/day_clean.csv")
hour_clean_df = pd.read_csv("dashboard/hour_clean.csv")

# Filter data
day_clean_df["dateday"] = pd.to_datetime(day_clean_df["dateday"])
hour_clean_df["dateday"] = pd.to_datetime(hour_clean_df["dateday"])
min_date = day_clean_df["dateday"].min()
max_date = day_clean_df["dateday"].max()

with st.sidebar:
    st.image("dashboard/bike_ride.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_clean_df[(day_clean_df["dateday"] >= str(start_date)) & 
                       (day_clean_df["dateday"] <= str(end_date))]

second_df = hour_clean_df[(hour_clean_df["dateday"] >= str(start_date)) & 
                       (hour_clean_df["dateday"] <= str(end_date))]

count_df = create_count_df(main_df)
registered_df = create_registered_df(main_df)
casual_df = create_casual_df(main_df)
temp_df = create_temp_df(main_df)
atemp_df = create_atemp_df(main_df)
season_df = create_season_df(main_df)
weather_df = create_weather_df(main_df)
monthly_df = create_monthly_df(main_df)
grouped_df = create_grouped_df(second_df)

# Membuat dashboard Lengkap

# Dashboard (Header) Judul
st.header('Bike Sharing Dashboard 🚴‍♂️')

# Dashboard (SubHeader)

# Membuat jumlah penyewaan sepeda
st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)

with col1:
    casual_df = casual_df['casual'].sum()
    st.metric('Casual User', value= casual_df)

with col2:
    registered_df = registered_df['registered'].sum()
    st.metric('Registered User', value= registered_df)
 
with col3:
    count_df = count_df['count'].sum()
    st.metric('Total User', value= count_df)

# Membuat dashboard jumlah penyewaan berdasarkan season
st.subheader('Statistik total User berdasarkan Musim')

# Membuat suplot
fig, ax = plt.subplots()

# Membuat barplot
sns.barplot(
    data=season_df,
    x="season", 
    y="count", 
    hue="year", 
    palette="viridis")

# Membuat judul, label X dan label Y 
plt.ylabel("Jumlah")
plt.xlabel("Season")
plt.title("Jumlah total sepeda yang disewakan berdasarkan Musim")
plt.legend(
    title="Tahun", 
    loc="upper right")  

for container in ax.containers:
    ax.bar_label(container, fontsize= 8, color= 'white', weight= 'bold', label_type= 'edge')
plt.tight_layout()

st.pyplot(fig)

# Membuat dashboard jumlah penyewaan berdasarkan cuaca
st.subheader("Statistik total user berdasarkan Cuaca")

# membuat subplot
fig, ax = plt.subplots()

# Buat barplot
sns.barplot(
    data=weather_df,
    x="weather_cond", 
    y="count", 
    hue="year", 
    palette="viridis")

# Mengatur judul, label y, dan label x
plt.ylabel("Jumlah Penyewa")
plt.xlabel("Cuaca")
plt.title("Jumlah total sepeda yang disewakan berdasarkan Cuaca")
plt.legend(title="Tahun", loc="upper right")  

for container in ax.containers:
    ax.bar_label(container, fontsize= 8, color= 'white', weight= 'bold', label_type= 'edge')
plt.tight_layout()

st.pyplot(fig)

# Membuat dashboard jumlah penyewaan berdasarkan Bulan dan Tahun
st.subheader("Jumlah total sepeda yang disewakan berdasarkan Bulan dan tahun")

# Membuat subplot
fig, ax = plt.subplots()

# Membuat urutan bulan
monthly_df["month"] = pd.Categorical(monthly_df["month"], 
                                           categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], 
                                           ordered=True)

# Buat lineplot
sns.lineplot(
    data=monthly_df,
    x="month",
    y="count",
    hue="year",
    palette="viridis",
    marker="o")

# Mengatur judul, label y, dan label x
plt.title("Jumlah total sepeda yang disewakan berdasarkan Bulan dan tahun")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewa")
plt.legend(title="Tahun", loc="upper right")
plt.tight_layout()

st.pyplot(fig)

# Membuat dashboard Perbandingan Jumlah Registered dengan Casual
st.subheader("Perbandingan Jumlah Registered dengan Casual")

# Membuat subplot
fig, ax = plt.subplots(figsize=(7, 7))

# Data Untuk Casual
total_casual = sum(main_df['casual'])

# Data Untuk Registered
total_registered = sum(main_df['registered'])

# Data untuk Pieplot
data = [total_casual, total_registered]
labels = ['Casual', 'Registered']

# Membuat label Pieplot
plt.pie(
    data,
    labels=labels,
    autopct='%1.1f%%',
    colors=["gold", "tomato"]
    )

# Membuat label Pieplot
plt.title("Perbandingan Jumlah Registered dengan Casual")

st.pyplot(fig)

# Membuat dashboard Analisis Regresi berdasarkan Suhu Lingkungan
st.subheader("Analisis Regresi berdasarkan Suhu Lingkungan")

# Membuat subplot
fig, ax = plt.subplots()

# Membuat Regplot
sns.regplot(
    x=main_df["temp"],
    y=main_df["count"]
    )

# Membuat label Regplot
plt.title("Analisis Regresi berdasarkan Suhu Lingkungan")
plt.xlabel("Temperatur (Celcius)")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.tight_layout()

st.pyplot(fig)

# Membuat dashboard Analisis Regresi berdasarkan Suhu yang dirasakan Tubuh
st.subheader("Analisis Regresi berdasarkan Suhu  yang dirasakan Tubuh")

# Membuat subplot
fig, ax = plt.subplots()

# Membuat Regplot
sns.regplot(
    data=main_df,
    x=main_df["atemp"],
    y=main_df["count"]
    )

# Membuat label Regplot
plt.title("Analisis Regresi berdasarkan Suhu  yang dirasakan Tubuh")
plt.xlabel("Temperatur (Celcius)")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.tight_layout()

st.pyplot(fig)

# Membuat dashboard Clustering (Manual Grouping)
st.subheader("Clustering berdasarkan waktu penggunaan, frekuensi penyewaan sepeda, suhu, kelembapan lingkungan, dan kecepatan angin")
st.table(grouped_df)

st.subheader("Clustering waktu penyewaan sepeda dengan jumlah penyewaan sepeda")

# Membuat subplot
fig, ax = plt.subplots()

# Menbuat regression plot untuk menampilkan hubungan season dan jumlah penyewaan sepeda
plt.figure(figsize=(8, 6))
sns.regplot(
    x='hr', 
    y='count', 
    data=grouped_df, 
    scatter_kws={'s': 10}, 
    line_kws={'color': 'red'}
)

# Membuat plot
plt.title('Jumlah Penyewaan Sepeda dengan Waktu')
plt.xlabel('Waktu')
plt.ylabel('Jumlah Penyewaan Sepeda')

st.pyplot(fig)
