import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from pytz import timezone
import pytz
import urllib.error
import urllib.request

# GitHub-repositorio ja tiedoston polku
GITHUB_REPO = 'saqfromchurchvillage/kasvihuone'
CSV_URL = 'https://raw.githubusercontent.com/saqfromchurchvillage/kasvihuone/main/data/sensor_data.csv'


# Oletetaan, että Streamlit-serveri käyttää UTC-aikaa
SERVER_TZ = timezone('UTC')
LOCAL_TZ = timezone('Europe/Helsinki')  # Korvaa 'Europe/Helsinki' oikealla aikavyöhykkeelläsi

# Lataa CSV-tiedosto DataFrameksi
@st.cache(ttl=600)  # Välimuistita tiedot 10 minuutiksi
def load_data(url):
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
        df = pd.read_csv(pd.compat.StringIO(data))
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')
        df.index = df.index.tz_localize(SERVER_TZ).tz_convert(LOCAL_TZ)
        return df
    except urllib.error.HTTPError as e:
        st.error(f"HTTPError: {e.code} - {e.reason}")
        st.stop()
    except urllib.error.URLError as e:
        st.error(f"URLError: {e.reason}")
        st.stop()
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

data = load_data(CSV_URL)

# Suodata viimeiset 12 tuntia
now = dt.datetime.now(LOCAL_TZ)
twelve_hours_ago = now - dt.timedelta(hours=12)
data_last_12_hours = data[data.index >= twelve_hours_ago]

# Aseta aikaleima x-akselille
data_last_12_hours = data_last_12_hours.resample('5T').mean()  # Resample 5 minutes average

# Luodaan viivadiagrammi
st.title('Reaaliaikainen Lämpötila- ja Ilmankosteusdata')
st.write(f"Viimeisten 12 tunnin data päivitettynä: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

# Näytä viivadiagrammi
st.line_chart(data_last_12_hours[['temperature', 'humidity']])

# Näytä DataFrame
st.write(data_last_12_hours)
