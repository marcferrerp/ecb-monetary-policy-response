import io
import pandas as pd
import requests

BASE_URL = "https://data-api.ecb.europa.eu/service/data"



def get_ecb_series(series_key, start="2015-01-01"):
    "Download one series from the ECB Data Portal as a pandas Series."
    # 1. Split the key at the first dot: "HICP.M.U2..." -> "HICP", "M.U2..."
    dataflow, rest = series_key.split(".", 1)

    # 2. Build the URL with an f-string (without the part after the "?")
    url = f"{BASE_URL}/{dataflow}/{rest}"

    # 3. Download it; requests adds the "?format=...&startPeriod=..." part
    response = requests.get(url, params={"format": "csvdata", "startPeriod": start})

    # 4. If the download failed, stop with a clear error message
    if response.status_code != 200:
        raise ValueError(...)

    # 5. Read the CSV text into a DataFrame
    df = pd.read_csv(io.StringIO(response.text))

    # 6. Build a Series: dates as the index, values as floats, key as the name
    values = df["OBS_VALUE"]
    dates = pd.to_datetime(df["TIME_PERIOD"])
    series = pd.Series(values, index = dates, name = series_key)
    return series





