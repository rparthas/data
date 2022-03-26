import glob
import pandas as pd

prefix = 'yellow'

for filename in glob.glob(f"/users/rajagopalps/data/{prefix}/*.parquet"):
    df = pd.read_parquet(filename)
    for col in ['VendorID', 'RatecodeID', 'passenger_count', 'payment_type']:
        df[col] = df.fillna({col: 0})[col].astype(int)
    df.to_parquet(f"/users/rajagopalps/data/{prefix}_new/{filename.split('/')[-1]}")

    