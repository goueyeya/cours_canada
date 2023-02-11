from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import sqlite3
import hashlib
import uuid
import re

app = Flask(__name__)


@app.route('/')
def display_form():
    return render_template("form.html")


@app.route('/envoyer', methods=['POST', 'GET'])
def save_util():
    if request.method == 'GET':
        return redirect("/")
    else:
        # Récupération des données du formulaire
        nom = request.form['nom']
        prenom = request.form['prenom']
        courriel = request.form['courriel']
        mdp = request.form['mdp']
        mdpconf = request.form['mdpconf']

        # Validation des données du formulaire
        if nom == '' or prenom == '' or courriel == '' or mdp == '' or mdpconf == '':
            return render_template("form.html", error_message="Tous les champs doivent être remplis.")
        elif mdp != mdpconf:
            return render_template("form.html", error_message="Les mots de passes ne correspondent pas.")
        elif len(mdp) < 8:
            return render_template("form.html", error_message="Le mot de passe doit avoir au moins 8 caractères.")
        elif not re.search(r"[a-z]", mdp):
            return render_template("form.html",
                                   error_message="Le mot de passe doit contenir au moins une lettre minuscule.")
        elif not re.search(r"[A-Z]", mdp):
            return render_template("form.html",
                                   error_message="Le mot de passe doit contenir au moins une lettre majuscule.")
        elif not re.search(r"[0-9]", mdp):
            return render_template("form.html", error_message="Le mot de passe doit contenir au moins un chiffre.")

        elif not re.search(r"[.,?:!;'/-]", mdp):
            return render_template("form.html",
                                   error_message="Le mot de passe doit contenir au moins un caractère de ponctuation.")
        else:
            # Génération du salt et du hash du mot de passe
            salt = uuid.uuid4().hex
            mdp_hashed = hashlib.sha512(str(mdp + salt).encode("utf-8")).hexdigest()

            # Enregistrement des données de l'utilisateur dans la base de données
            user = (nom, prenom, courriel, salt, mdp_hashed)
            co = sqlite3.connect("database/util.db")
            script = "insert into utilisateur(nom, prenom, courriel, date_inscription, salt, mdp) values(?, ?, ?, " \
                     "date('now','localtime'), ?, ?) "
            cursor = co.cursor()
            cursor.execute(script, user)
            co.commit()
            co.close()
            return render_template("conf.html", nom=nom, prenom=prenom)





@app.route('/confirmation')
def conf():
    return render_template("conf.html")


if __name__ == '__main__':
    app.run(debug=True)
