from flask import Flask
from flask import g
from flask import render_template
from flask import request
from database import Database
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

app = Flask(__name__, static_url_path="", static_folder="static")
scheduler = BackgroundScheduler()
scheduler.start()


@app.errorhandler(404)
def display_page_not_found(e):
    return render_template("404.html", error=e), 404


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = Database()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@scheduler.scheduled_job(trigger=CronTrigger.from_crontab('00 00 * * *', timezone="America/Montreal"), id='update_id')
def update_database():
    try:
        with app.app_context():
            get_db().update_bd()
    except RuntimeError as e:
        print(e)


@app.route("/", methods=["GET"])
def display_index_page():
    return render_template("index.html")


@app.route("/recherche", methods=["POST"])
def display_search():
    recherche = request.form["search"]
    filtre = request.form["options"] if "options" in request.form else "etablissement"
    results = get_db().recherche_by(recherche, filtre)
    restaurants = list(({"id_poursuite": result[0], "business_id": result[1], "date": result[2], "description":
                         result[3], "adresse": result[4], "date_jugement": result[5], "etablissement": result[6],
                         "montant": result[7], "proprietaire": result[8], "ville": result[9], "statut": result[10],
                         "date_statut": result[11], "categorie": result[12]} for result in results))
    return render_template("recherche.html", search=request.form["search"], restaurants=restaurants)


if __name__ == '__main__':
    app.run(debug=True)
