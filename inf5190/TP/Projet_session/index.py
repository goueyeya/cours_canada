import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yaml
from flask import Flask, jsonify, g, render_template, request, abort
from db.database import Database
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

app = Flask(__name__, static_url_path="", static_folder="static")
scheduler = BackgroundScheduler()
scheduler.start()


@app.errorhandler(404)
def display_page_not_found(e):
    return render_template("404.html", error=e), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


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


@scheduler.scheduled_job(trigger=CronTrigger.from_crontab('03 18 * * *', timezone="America/Montreal"), id='update_id')
def update_database():
    try:
        with app.app_context():
            new_contrevenants = get_db().get_new_contrevenants()
            get_db().update_bd()
            if len(list(new_contrevenants)) != 0:
                send_email(new_contrevenants)
    except RuntimeError as e:
        print(e)


@app.route("/", methods=["GET"])
def display_index_page():
    liste_etablissement = get_db().get_contrevenant_names()
    return render_template("index.html", liste=liste_etablissement)


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


def validate(date_debut, date_fin):
    try:
        if datetime.date.fromisoformat(date_fin) < datetime.date.fromisoformat(date_debut):
            return False
        datetime.date.fromisoformat(date_debut)
        datetime.date.fromisoformat(date_fin)
        return True
    except ValueError:
        return False


@app.route("/api/contrevenants", methods=["GET"])
def get_contrevenant_by_dates():
    if not request.args.get("du") or not request.args.get("au"):
        return abort(400, "Paramètres d'URL incorrect, il est attendu dans l'URL 'du' et 'au'.")
    if not validate(request.args.get("du"), request.args.get("au")):
        return abort(400, "Format de date incorect. Format de date attendu: YYYY-MM-DD.")
    date_debut = request.args.get("du")
    date_fin = request.args.get("au")
    results = get_db().get_contrevenants_by_dates(date_debut, date_fin)
    dico = [{"id_poursuite": result[0], "business_id": result[1], "date": result[2], "description":
        result[3], "adresse": result[4], "date_jugement": result[5], "etablissement": result[6],
             "montant": result[7], "proprietaire": result[8], "ville": result[9], "statut": result[10],
             "date_statut": result[11], "categorie": result[12]} for result in results]
    return jsonify(dico), 200


@app.route("/doc", methods=["GET"])
def display_documentation():
    return render_template("doc.html")


@app.route("/api/contrevenant", methods=["GET"])
def get_contrevenants_by_name():
    if not request.args["name"]:
        return abort(400, "Paramètres d'URL incorrect, il est attendu dans l'URL 'name'.")
    nom = request.args["name"]
    results = get_db().get_contrevenant_by_name(nom)
    dico = [{"id_poursuite": result[0], "business_id": result[1], "date": result[2], "description":
        result[3], "adresse": result[4], "date_jugement": result[5], "etablissement": result[6],
             "montant": result[7], "proprietaire": result[8], "ville": result[9], "statut": result[10],
             "date_statut": result[11], "categorie": result[12]} for result in results]
    return jsonify(dico), 200


def send_email(contrevenants):
    source_address = 'test.uqam.gtoueyeya@gmail.com'
    sender_password = 'htnbUOXxGa8z09Br'
    with open('config.yml', 'r') as config_file:
        config = yaml.safe_load(config_file)
        destination_address = config['Destinataires']['Destinataire_1']
    message = MIMEMultipart()
    message['From'] = source_address
    message['To'] = destination_address
    message['Subject'] = "Nouveaux Contrevenants"
    body = "Cher Admnistrateur,\n\nVoici la liste de tous les nouveaux contrevenants:\n" + "\n" \
        .join("- " + cont[0] + "," + cont[1] for cont in contrevenants) + "\nMise à jour du " + \
           datetime.datetime.today().strftime('%d-%m-%y %H:%M:%S') + \
           ".\n\nBien cordialement,\nL'équipe MTLGastroPolice."
    message.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp-relay.sendinblue.com', 587)
    server.starttls()
    server.login(source_address, sender_password)
    server.sendmail(source_address, destination_address, message.as_string())
    server.quit()


if __name__ == '__main__':
    app.run(debug=True)
