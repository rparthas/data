import os

import pandas as pd
import requests
from google.cloud import storage

folder = "data/"

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

init_url = 'https://nyc-tlc.s3.amazonaws.com/trip+data/'
BUCKET = os.environ.get("GCP_GCS_BUCKET", "dtc_data_lake_dezoomcamp-341110")


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client(project="dezoomcamp-341110")
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def web_to_gcs(year, service):
    for i in range(0, 12):
        month = '0' + str(i + 1)
        month = month[-2:]
        file_name = service + '_tripdata_' + year + '-' + month + '.csv'
        request_url = init_url + file_name
        r = requests.get(request_url)
        with open(folder + file_name, 'wb') as f:
            f.write(r.content)
        print(f"Local: {file_name}")
        df = pd.read_csv(folder + file_name)
        file_name = file_name.replace('.csv', '.parquet')
        df.to_parquet(folder + file_name, engine='pyarrow')
        print(f"Parquet: {file_name}")
        upload_to_gcs(BUCKET, f"{service}/{file_name}", folder + file_name)
        print(f"GCS: {service}/{file_name}")


web_to_gcs('2019', 'green')
web_to_gcs('2020', 'green')
web_to_gcs('2019', 'yellow')
web_to_gcs('2020', 'yellow')
