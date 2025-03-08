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
    temp_df = df.groupby(by='temp').agg({
        'temp': 'sum'
    }).reset_index()
    return temp_df

# Mendefinisikan Suhu yang dirasakan Tubuh
def create_atemp_df(df):
    temp_df = df.groupby(by='atemp').agg({
        'atemp': 'sum'
    }).reset_index()
    return atemp_df

# Mendefinisikan Casual
def create_casual_df(df):
    casual_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return casual_df

casual_df = create_casual_df(main_df)

# Mendefinisikan Season
def create_season_df(df):
    season_df = df.groupby(by=["season","yr"]).agg({
        "count": "sum"
    }).reset_index() 
    return season_df

# Mendefinisikan Registered
def create_registered_df(df):
    registered_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_df

registered_df = create_registered_df(main_df)

# Mendefinisikan Count
def create_count_df(df):
    count_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return count_df

count_df = create_count_df(main_df)

# Mendefinisikan Month and Year
def create_monthly_df(df):
    monthly_df = df.groupby(by=["month","year"]).agg({
        "count": "sum"
    }).reset_index() 
    return monthly_df

# Menyiapkan cleaned data
day_clean_df = pd.read_csv("dashboard/day_clean.csv")
hour_clean_df = pd.read_csv("data/hour_clean.csv")

# Filter data
day_clean_df["dateday"] = pd.to_datetime(day_clean_df["dateday"])
hour_df["dateday"] = pd.to_datetime(hour_clean_df["dateday"])
min_date = day_clean_df["dateday"].min()
max_date = day_clean_df["dateday"].max()

with st.sidebar:
    st.image("dashboard/bike_ride.png")
    
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

# Membuat dashboard Lengkap

# Dashboard (Header) Judul
st.header('Bike Sharing Dashboard 🚲')

# Dashboard (SubHeader)

# Membuat jumlah penyewaan sepeda
st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)

with col1:
    casual_df = casual_df['casual'].sum()
    st.metric('Casual User', value= count_df)

with col2:
    registered_df = registered_df['registered'].sum()
    st.metric('Registered User', value= count_df)
 
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
fig, ax = plt.subplots(figsize=(20, 10))

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

# Buat lineplot
sns.lineplot(
    data=monthly_df,
    x="month",
    y="count",
    hue="year",
    palette="rocket",
    marker="o")

# Mengatur judul, label y, dan label x
plt.title("Jumlah total sepeda yang disewakan berdasarkan Bulan dan tahun")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewa")
plt.legend(title="Tahun", loc="upper right")
plt.tight_layout()

st.pyplot(fig)

# Membuat dashboard Analisis Regresi berdasarkan Suhu Lingkungan
st.subheader("Analisis Regresi berdasarkan Suhu Lingkungan")

# Membuat subplot
fig, ax = plt.subplots()

# Membuat Regplot
sns.regplot(
    x=temp_df, 
    y=count_df
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
    x=atemp_df, 
    y=count_df
    )

# Membuat label Regplot
plt.title("Analisis Regresi berdasarkan Suhu  yang dirasakan Tubuh")
plt.xlabel("Temperatur (Celcius)")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.tight_layout()

st.pyplot(fig)
