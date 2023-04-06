import csv
import datetime
import smtplib
import tempfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from xml.dom import minidom
import requests
import yaml
from flask import Flask, jsonify, g, render_template, request, abort, Response
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


def post_tweet(contrevenants, token):
    body = "Voici la liste de tous les nouveaux contrevenants:\n" + "\n" \
        .join("- " + cont[0] + "," + cont[1] for cont in contrevenants) + "\nMise à jour du :" + \
           datetime.datetime.today().strftime('%d-%m-%y %H:%M:%S') + \
           ".\n\nL'équipe MTLGastroPolice."
    return requests.request(
        "POST",
        "https://api.twitter.com/2/tweets",
        json={"text": body},
        headers={
            "Authorization": "Bearer {}".format(token),
            "Content-Type": "application/json",
        },
    )


@app.route("/api/etablissements/json", methods=["GET"])
def get_liste_etablissements():
    liste = get_db().get_liste_etablissement()
    dico = [{"Etablissement": {"Nom": li[0], "Nombre d'infractions": li[1]}} for li in liste]
    return jsonify(dico), 200


@app.route("/api/etablissements/xml", methods=["GET"])
def get_liste_etablissement_xml():
    liste = get_db().get_liste_etablissement()
    doc = minidom.Document()  # Créer un document XML vide
    root = doc.createElement("etablissements")  # Créer l'élément racine
    doc.appendChild(root)
    for etablissement in liste:
        etab = doc.createElement("etablissement")  # Créer l'élément enfant et l'ajouter à l'élément racine
        root.appendChild(etab)
        name = doc.createElement("name")  # partie nom
        name_text = doc.createTextNode(etablissement[0])
        name.appendChild(name_text)
        etab.appendChild(name)
        nb_infrac = doc.createElement("nombre_infractions")  # partie nb infractions
        nb_infrac_text = doc.createTextNode(str(etablissement[1]))
        nb_infrac.appendChild(nb_infrac_text)
        etab.appendChild(nb_infrac)
    xml_string = doc.toxml(encoding='UTF-8')
    return Response(xml_string, mimetype='application/xml'), 200


@app.route("/api/etablissements/csv", methods=["GET"])
def get_liste_etablissements_csv():
    liste = get_db().get_liste_etablissement()
    with tempfile.TemporaryFile(mode='w+', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Nom_Etablissement", "Nombre_infractions"])
        for etab in liste:
            writer.writerow([etab[0], etab[1]])
        csv_file.seek(0)
        csv_data = csv_file.read()
    return Response(csv_data, mimetype='text/csv')


if __name__ == '__main__':
    app.run(debug=True)
