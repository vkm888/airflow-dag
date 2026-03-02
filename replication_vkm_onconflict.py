from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator #попередження про "застарілий імпорт" (Deprecation Warning)
# from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

def migrate_data():
    # 1. Підключаємось до Джерела та Приймача
    source_hook = PostgresHook(postgres_conn_id='pg_source_vkm')
    target_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # 2. Читаємо дані з джерела
    records = source_hook.get_records("SELECT order_id, product_name, amount FROM orders")
    
    # 3. Вставляємо дані через чистий SQL з обробкою конфліктів
    if records:
        # Формуємо SQL запит
        sql = """
            INSERT INTO airflow_orders (order_id, product_name, amount)
            VALUES (%s, %s, %s)
            ON CONFLICT (order_id) DO NOTHING;
        """
        
        # Використовуємо метод run для виконання запиту для кожного рядка
        # (Airflow передасть список records у запит)
        # target_hook.run(sql, parameters=records) # Неспрацював видав помилку, запропоновано через курсор

        # Використовуємо з'єднання (connection), щоб виконати запити в одній транзакції
        conn = target_hook.get_conn()
        cursor = conn.cursor()
        
        try:
            # Використовуємо executemany для швидкої вставки всього списку
            cursor.executemany(sql, records)
            conn.commit()
            print(f"Успішно оброблено {len(records)} записів.")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

with DAG(
    dag_id='vkm_manual_replication_on_conflict',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    # Створюємо таблицю-копію в базі-приймачі
    create_target_table = SQLExecuteQueryOperator(
        task_id='create_target_table',
        conn_id='postgres_default',
        sql="""
            CREATE TABLE IF NOT EXISTS airflow_orders (
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