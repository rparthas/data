import logging
import os
from datetime import datetime

import pyarrow.csv as pv
import pyarrow.parquet as pq
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from google.cloud import storage


def format_to_parquet(src_file):
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    table = pv.read_csv(src_file)
    pq.write_table(table, src_file.replace('.csv', '.parquet'))


# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def download_parquetize_upload_dag(dag, url_template, csv_template, parquet_gcp_template, bucket):
    with dag:
        download_dataset_task = BashOperator(
            task_id="download_dataset_task",
            bash_command=f"curl -sSfL {url_template} > {csv_template}"
        )

        format_to_parquet_task = PythonOperator(
            task_id="format_to_parquet_task",
            python_callable=format_to_parquet,
            op_kwargs={
                "src_file": f"{csv_template}",
            },
        )

        local_to_gcs_task = PythonOperator(
            task_id="local_to_gcs_task",
            python_callable=upload_to_gcs,
            op_kwargs={
                "bucket": bucket,
                "object_name": f"{parquet_gcp_template}",
                "local_file": f"{csv_template.replace('.csv', '.parquet')}",
            },
        )

        rm_task = BashOperator(
            task_id="rm_dataset_task",
            bash_command=f"rm  {csv_template} {csv_template.replace('.csv', '.parquet')}"
        )

        download_dataset_task >> format_to_parquet_task >> local_to_gcs_task >> rm_task


PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
PREFIX = "fhv"

URL_PREFIX = 'https://s3.amazonaws.com/nyc-tlc/trip+data'
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
TAXI_URL_TEMPLATE = URL_PREFIX + "/" + PREFIX + "_tripdata_{{execution_date.strftime('%Y-%m')}}.csv"
TAXI_CSV_FILE_TEMPLATE = AIRFLOW_HOME + "/" + PREFIX + "_tripdata_{{execution_date.strftime('%Y-%m')}}.csv"
TAXI_PARQUET_FILE = PREFIX + "_tripdata_{{execution_date.strftime('%Y-%m')}}.parquet"
TAXI_PARQUET_GCP_FILE = "raw/" + PREFIX + "_trip_data/" + TAXI_PARQUET_FILE

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

dag = DAG(
    dag_id=PREFIX + "_taxi_gcs_dag_v1",
    schedule_interval="0 6 2 * *",
    default_args=default_args,
    start_date=datetime(2019, 1, 1),
    catchup=False,
    max_active_runs=3,
    tags=['dtc-de'],
)

download_parquetize_upload_dag(dag, TAXI_URL_TEMPLATE, TAXI_CSV_FILE_TEMPLATE,
                               TAXI_PARQUET_GCP_FILE, BUCKET)
