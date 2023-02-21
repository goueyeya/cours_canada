import sqlite3
from flask import Flask
from flask import request
from flask import g
from flask import abort
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


@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.route("/api/livres/", methods=["GET"])
def display_all_books():
    if request.method == "GET":
        livres = get_db().get_livres()
        data = [{"id": livre[0], "titre": livre[1]} for livre in livres]
        return jsonify(data)


@app.route("/api/book/<id_book>", methods=["GET"])
def display_book(id_book):
    if request.method == "GET":
        nb_book = get_db().nb_livres()
        if not id_book.isnumeric() or int(id_book) > nb_book:
            abort(404, description="Resource not found")
        else:
            book = get_db().get_livre_by_id(id_book)
            data = [{"id": book[0][0], "titre": book[0][1], "auteur": book[0][2], "annee_publi": book[0][3],
                     "nb_pages": book[0][4], "nb_chap": book[0][5]}]
            return jsonify(data)


@app.route("/api/livre/<id_book>", methods=["DELETE"])
def delete_book(id_book):
    if request.method == "DELETE":
        nb_book = get_db().nb_livres()
        if not id_book.isnumeric() or int(id_book) > nb_book:
            abort(404, description="Resource not found")
        else:
            get_db().del_book(id_book)
            return "", 200


@app.route("/api/livre", methods=["POST"])
def add_book():
    if request.method == "POST":
        data = request.get_json()
        if ("titre" and "auteur" and "annee_publi" and "nb_pages" and "nb_chap") in data:
            if type(data["annee_publi"]) == int and type(data["nb_pages"]) == int and type(data["nb_chap"]) == int:
                get_db().add_book(data["titre"], data["auteur"], data["annee_publi"], data["nb_pages"], data["nb_chap"])
                return "", 201
            else:
                return abort(400, "Bad request")
        else:
            return abort(400, "Bad request")

if __name__ == '__main__':
    app.run(debug=True)
