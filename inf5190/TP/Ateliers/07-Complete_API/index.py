from flask import Flask
from flask_json_schema import jsonSchema
from flask_json_schema import JsonValidationError


app = Flask(__name__, static_url_path="", static_folder="static")


@app.route("/api/personne", methods=["POST"])
@app
def create_person():
