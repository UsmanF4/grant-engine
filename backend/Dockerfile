FROM python:3.10.13

RUN mkdir fastapi-postgres-boilerplate

RUN mkdir fastapi-postgres-boilerplate/app

WORKDIR /fastapi-postgres-boilerplate/

COPY ./requirements.txt /fastapi-postgres-boilerplate/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fastapi-postgres-boilerplate/requirements.txt

COPY ./start-reload.sh /start-reload.sh
COPY ./worker-start.sh /worker-start.sh

COPY ./app /fastapi-postgres-boilerplate/app
RUN apt-get update && apt-get install -y dos2unix

RUN pip install uvicorn
RUN dos2unix /start-reload.sh /worker-start.sh && chmod +x /start-reload.sh /worker-start.sh

ENV PYTHONPATH=/fastapi-postgres-boilerplate
EXPOSE 8888
CMD ["uvicorn", "--reload", "app.main:app", "--host", "0.0.0.0", "--port", "8888", "--log-level", "info"]