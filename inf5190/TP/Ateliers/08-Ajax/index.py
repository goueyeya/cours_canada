from flask import Flask
from flask import g
from database import Database
from flask import render_template

app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g,"_database", None)
    if db is None:
        db = g._database = Database()
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g,"_database", None)
    if db is not None:
        db.disconnect()


@app.route("/", methods=["GET"])
def display_person():
    persons = get_db().get_persons()
    return render_template("persons.html", persons=persons)


@app.route("/person/<id_person>", methods=["GET"])
def display_infos(id_person):
    info_person = get_db().get_person_by_nom(id_person)
    return render_template("person.html", person=info_person)


if __name__ == '__main__':
    app.run(debug=True)