FROM puckel/docker-airflow:latest
COPY requirements.txt .
RUN pip install -r requirements.txt
USER root
RUN usermod -G root airflow
USER airflow
RUN mkdir /usr/local/airflow/data