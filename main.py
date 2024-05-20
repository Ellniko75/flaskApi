from flask import Flask
from flask_cors import CORS
from flask import request
from Database import Database
from flask import make_response
from dotenv import load_dotenv
from errorHandling import IsApiKeyError
import os


def create_app(database, user, password, host, port):
    Database.createConnection(
        database=database, user=user, password=password, host=host, port=port)

    Database.setupDatabase()

    app = Flask(__name__)
    CORS(app)

    @app.route("/Mails", methods=['GET'])
    def get_mails():
        err = IsApiKeyError(request=request)
        if (err):
            return err
        # Check if there is a search param, if not just serve the mails from today
        searchParam = request.args.get('search')
        if (searchParam):
            data = Database.searchData(searchParam=searchParam)
        else:
            data = Database.getData(
                "select * from Mails where msg_date > CURRENT_DATE-1;")
        return data

    @app.route("/Mails", methods=['POST'])
    def post_mail():
        err = IsApiKeyError(request=request)
        if (err):
            return err

        data = request.json
        print(data['msg_id_data'])
        res = Database.insertData(data=data)
        return res

    return app
