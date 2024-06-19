import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from pytz import timezone
import pytz

# GitHub-repositorio ja tiedoston polku
GITHUB_REPO = 'saqfromchurchvillage/kasvihuone'
CSV_URL = 'https://raw.githubusercontent.com/saqfromchurchvillage/kasvihuone/main/data/sensor_data.csv'


# Oletetaan, että Streamlit-serveri käyttää UTC-aikaa
SERVER_TZ = timezone('UTC')
LOCAL_TZ = timezone('Europe/Helsinki')  # Korvaa 'Europe/Helsinki' oikealla aikavyöhykkeelläsi

# Lataa CSV-tiedosto DataFrameksi
@st.cache(ttl=600)  # Välimuistita tiedot 10 minuutiksi
def load_data(url):
    df = pd.read_csv(url)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

data = load_data(CSV_URL)

# Muunna ajat paikalliselle aikavyöhykkeelle
data['timestamp'] = data['timestamp'].dt.tz_convert(LOCAL_TZ)

# Suodata viimeiset 12 tuntia
now = dt.datetime.now(LOCAL_TZ)
twelve_hours_ago = now - dt.timedelta(hours=12)
data_last_12_hours = data[data['timestamp'] >= twelve_hours_ago]

# Aseta aikaleima x-akselille
data_last_12_hours.set_index('timestamp', inplace=True)

# Luodaan viivadiagrammi
st.title('Reaaliaikainen Lämpötila- ja Ilmankosteusdata')
st.write(f"Viimeisten 12 tunnin data päivitettynä: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

# Näytä viivadiagrammi
st.line_chart(data_last_12_hours[['temperature', 'humidity']])

# Näytä DataFrame
st.write(data_last_12_hours)

