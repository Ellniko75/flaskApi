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
    print(data['msg_id_data'])
    res = Database.insertData(data=data)
    return res


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
