# PMDS-Twitter-Analysis

Small data pipelines created by the PMDS Projects team to do analysis on twitter posts

Greatly insipered by https://github.com/vjgpt/twitter-pipeline

## Install Required Libraries
    pip install -r requirements.txt 

## Pull Airflow Docker Image
    docker pull puckel/docker-airflow

## Run Airflow Docker Image
    docker run -d -p 8080:8080 -v /path/to/dags/on/your/local/machine/:/usr/local/airflow/dags  puckel/docker-airflow webserver


Once you do that, Airflow is running on your machine, and you can visit the UI by visiting http://localhost:8080/admin/
