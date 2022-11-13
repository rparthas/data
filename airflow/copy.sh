#!/bin/bash
cp rocket_launch.py ~/airflow/dags/
cp event_fetcher.py ~/airflow/dags/
sleep 5
if [ "$1" ]; then
  airflow dags trigger $1
fi