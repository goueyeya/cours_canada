import csv
import datetime
import hashlib
import requests
import smtplib
import tempfile
import uuid
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from xml.dom import minidom

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, jsonify, g, render_template, request, abort, \
    Response, url_for, flash, make_response, session, redirect
from flask_json_schema import JsonSchema, JsonValidationError

from db.database import Database
from db.demande import Demande
from schemas import insert_demande_schema, insert_user_schema, \
    update_etab_user_schema

app = Flask(__name__, static_url_path="", static_folder="static")
scheduler = BackgroundScheduler()
scheduler.start()
schema = JsonSchema(app)
app.secret_key = 'fb87626dd1570068d4e5df3282de21eb649520327' \
                 '4e1e2c9903a0333810888c7'
ALLOWED_EXTENSIONS = {'png', 'jpg'}


# fonctions de gestion d'erreurs
@app.errorhandler(404)
def display_page_not_found(e):
    return render_template("404.html", error=e), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validate_error.message for validate_error in e.errors]
    return jsonify({"error": e.message, "errors": errors}), 400


# récupère la connexion de la db
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = Database()
    return db


# ferme la connexion de la db à la fermeture du site
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


# permet de lancer la routine d'update et d'envoi de mail
@scheduler.scheduled_job(
    trigger=CronTrigger.from_crontab('00 00 * * *', timezone="America"
                                                             "/Montreal"),
    id='update_id')
def launch_routine():
    try:
        with app.app_context():
            new_contrevenants = get_db().get_new_contrevenants()
            get_db().update_bd()
            if len(list(new_contrevenants)) != 0:
                send_email(new_contrevenants)
    except RuntimeError as e:
        print(e)


@app.route("/", methods=["GET"])
def display_index_page():  # affiche la page index
    liste_etablissement = get_db().get_contrevenant_names()
    if "id" in session:
        return render_template("index.html", liste=liste_etablissement)
    return render_template("index.html", liste=liste_etablissement)


# afiche la page de recherche retournée en A2
@app.route("/recherche", methods=["POST"])
def display_search():
    recherche = request.form["search"]
    filtre = request.form["options"] \
        if "options" in request.form else "etablissement"
    results = get_db().recherche_by(recherche, filtre)
    restaurants = list(({"id_poursuite": result[0], "business_id":
                        result[1], "date": result[2], "description":
                        result[3], "adresse": result[4], "date_jugement":
                        result[5], "etablissement": result[6],
                         "montant": result[7], "proprietaire": result[8],
                         "ville": result[9], "statut": result[10],
                         "date_statut": result[11], "categorie":
                             result[12]} for result in results))
    return render_template("recherche.html",
                           search=request.form["search"],
                           restaurants=restaurants)


# valide le format des dates reçues en A2
def validate(date_debut, date_fin):
    try:
        if datetime.date.fromisoformat(date_fin) \
                < datetime.date.fromisoformat(date_debut):
            return False
        datetime.date.fromisoformat(date_debut)
        datetime.date.fromisoformat(date_fin)
        return True
    except ValueError:
        return False


# récupère les contrevenants en fonction des dates -- REST
@app.route("/api/contrevenants", methods=["GET"])
def get_contrevenant_by_dates():
    if not request.args.get("du") or not request.args.get("au"):
        return abort(400, "Paramètres d'URL incorrect, "
                          "il est attendu dans l'URL 'du' et 'au'.")
    if not validate(request.args.get("du"), request.args.get("au")):
        return abort(400, "Format de date incorect. "
                          "Format de date attendu: YYYY-MM-DD.")
    date_debut = request.args.get("du")
    date_fin = request.args.get("au")
    results = get_db().get_contrevenants_by_dates(date_debut, date_fin)
    dico = [{"id_poursuite": result[0], "business_id": result[1],
             "date": result[2], "description":result[3], "adresse":
                 result[4], "date_jugement": result[5],
             "etablissement": result[6], "montant": result[7],
            "proprietaire": result[8], "ville": result[9], "statut":
                 result[10], "date_statut": result[11],
             "categorie": result[12]} for result in results]
    return jsonify(dico), 200


# afiche la documentation REST
@app.route("/doc", methods=["GET"])
def display_documentation():
    return render_template("doc.html")


