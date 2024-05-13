from flask import Flask
from flask_cors import CORS
from flask import request
from Database import Database


def create_app(database, user, password, host, port):
    Database.createConnection(
        database=database, user=user, password=password, host=host, port=port)

    Database.setupDatabase()

    app = Flask(__name__)
    CORS(app)

    @app.route("/Mails", methods=['GET'])
    def get_mails():
        data = Database.getData(
            "select * from Mails where mail_date > CURRENT_DATE-1;")
        return data

    @app.route("/Mails", methods=['POST'])
    def post_mail():
        data = request.json
        print(data['msg_id_data'])
        res = Database.insertData(data=data)
        return res

    return app
