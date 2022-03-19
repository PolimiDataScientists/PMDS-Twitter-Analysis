import airflow
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
    'start_date': airflow.utils.dates.days_ago(1),
    'email': ['alessandro1.messori@mail.polimi.it'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('DailyFetchTweets',schedule_interval=timedelta(days=1), default_args=default_args)

t1 = BashOperator(
    task_id='tweepy',
    bash_command='python /usr/local/airflow/dags/daglibs/fetch_tweets.py',
    dag=dag)

