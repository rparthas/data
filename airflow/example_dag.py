from airflow import DAG, utils
from airflow.decorators import task
from airflow.operators.python import PythonOperator,BranchPythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

with DAG(
        dag_id='learn_example',
        start_date=utils.dates.days_ago(3),
        schedule_interval="@daily"
) as dag:
    @task()
    def step1(**context):
        context["task_instance"].xcom_push(key="message", value="step5")
        return "message"


    @task()
    def step2(message):
        print(message)


    def __step3__(**context):
        message = context["task_instance"].xcom_pull(key="message")
        print(message)
        return message


    step3 = BranchPythonOperator(
        task_id='step3',
        python_callable=__step3__
    )

    step4 = PythonOperator(
        task_id='step4',
        trigger_rule="all_done",
        python_callable=lambda : print("step4")
    )

    step5 = PythonOperator(
        task_id='step5',
        python_callable=lambda: print("step5")
    )

    step6 = PythonOperator(
        task_id='step6',
        python_callable=lambda: print("step6")
    )

    step7 = TriggerDagRunOperator(
        trigger_dag_id="context",
        task_id='step7'
    )


    msg = step1()
    step2(msg)
    step3.set_upstream(msg)
    step4.set_upstream(msg)
    step5.set_upstream(step3)
    step6.set_upstream(step3)
    step7.set_upstream(step4)
