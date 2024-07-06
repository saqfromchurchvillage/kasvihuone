import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import urllib.error
import urllib.request
from io import StringIO
from dateutil import parser

# GitHub repository and file path
GITHUB_REPO = 'saqfromchurchvillage/kasvihuone'
CSV_URL = 'https://raw.githubusercontent.com/saqfromchurchvillage/kasvihuone/main/data/sensor_data.csv'
CSV_PATH = 'data/sensor_data.csv'

# Load CSV file into DataFrame
@st.cache_data(ttl=600)  # Cache data for 10 minutes
def load_data(url):
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
        df = pd.read_csv(StringIO(data))  # Using correct StringIO
        if 'timestamp' not in df.columns:
            st.error("CSV file does not contain 'timestamp' column.")
            st.stop()
        
        # Flexible date parsing
        df['timestamp'] = df['timestamp'].apply(parser.parse)
        df = df.set_index('timestamp')
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

# Cleanup old data
def cleanup_old_data(df, hours=24):
    now = dt.datetime.now()
    cutoff_time = now - dt.timedelta(hours=hours)
    df = df[df.index >= cutoff_time]
    return df

data = load_data(CSV_URL)

# Cleanup old data (older than 24 hours)
data = cleanup_old_data(data)

# Filter the last 12 hours of data
now = dt.datetime.now()
twelve_hours_ago = now - dt.timedelta(hours=12)
data_last_12_hours = data[data.index >= twelve_hours_ago]

# Sort data to show the most recent entries first
data_last_12_hours = data_last_12_hours.sort_index(ascending=False)

# Plot data if available
if not data_last_12_hours.empty:
    data_last_12_hours = data_last_12_hours.resample('5T').mean()  # Resample 5 minutes average

    # Create line chart
    st.title('Kasvihuoneen lämpötila ja ilmankosteus')
    st.write(f"Data viimeiseltä 12 tunnilta päivitettynä: {now.strftime('%Y-%m-%d %H+3:%M:%S %Z')}")

    # Show line chart
    st.line_chart(data_last_12_hours[['lämpötila', 'ilmankosteus']])

    # Show DataFrame with most recent data first
    st.write(data_last_12_hours.sort_index(ascending=False))
else:
    st.write("Not enough data for the last 12 hours.")
    st.write(data)

# Save cleaned data back to CSV (optional, requires authentication to push to GitHub)
def save_cleaned_data(df, path):
    df.to_csv(path)

# Uncomment below line to save cleaned data locally (for testing purposes)
# save_cleaned_data(data, CSV_PATH)
