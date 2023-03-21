from flask import Flask
from flask import g
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from database import Database

app = Flask(__name__, static_url_path="", static_folder="static")


@app.errorhandler(404)
def display_page_not_found(e):
    return render_template("404.html", error=e), 404


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        g._database = Database()
    return g._database


@app.route("/", methods=["GET"])
def display_index_page():
    return render_template("index.html")


@app.route("/recherche", methods=["POST"])
def display_search():
    recherche = request.form["search"]
    filtre = request.form["options"] if "options" in request.form else "etablissement"
    results = get_db().recherche_by(recherche, filtre)
    restaurants = ({"id_poursuite": result[0], "business_id": result[1], "date": result[2],"description": result[3],
                    "adresse": result[4], "date_jugement": result[5], "etablissement": result[6], "montant": result[7],
                    "proprietaire": result[8], "ville": result[9], "statut": result[10], "date_statut": result[11],
                    "categorie": result[12]} for result in results)
    return render_template("recherche.html", search=request.form["search"], restaurants=restaurants)


# permet de lancer flask sur windows
if __name__ == '__main__':
    app.run(debug=True)
