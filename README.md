# PMDS-Twitter-Analysis

Small data pipelines created by the PMDS Projects team to do analysis on twitter posts

Greatly insipered by https://github.com/vjgpt/twitter-pipeline

## Build Docker Image
    docker build -t pmds-twitter-analysis .

## Run Airflow Docker Image
    docker run -d -p 8080:8080 -v /path/to/dags/on/your/local/machine/:/usr/local/airflow/dags pmds-twitter-analysis


Once you do that, Airflow is running on your machine, and you can visit the UI by visiting http://localhost:8080/admin/
