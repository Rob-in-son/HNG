from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# Init app
app = Flask(__name__)

#The absolute path of the current folder 
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'Sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
#Init db
db = SQLAlchemy(app)
#init ma
ma = Marshmallow(app)

#Person class/model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    track = db.Column(db.String(200))
    gender = db.Column(db.String)
    nationality = db.Column(db.String)

    def __init__(self, name, track, gender, nationality):
        self.name = name
        self.track = track 
        self.gender = gender
        self. nationality = nationality 

class PersonSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "track", "gender", "nationality")

#Init Schema



# Run server
if __name__ == "__main__":
    app.run(debug=True)



