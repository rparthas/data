import shutil

import requests
from airflow import utils, DAG
from airflow.operators.bash import BashOperator
import pathlib
import json
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id="rocket_launch",
    start_date=utils.dates.days_ago(14),
    schedule_interval="@daily",
)

download_launches = BashOperator(
    task_id="download_launches",
    bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'",
    dag=dag,
)


def _get_pictures():
    # Ensure directory exists
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)
    # Download all pictures in launches.json
    with open("/tmp/launches.json") as f:
        launches = json.load(f)
    image_urls = [launch["image"] for launch in launches["results"]]
    for image_url in image_urls:
        try:
            image_filename = image_url.split("/")[-1]
            response = requests.get(image_url, stream=True)
            target_file = f"/tmp/images/{image_filename}"
            with open(target_file, "wb") as f:
                shutil.copyfileobj(response.raw, f)
            print(f"Downloaded {image_url} to {target_file}")
        except:
            print("Error")
            continue


get_pictures = PythonOperator(task_id="get_pictures",
                              python_callable=_get_pictures,
                              dag=dag,
                              )

notify = BashOperator(
    task_id="notify",
    bash_command='echo "There are now $(ls /tmp/images/ | wc -l) images."',
    dag=dag,
)

download_launches >> get_pictures >> notify
# _get_pictures()