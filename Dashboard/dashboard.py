import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
def load_data():
    return pd.read_csv("/main_data.csv")

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

def plot_highest_lowest_rentals(data):
    seasonal_rentals = data.groupby("season")["total"].agg(["max", "min"]).reset_index()
    seasonal_rentals["season"] = range(len(seasonal_rentals))
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x=seasonal_rentals["season"], y=seasonal_rentals["max"], color="red", s=100, label="Highest Rental", ax=ax)
    sns.scatterplot(x=seasonal_rentals["season"], y=seasonal_rentals["min"], color="blue", s=100, label="Lowest Rental", ax=ax)
    plt.title("Jumlah Penyewa Tertinggi dan Terendah per Musim")
    plt.xlabel("Musim")
    plt.ylabel("Jumlah Penyewa")
    plt.legend()
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
st.title("Analisis Data Bike Sharing")

data_hour = load_data()
data_hour = preprocess_data(data_hour)

# Pilihan visualisasi
option = st.selectbox("Pilih Visualisasi:", [
    "Total Rentals per Season",
    "Highest and Lowest Rentals per Season",
    "Hourly Usage Pattern"
])

if option == "Total Rentals per Season":
    plot_total_rentals(data_hour)
elif option == "Highest and Lowest Rentals per Season":
    plot_highest_lowest_rentals(data_hour)
elif option == "Hourly Usage Pattern":
    plot_hourly_usage(data_hour)