# récupère un contrevenant spécifié par son nom -- REST
@app.route("/api/contrevenant", methods=["GET"])
def get_contrevenants_by_name():
    if not request.args["name"]:
        return abort(400, "Paramètres d'URL incorrect, "
                          "il est attendu dans l'URL 'name'.")
    nom = request.args["name"]
    results = get_db().get_contrevenant_by_name(nom)
    dico = [{"id_poursuite": result[0], "business_id": result[1],
             "date": result[2], "description": result[3], "adresse":
                 result[4], "date_jugement": result[5],
             "etablissement": result[6], "montant": result[7],
             "proprietaire": result[8], "ville": result[9], "statut":
                 result[10], "date_statut": result[11],
             "categorie": result[12]} for result in results]
    return jsonify(dico), 200


# fonction d'envoi des contrevenants par mail
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
    body = "Cher Admnistrateur,\n\nVoici la liste de tous " \
           "les nouveaux contrevenants:\n" + "\n" \
        .join("- " + cont[0] + "," + cont[1] for cont in contrevenants) + \
           "\nMise à jour du " + \
           datetime.datetime.today().strftime('%d-%m-%y %H:%M:%S') + \
           ".\n\nBien cordialement,\nL'équipe MTLGastroPolice."
    message.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp-relay.sendinblue.com', 587)
    server.starttls()
    server.login(source_address, sender_password)
    server.sendmail(source_address, destination_address, message.as_string())
    server.quit()


# fonction de post de tweet (non implementée)
def post_tweet(contrevenants, token):
    body = "Voici la liste de tous les nouveaux contrevenants:\n" + "\n" \
        .join("- " + cont[0] + "," +
              cont[1] for cont in contrevenants) + "\nMise à jour du :" + \
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


# récupère les données au format json --REST
@app.route("/api/etablissements/json", methods=["GET"])
def get_liste_etablissements():
    liste = get_db().get_liste_etablissement()
    dico = [{"Etablissement":
            {"Nom": li[0], "Nombre d'infractions": li[1]}} for li in liste]
    return jsonify(dico), 200


# récupère les données au format xml --REST
@app.route("/api/etablissements/xml", methods=["GET"])
def get_liste_etablissement_xml():
    liste = get_db().get_liste_etablissement()
    doc = minidom.Document()  # Créer un document XML vide
    root = doc.createElement("etablissements")  # Créer l'élément racine
    doc.appendChild(root)
    for etablissement in liste:
        # Créer l'élément enfant et l'ajouter à l'élément racine
        etab = doc.createElement("etablissement")
        root.appendChild(etab)
        name = doc.createElement("name")  # partie nom
        name_text = doc.createTextNode(etablissement[0])
        name.appendChild(name_text)
        etab.appendChild(name)
        # partie nb infractions
        nb_infrac = doc.createElement("nombre_infractions")
        nb_infrac_text = doc.createTextNode(str(etablissement[1]))
        nb_infrac.appendChild(nb_infrac_text)
        etab.appendChild(nb_infrac)
    xml_string = doc.toxml(encoding='UTF-8')
    return Response(xml_string, mimetype='application/xml'), 200


# récupère les données au format csv --REST
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


# crée une demande d'inspection --REST
@app.route("/api/demande", methods=["POST"])
@schema.validate(insert_demande_schema)
def create_demande():
    data = request.get_json()
    demande = Demande(None, data["nom_etablissement"], data["adresse"],
                      data["ville"], data["date_visite"], data["nom"],
                      data["prenom"], data["description_probleme"])
    demande = get_db().create_demande(demande)
    return jsonify(demande.asDictionnary()), 201


# affiche le formulaire de plainte
@app.route("/formulaire_plainte", methods=["GET"])
def display_formulaire_plainte():
    return render_template("formulaire_plainte.html")


# affiche la page de confirmation de l'envoi de la plainte
@app.route("/confirmation_formulaire_plainte", methods=["GET"])
def display_confirmation():
    return render_template("confirmation_formulaire.html")


# supprime une demande spécifiée par son id --REST
@app.route("/api/demande/<int:id_demande>", methods=["DELETE"])
def delete_demande_by_id(id_demande):
    demande = get_db().search_demande(id_demande)
    if demande is None:
        return jsonify({"error": "Opération de suppression "
                                 "de la demande {} non validée car la demande"
                                 " n'existe pas".format(id_demande)}), 404
    else:
        get_db().delete_demande(id_demande)
        return jsonify({"message": "Opération de suppression de la demande "
                                   "{} validée".format(id_demande)}), 200


