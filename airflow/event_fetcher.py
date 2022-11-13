import datetime as dt
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id="event_fetcher",
    start_date=dt.datetime(2022, 11, 3),
    schedule_interval=dt.timedelta(days=3),
    catchup=True
)

fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /tmp/data/events && "
        "curl -o /tmp/data/events/{{ds}}.json "
        "http://localhost:5000/events?"
        "start_date={{ds}}"
        "&end_date={{next_execution_date.strftime('%Y-%m-%d')}}"
    ),
    dag=dag,
)


def _calculate_stats(**context):
    input_path = context["templates_dict"]["input_path"]
    output_path = context["templates_dict"]["output_path"]
    Path(output_path).parent.mkdir(exist_ok=True)
    events = pd.read_json(input_path)
    print(events.head(10))
    stats = events.groupby(["date", "user"]).size().reset_index()
    Path(output_path).parent.mkdir(exist_ok=True)
    stats.to_csv(output_path, index=False)


calculate_stats = PythonOperator(
    task_id="calculate_stats",
    python_callable=_calculate_stats,
    templates_dict={
        "input_path": "/tmp/data/events/{{ds}}.json",
        "output_path": "/tmp/data/events/{{ds}}.csv",
    },
    dag=dag,
)

fetch_events >> calculate_stats
