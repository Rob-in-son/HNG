from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import re


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
    try:
        name = request.json['name']
    
        # Check if 'name' is ""
        if name is name.strip() == "":
            return jsonify({"error": "Name field must not be empty"}), 400
        
        #Check if name is empty
        if name is None:
            return jsonify({"error": "Name field must not be empty"}), 400
        # Check if 'name' is a string
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        
        # Check if the name already exists in the database
        existing_person = Person.query.filter_by(name=name).first()
        if existing_person:
            return jsonify({"error": "Name already exists"}), 400
        
        if not re.match("^[A-Za-z]+$", name):
            raise ValueError("Name must contain only letters")
        
        new_person = Person(name)

        db.session.add(new_person)
        db.session.commit()

        return person_schema.jsonify(new_person)
 
    except KeyError:
        return jsonify({"error": "Name is missing in the request"}), 400

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

#Fetching details of a person.
@app.route("/api/<user_id>", methods= ["GET"])
def get_persons(user_id):
    try:
        person = Person.query.get(user_id)

        # Check if person is None (not found)
        if person is None:
            return jsonify({"error": "Person not found"}), 404
        
        result = person_schema.dump(person)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
    
#Update person. 
@app.route("/api/<user_id>", methods= ["PUT"])
def update_person(user_id):
    try:
        #fetch person
        person = Person.query.get(user_id)
        
        #check is user exist
        if person is None:
            return jsonify({"error": "Person not found"}), 404
        
        #get field from request body
        name = request.json['name']

                # Check if 'name' is ""
        if name is name.strip() == "":
            return jsonify({"error": "Name field must not be empty"}), 400
       
        # Check if 'name' is missing
        if name is None:
            return jsonify({"error": "Name field is required"}), 400
        
        #Get a new person to submit to the database
        person.name = name
        #save
        db.session.commit()

        return person_schema.jsonify(person)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Deleting a person.
@app.route("/api/<user_id>", methods= ["DELETE"])
def delete_persons(user_id):
    try:
        person = Person.query.get(user_id)

        # Check if person exist
        if person is None:
            return jsonify({"error": "No such user"}), 404
        
        db.session.delete(person)
        db.session.commit()
        
        return jsonify({"msg": "User has been deleted successfully"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500 


#Get all persons
@app.route("/api/", methods= ["GET"])
def all_persons():
    all_person = Person.query.all()
    result = persons_schema.dump(all_person)
    return jsonify(result)

# Run server
if __name__ == "__main__":
    app.run(debug=True)