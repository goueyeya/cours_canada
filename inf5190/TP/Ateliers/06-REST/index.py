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


@app.route("/api/livre/<id_book>", methods=["GET"])
def display_book(id_book):
    if request.method == "GET":
        livre = get_db().get_livre_by_id(id_book)
        nb_book = get_db().nb_livres()
        if id_book > nb_book:
            return 404
        else:
            data = [{"id": livre[0][0], "titre": livre[0][1], "auteur": livre[0][2], "annee_publi": livre[0][3],
                     "nb_pages": livre[0][4], "nb_chap": livre[0][5]}]
            return jsonify(data)

@app.route("/api/livre", methods=["POST"])
def add_book():
    if request.method == "POST":
        data = request.get_json()
        if ("titre" and "auteur" and "annee" and "nb_pages" and "nb_chap") in data:
            if type(data["annee"]) == int and type(data["nb_pages"]) == int and type(data["nb_chap"]) == int:
                get_db().add_book(data["titre"], data["auteur"], data["annee"], data["nb_pages"], data["nb_chap"])
                return 201
            else:
                return 400
        else:
            return 400


if __name__ == '__main__':
    app.run(debug=True)
