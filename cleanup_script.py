import pandas as pd
import datetime as dt
from dateutil import parser

# GitHub-repositorio ja tiedoston polku
CSV_PATH = 'data/sensor_data.csv'

def cleanup_old_data(df, hours=24):
    """
    This function removes rows from the DataFrame that are older than the specified number of hours.
    """
    now = dt.datetime.now()
    cutoff_time = now - dt.timedelta(hours=hours)
    df = df[df.index >= cutoff_time]
    return df

def main():
    # Load data
    try:
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        print(f"File not found: {CSV_PATH}")
        return

    # Parse and set timestamp index
    df['timestamp'] = df['timestamp'].apply(parser.parse)
    df = df.set_index('timestamp')

    # Cleanup old data
    df = cleanup_old_data(df)

    # Save cleaned data back to CSV
    df.to_csv(CSV_PATH)
    print("Old data cleaned and saved successfully.")

if __name__ == "__main__":
    main()
