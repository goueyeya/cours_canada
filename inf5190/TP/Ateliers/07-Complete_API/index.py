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


@app.route('/api/person/<id>', methods=["PUT"])
@schema.validate(update_personne_schema)
def modify_person(id):
    person = get_db().search_person(id)
    if person is None:
        return "", 404
    else:
        data = request.get_json()
        person.prenom = data["prenom"] if ("prenom" in data) else person.prenom
        person.nom = data["nom"] if ("nom" in data) else person.nom
        person.age = data["age"] if ("age" in data) else person.age
        person.date_naissance = data["date_naissance"] if ("date_naissance" in data) else person.date_naissance
        person.grades = data["grades"] if ("grades" in data) else person.grades
        person = get_db().update_person(person)
        return jsonify(person.asDictionnary()), 200


@app.route('/api/person', methods=["GET"])
def get_persons():
    persons = get_db().get_persons()
    return jsonify([person.asDictionnary() for person in persons]), 200


if __name__ == '__main__':
    app.run(debug=True)
