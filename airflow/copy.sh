#!/bin/bash
rm ~/airflow/dags/rocket_launch.py
rm ~/airflow/dags/event_fetcher.py
rm ~/airflow/dags/context.py
rm ~/airflow/dags/example_dag.py
cp rocket_launch.py ~/airflow/dags/
cp event_fetcher.py ~/airflow/dags/
cp context.py ~/airflow/dags/
cp example_dag.py ~/airflow/dags/
sleep 5
if [ "$1" ]; then
  airflow dags trigger $1
fi