import sqlite3
from flask import Flask
from flask import request
from flask import g
from database import Database
from flask import jsonify

app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route("/api/livres/", methods=["GET"])
def display_all_books():
    if request.method == "GET":
        livres = get_db().get_livres()
        data = [{"id": livre[0], "titre": livre[1]} for livre in livres]
        return jsonify(data)


@app.route("/api/livre/<id>", methods=["GET"])
def display_book(id):
    if request.method == "GET":
        livre = get_db().get_livre_by_id(id)
        data = [{"id": livre[0], "titre": livre[1], "auteur": livre[2], "annee_publi": livre[3], "nb_pages": livre[4], "nb_chap": livre[5]}]
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
