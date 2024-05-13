FROM python:3.8

WORKDIR /app
COPY . /app

RUN pip install flask
RUN pip install psycopg2
RUN pip install -U flask-cors
RUN pip install gunicorn
EXPOSE 8000
CMD ["gunicorn","-b","0.0.0.0:8000","main:create_app('postgres','postgres','1234','host.docker.internal',5432)"]

