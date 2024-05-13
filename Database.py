import psycopg2
from psycopg2 import sql
from flask import make_response
from datetime import datetime
from DateTimeFormat import parseDateTime


class Database:

    connection = None

    @staticmethod
    def createConnection(database, user, password, host, port):
        Database.connection = psycopg2.connect(
            database=database, user=user, password=password, host=host, port=port)

    @staticmethod
    def setupDatabase():
        with (Database.connection):
            with Database.connection.cursor() as cursor:
                try:
                    sql_query = """
                    CREATE TABLE IF NOT EXISTS Mails(
                    mail_id text primary key,
                    mail_from varchar(255) not null,
                    mail_message text not null,
                    mail_extracted_data text not null,
                    mail_date TIMESTAMP not null
                    )
                    """
                    cursor.execute(sql_query)
                except psycopg2.DatabaseError as e:
                    print(f"ERROR: {e}")

    @staticmethod
    def getData(msg):
        with (Database.connection):
            with Database.connection.cursor() as cursor:
                try:
                    sql_query = f"""
                    {msg}
                    """
                    cursor.execute(sql_query)
                    rows = cursor.fetchall()
                    arrayDictionary = []
                    # Transform the result from the function "fetchall()" to an array of json
                    for row in rows:

                        json = {"msg_id_data": row[0],
                                "from_message": row[1],
                                "message_data": row[2],
                                "msg_data_extracted": row[3],
                                "msg_date": row[4]
                                }

                        arrayDictionary.append(json)
                    return arrayDictionary
                except psycopg2.DatabaseError as e:
                    return make_response(e)

    @staticmethod
    def insertData(data):
        with (Database.connection):
            with Database.connection.cursor() as cursor:
                try:
                    sql_query = sql.SQL("INSERT INTO Mails (mail_id, mail_from, mail_message, mail_extracted_data,mail_date) VALUES ({}, {}, {}, {},{})").format(
                        sql.Literal(data['msg_id_data']),
                        sql.Literal(data['from_message']),
                        sql.Literal(data['message_data']),
                        sql.Literal(data['msg_data_extracted']),
                        sql.Literal(parseDateTime(data['msg_date']))
                    )
                    cursor.execute(
                        sql_query)
                    return make_response("Success", 201)
                except psycopg2.DatabaseError as e:
                    return make_response(f"{e}", 400)
