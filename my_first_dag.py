from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'vkm',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='hello_world_vkm',
    default_args=default_args,
    description='Мій перший тестовий DAG',
    schedule=None, # Запускатимемо вручну
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    t1 = BashOperator(
        task_id='print_hello',
        bash_command='echo "Привіт! Airflow працює на моїй віртуалці!"',
    )

    t2 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    t1 >> t2  # Встановлюємо черговість: спочатку t1, потім t2
