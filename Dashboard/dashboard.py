import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi tampilan
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.markdown("""
    <style>
    .big-font { font-size:20px !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Load data
csv_url = "https://raw.githubusercontent.com/DivanoRizqiAnandra/MC443D5Y2243-Analisis-data/refs/heads/main/Dashboard/main_data.csv"
data_hour = pd.read_csv(csv_url)

# Konversi kolom tanggal jika ada
data_hour['date'] = pd.to_datetime(data_hour['date'])

def rental_category(total):
    if total < 100:
        return "Low Usage"
    elif 100 <= total < 500:
        return "Medium Usage"
    else:
        return "High Usage"

def preprocess_data(data):
    data["rental_category"] = data["total"].apply(rental_category)
    bins = [0, 6, 12, 18, 24]
    labels = ["Late Night", "Morning", "Afternoon", "Evening"]
    data["time_of_day"] = pd.cut(data["hour"], bins=bins, labels=labels, right=False)
    return data

data_hour = preprocess_data(data_hour)

# Sidebar Filters
st.sidebar.header("📌 Filter Data")
start_date = st.sidebar.date_input("Tanggal Awal", data_hour['date'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", data_hour['date'].max())
season_filter = st.sidebar.multiselect("Musim", options=data_hour['season'].unique(), default=data_hour['season'].unique())
weather_filter = st.sidebar.multiselect("Cuaca", options=data_hour['weather'].unique(), default=data_hour['weather'].unique())
hour_range = st.sidebar.slider("Jam", min_value=0, max_value=23, value=(0, 23))
renter_category = st.sidebar.selectbox("Kategori Penyewa", ["Semua", "Casual", "Registered"])

# Apply Filters
filtered_data = data_hour[
    (data_hour['date'] >= pd.to_datetime(start_date)) &
    (data_hour['date'] <= pd.to_datetime(end_date)) &
    (data_hour['season'].isin(season_filter)) &
    (data_hour['weather'].isin(weather_filter)) &
    (data_hour['hour'].between(hour_range[0], hour_range[1])) 
]

if renter_category == "Casual":
    filtered_data["total"] = filtered_data["casual"]
elif renter_category == "Registered":
    filtered_data["total"] = filtered_data["registered"]

def plot_total_rentals(data):
    seasonal_rentals = data.groupby("season")["total"].sum().reset_index()
    season_order = ["Spring", "Summer", "Fall", "Winter"]
    seasonal_rentals["season"] = pd.Categorical(seasonal_rentals["season"], categories=season_order, ordered=True)
    seasonal_rentals = seasonal_rentals.sort_values("season")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="season", y="total", data=seasonal_rentals, palette="coolwarm", ax=ax)
    plt.xlabel("Season")
    plt.ylabel("Total Rentals")
    plt.title("Total Rentals per Season")
    st.pyplot(fig)

def plot_hourly_usage(data):
    hourly_usage = data.groupby("hour")[["registered", "casual"]].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=hourly_usage, x="hour", y="registered", label="Registered Users", marker="o", ax=ax)
    sns.lineplot(data=hourly_usage, x="hour", y="casual", label="Casual Users", marker="o", ax=ax)
    plt.title("Penggunaan Sepeda Sepanjang Hari")
    plt.xlabel("Jam")
    plt.ylabel("Rata-Rata Pengguna")
    plt.legend()
    st.pyplot(fig)

# Judul aplikasi
st.title("🚲 Bike Sharing Dashboard")
st.markdown('<p class="big-font">Analisis Data Penyewaan Sepeda</p>', unsafe_allow_html=True)

# Pilihan visualisasi
tabs = st.tabs(["📊 Total Penyewaan per Musim", "📈 Pola Penggunaan per Jam"])

with tabs[0]:
    plot_total_rentals(filtered_data)

with tabs[1]:
    plot_hourly_usage(filtered_data)

# Menampilkan data yang difilter
st.write("## 🗂 Hasil Data yang Telah di Filter")
st.dataframe(filtered_data)

# Download Button
st.download_button(label="📥 Download Data yang Telah di Filter", data=filtered_data.to_csv(index=False), file_name="filtered_data.csv", mime="text/csv")

