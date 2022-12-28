#!/bin/bash
rm -r ~/airflow/dags/*.py
cp dags/*.py ~/airflow/dags/
sleep 5
if [ "$1" ]; then
  airflow dags trigger $1
fi