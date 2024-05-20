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
                    msg_id_data text primary key,
                    from_message varchar(255) not null,
                    message_data text not null,
                    msg_data_extracted text not null,
                    msg_date TIMESTAMP not null
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

    def searchData(searchParam):
        with (Database.connection):
            with Database.connection.cursor() as cursor:
                try:
                    sql_query = sql_query = sql.SQL("select * from Mails where from_message ILIKE {} or message_data ILIKE {} or msg_data_extracted ILIKE {}").format(
                        sql.Literal("%"+searchParam+"%"),
                        sql.Literal("%"+searchParam+"%"),
                        sql.Literal("%"+searchParam+"%")

                    )
                    cursor.execute(sql_query)
                    rows = cursor.fetchall()
                    if len(rows) == 0:
                        return []
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
                    sql_query = sql.SQL("INSERT INTO Mails (msg_id_data, from_message, message_data, msg_data_extracted,msg_date) VALUES ({}, {}, {}, {},{})").format(
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
