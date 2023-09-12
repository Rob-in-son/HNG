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
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, name):
        self.name = name

# Create the database tables
with app.app_context():
    db.create_all()

#Product  Schema
class PersonSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "name")

#Init Schema
person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)

#Adding a new person. 
@app.route("/api", methods= ["POST"])
def add_person():
    name = request.json['name']
    
    new_person = Person(name)

    db.session.add(new_person)
    db.session.commit()

    return person_schema.jsonify(new_person)

#Fetching details of a person.
@app.route("/api/<user_id>", methods= ["GET"])
def get_persons(user_id):
    person = Person.query.get(user_id)
    result = person_schema.dump(person)
    return jsonify(result)

#Update person. 
@app.route("/api/<user_id>", methods= ["PUT"])
def update_person(user_id):
    #fetch person
    person = Person.query.get(user_id)
    #get field from request body
    name = request.json['name']
    #Get a new person to submit to the database
    person.name = name
    #save
    db.session.commit()

    return person_schema.jsonify(person)

#Deleting a person.
@app.route("/api/<user_id>", methods= ["DELETE"])
def delete_persons(user_id):
    person = Person.query.get(user_id)
    db.session.delete(person)
    db.session.commit()
    
    return person_schema.jsonify(person)


#Get all persons
@app.route("/api/", methods= ["GET"])
def all_persons():
    all_person = Person.query.all()
    result = persons_schema.dump(all_person)
    return jsonify(result)

# Run server
if __name__ == "__main__":
    app.run(debug=True)