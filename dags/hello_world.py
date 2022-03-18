from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.path.append('/usr/local/airflow/dags/daglibs')

# Following are defaults which can be overridden later on
default_args = {
    'owner': 'PMDS',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': ['alessandro1.messori@mail.polimmi.it'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# DAG is scheduled to run every minute  
dag = DAG('PrintDate',schedule_interval=timedelta(minutes=1), default_args=default_args)


dag = DAG('Helloworld', default_args=default_args)

# t1, t2, t3 and t4 are examples of tasks created using operators

t1 = BashOperator(
    task_id='task_1',
    bash_command='echo "Hello World from Task 1"',
    dag=dag)

t2 = BashOperator(
    task_id='task_2',
    bash_command='echo "Hello World from Task 2"',
    dag=dag)

t3 = BashOperator(
    task_id='task_3',
    bash_command='echo "Hello World from Task 3"',
    dag=dag)

t4 = BashOperator(
    task_id='task_4',
    bash_command='echo "Hello World from Task 4"',
    dag=dag)

t2.set_upstream(t1)
t3.set_upstream(t1)
t4.set_upstream(t2)