# crée un utilisateur --REST
@app.route("/api/utilisateur", methods=["POST"])
@schema.validate(insert_user_schema)
def create_user():
    data = request.get_json()
    nom_complet, password, email = data["nom_complet"], \
        data["password"], data["email"]
    existing_email = get_db().get_email_users()
    if email in existing_email:
        return jsonify({"error": "L'email "
                                 "'{}' est déjà utilisé.".format(email)}), 409
    liste = " ;".join(str(etab) for etab in data["etablissements"])
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(
        str(password + salt).encode("utf-8")).hexdigest()
    get_db().create_user(nom_complet, email, liste, hashed_password, salt)
    return jsonify({"message": "Utilisateur {} créé avec "
                               "succès".format(nom_complet)}), 201


# affiche la page d'inscription
@app.route("/subscribe", methods=["GET"])
def display_subscribe_page():
    if "id" in session:
        return redirect(url_for("display_account"))
    return render_template("sub.html")


# affiche la page de connexion
@app.route("/login", methods=["GET"])
def display_login_page():
    if is_authenticated():
        return redirect(url_for("display_account"))
    return render_template("login.html")


# affiche la page de confirmation de création d'un utilisateur
@app.route("/confirmation_formulaire_compte", methods=["GET"])
def display_confirmation_compte():
    return render_template("confirmation_formulaire_compte.html")


# vérifie les identifiants donnée, crée les données de session
# et redirige vers le compte
@app.route("/connexion", methods=["POST", "GET"])
def try_connection():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        # Validation des données du formulaire
        if email == '' or password == '':
            flash("Tous les champs doivent être remplis.")
            return redirect(request.url)
        user = get_db().get_user_by_email(email)
        if user is None:
            flash("Impossible de trouver votre compte.")
            return redirect(request.url)
        salt = user[5]
        hashed_pass = hashlib.sha512(str(password + salt)
                                     .encode("utf-8")).hexdigest()
        if hashed_pass == user[4]:
            id_session = uuid.uuid4().hex
            id_img = get_db().get_id_img_by_email(email) \
                if get_db().get_id_img_by_email(email) is not None else 1
            get_db().save_session(id_session, email)
            session["id"], session["id_img"] = id_session, id_img
            return redirect(url_for("display_account"))
        else:
            flash("Mot de passe ou email incorrect(s).")
            return redirect(request.url)
    if request.method == "GET":
        return redirect(url_for("display_login_page"))


# déconnecte un utilisateur
@app.route('/logout', methods=["GET"])
def logout():
    if not is_authenticated():
        return redirect(url_for("display_index_page"))
    id_session = session["id"]
    session.pop('id', None)
    get_db().delete_session(id_session)
    return redirect("/")


# vérifie qu'une session existe
def is_authenticated():
    return "id" in session


# affiche la page utilisateur
@app.route("/account", methods=["GET"])
def display_account():
    if not is_authenticated():
        return redirect(url_for("display_login_page"))
    user = get_db().get_user_by_session(session["id"])
    return render_template("account.html", user=user)


# vérifie que l'extension de l'image est correct
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# sauvegarde l'image de l'utilsateur
@app.route("/save_img", methods=["POST"])
def save_img():
    if not is_authenticated():
        return redirect(url_for("display_index_page"))
    if "photo" not in request.files:
        flash("Aucune photo sélectionnée", 'warning')
        return redirect(request.url), 400

    img = request.files["photo"]
    user = get_db().get_user_by_session(session["id"])
    id_img = str(uuid.uuid4().hex)
    get_db().save_img(id_img, user[2], img)
    session["id_img"] = id_img
    return "<img src='{}' class='rounded mx-auto d-block img-profil' " \
           "alt='img_profil'>".format("/display_picture/" + id_img + ".png")


# affiche l'image d'un utilisateur
@app.route('/display_picture/<id_img>.png')
def display_picture(id_img):
    if not is_authenticated():
        return redirect(url_for("display_index_page"))
    binary_data = get_db().load_img(id_img)
    if binary_data is None:
        return Response(status=404)
    else:
        response = make_response(binary_data)
        response.headers.set('Content-Type', 'image/png')
    return response


# enregistre les modifications aux établissements à surveiller
# d'un utilisateur
@app.route("/save_etablissement", methods=["POST"])
@schema.validate(update_etab_user_schema)
def save_etablissement():
    if not is_authenticated():
        return redirect(url_for("display_index_page"))
    data = request.get_json()
    liste = ";".join(str(etab) for etab in data["etablissements"])
    etablissements = get_db().save_etablissements(liste)
    return etablissements


if __name__ == '__main__':
    app.run()
