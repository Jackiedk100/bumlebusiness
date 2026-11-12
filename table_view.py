# Import pandas to structure log data in a table (DataFrame)
import pandas as pd

import data_loader as dl


# Build a table (rows = log entries, columns = fields). Returns None if no logs are found.
def build_table():
    lines = dl.load_logs()
    if lines is None:
        return None
    df = pd.DataFrame(dl.parse_logs(lines))
    # Make timestamp a real datetime instead of text (easier to sort/filter/plot)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    # Make dest_port a number (needed for scatter plots). Invalid values become missing (<NA>)
    if "dest_port" in df.columns:
        df["dest_port"] = pd.to_numeric(df["dest_port"], errors="coerce").astype("Int64")
    return df


def show_table(df, rows=10):
    # to_string() prevents pandas from cutting off columns with "..."
    print(df.head(rows).to_string(index=False))
