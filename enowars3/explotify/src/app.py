from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging

if(not os.path.exists("files")):
    os.makedirs("files")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///explotify_db/explotify.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = 'super secret key'
app.config["MUSIC_FOLDER"] = "music"
logging.basicConfig(level=logging.DEBUG)
