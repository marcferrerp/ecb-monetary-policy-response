import io

import pandas as pd
import requests

BASE_URL = "https://data-api.ecb.europa.eu/service/data"


def get_ecb_series(series_key, start="2015-01-01"):
    """Download one series from the ECB Data Portal as a pandas Series.

    Parameters
    ----------
    series_key : str
        Full series key, e.g. "HICP.M.U2.N.000000.4D0.ANR".
    start : str
        First date to download, in YYYY-MM-DD format.

    Returns
    -------
    pd.Series
        Values indexed by date, named after the series key.
    """
    # The dataflow is the part of the key before the first dot
    dataflow, rest = series_key.split(".", 1)
    url = f"{BASE_URL}/{dataflow}/{rest}"

    response = requests.get(url, params={"format": "csvdata", "startPeriod": start})
    if response.status_code != 200:
        raise ValueError(f"Download failed for {series_key} (status {response.status_code})")

    df = pd.read_csv(io.StringIO(response.text))

    # .values drops the original row index so the values align with the new date index
    return pd.Series(
        df["OBS_VALUE"].values,
        index=pd.to_datetime(df["TIME_PERIOD"]),
        name=series_key,
    )