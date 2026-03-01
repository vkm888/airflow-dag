from airflow import DAG
# Використовуємо універсальний оператор для Airflow 3
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

default_args = {
    'owner': 'vkm',
}

with DAG(
    dag_id='postgres_demo_vkm',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    # 1. Створення таблиці (змінили назву класу тут)
    create_table = SQLExecuteQueryOperator(
        task_id='create_table',
        conn_id='postgres_default', 
        sql="""
            CREATE TABLE IF NOT EXISTS department_stats (
                dt DATE PRIMARY KEY,
                dept_name VARCHAR(50),
                task_count INT
            );
        """
    )

    # 2. Вставка даних (і тут теж)
    insert_data = SQLExecuteQueryOperator(
        task_id='insert_data',
        conn_id='postgres_default',
        sql="""
            INSERT INTO department_stats (dt, dept_name, task_count)
            VALUES ('{{ ds }}', 'Data Engineering', 1)
            ON CONFLICT (dt) DO UPDATE SET task_count = department_stats.task_count + 1;
        """
    )

    create_table >> insert_data