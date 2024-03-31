from flask import Flask
from database import ConnectDataBase
from flask_cors import CORS

NAME = 'lab1EYAZIS'
USER = 'postgres'
PASSWORD = 'postgres1'
HOST = 'localhost'
UPLOAD_FOLDER = ''

app = Flask(__name__)
CORS(app)
app.secret_key = '123451234554321'
db = ConnectDataBase(NAME, USER, PASSWORD, HOST)
conn = db.connect_to_database()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from wordController import *


if __name__ == "__main__":

    app.config["DEBUG"] = True
    app.run(debug=True)

