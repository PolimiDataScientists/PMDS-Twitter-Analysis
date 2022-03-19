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

dag = DAG('DailyFetchTweets', default_args=default_args)

t1 = BashOperator(
    task_id='tweepy',
    bash_command='python /usr/local/airflow/dags/daglibs/fetch_tweet.py',
    dag=dag)

