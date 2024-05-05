from flask import Flask
from flask_cors import CORS
from flask import make_response
from flask import request
from Database import Database


Database.setupDatabase()

app = Flask(__name__)
CORS(app)


@app.route("/Mails", methods=['GET'])
def get_mails():
    data = Database.getData("select * from Mails;")
    return data


@app.route("/Mails", methods=['POST'])
def post_mail():
    data = request.json
    res = Database.insertData(
        f"""INSERT INTO Mails values($${data['msg_id_data']}$$,$${data['from_message']}$$,$${data['message_data']}$$,$${data['msg_data_extracted']}$$);""")

    return res
