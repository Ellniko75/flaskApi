import psycopg2
import flask
from flask import make_response


class Database:
    connection = psycopg2.connect(
        database="postgres", user='postgres', password='1234', host="localhost", port=5432)

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
                    mail_extracted_data text not null
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
                                "msg_data_extracted": row[3]
                                }

                        arrayDictionary.append(json)
                    return arrayDictionary
                except psycopg2.DatabaseError as e:
                    return make_response(e)

    @staticmethod
    def insertData(msg):
        with (Database.connection):
            with Database.connection.cursor() as cursor:
                try:
                    sql_query = f"""
                    {msg}
                    """
                    cursor.execute(sql_query)
                    return make_response("Success", 201)
                except psycopg2.DatabaseError as e:
                    return make_response(f"{e}", 400)
