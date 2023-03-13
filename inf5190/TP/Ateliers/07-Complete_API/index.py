from flask import Flask
from flask import request
from flask import g
from flask import jsonify
from flask import render_template
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError
import json
from .database import Database
from .schemas import update_personne_schema
from .schemas import insert_personne_schema
from .person import Person


app = Flask(__name__, static_url_path="", static_folder="static")
schema = JsonSchema(app)

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        g._database = Database()
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_databases", None)
    if db is not None:
        db.disconnect()

@app.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({"error": e.message, "errors": errors}), 400


@app.route("/")
def documentation():
    return render_template("doc.html")

@app.route("/api/person", methods=["POST"])
@schema.validate(insert_personne_schema)
def create_person():
    data = request.get_json()
    person = Person(None, data["prenom"], data["nom"], data["age"], data["date_naissance"], data["grades"])
    person = get_db().create_person(person)
    return jsonify(person.asDictionnary()), 201
