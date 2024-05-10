FROM python:3.8

WORKDIR /app
COPY . /app



RUN pip install flask
RUN pip install psycopg2
RUN pip install -U flask-cors
EXPOSE 5000
CMD ["python","main.py"]

