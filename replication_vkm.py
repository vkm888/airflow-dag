from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

def migrate_data():
    # 1. Підключаємось до Джерела (нова віртуалка)
    source_hook = PostgresHook(postgres_conn_id='pg_source_vkm')
    # 2. Підключаємось до Приймача (база поруч з Airflow)
    target_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # 3. Читаємо дані
    records = source_hook.get_records("SELECT order_id, product_name, amount FROM public.orders")
    
    # 4. Записуємо в Приймач (спершу створимо там таблицю, якщо її нема)
    if records:
        target_hook.insert_rows(
            table='orders_replica', 
            rows=records, 
            target_fields=['order_id', 'product_name', 'amount']
        )

with DAG(
    dag_id='vkm_manual_replication',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    # Створюємо таблицю-копію в базі-приймачі
    create_target_table = SQLExecuteQueryOperator(
        task_id='create_target_table',
        conn_id='postgres_default',
        sql="""
            CREATE TABLE IF NOT EXISTS orders_replica (
                order_id INT PRIMARY KEY,
                product_name VARCHAR(100),
                amount DECIMAL(10, 2),
                replicated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
    )

    transfer_data = PythonOperator(
        task_id='transfer_data',
        python_callable=migrate_data
    )

    create_target_table >> transfer_data