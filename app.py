from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# Init app
app = Flask(__name__)

#The absolute path of the current folder 
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
#Init db
db = SQLAlchemy(app)
#init ma
ma = Marshmallow(app)

#Person class/model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, name):
        self.name = name

# Create the database tables
with app.app_context():
    db.create_all()


#Product  Schema
class PersonSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")

#Init Schema
person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)


@app.route("/person", methods= ["POST"])
def add_person():
    name = request.json(name)
    
    new_person = Person(name)

    db.session.add(new_person)
    db.session.commit()

    return person_schema.jsonify(new_person)

# Run server
if __name__ == "__main__":
    app.run(debug=True)