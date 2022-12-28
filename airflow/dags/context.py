import datetime as dt

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id='context',
    start_date=dt.datetime(2022, 11, 17)
)


def _print_context(**context):
    print(context)


print_context = PythonOperator(
    task_id='print_context',
    python_callable=_print_context,
    dag=dag,
)

dummy = EmptyOperator(
    task_id='dummy',
    dag=dag,
)


print_context >> dummy
