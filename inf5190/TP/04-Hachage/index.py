from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
import sqlite3
import hashlib
import uuid

app = Flask(__name__)

@app.route('/')
def display_form():
    return render_template("form.html")

@app.route('/envoyer', methods=['POST','GET'])
def save_util():
    if request.method == 'GET':
        return render_template("/")
    else:
        nom = request.form['nom']
        prenom = request.form['prenom']
        courriel = request.form['courriel']
        mdp = request.form['mdp']
        mdpconf = request.form['mdpconf']
        if nom == '' or prenom == '' or courriel == '' or mdp =='' or mdpconf == '':
            return render_template("form.html", error="Tous les champs doivent être remplis.")

        elif mdp != mdpconf:
            return render_template("form.html", error = "Les mots de passes ne correspondent pas.")

        else:
            date = "datetime('now','localtime')"
            salt = uuid.uuid4().hex
            mdp_hashed = hashlib.sha512(str(mdp + salt).encode("utf-8")).hexdigest()

            user = (nom, prenom, courriel, date, salt, mdp_hashed)

            co = sqlite3.connect("database/util.db")

            script = "insert into utilisateur(nom, prenom, courriel, date_inscription, salt, mdp) values(?, ?, ?, ?, ?, ?)"
            cursor = co.cursor()

            cursor.execute(script, user)
            co.commit()
            co.close()
            return render_template("conf.html", nom = nom, prenom = prenom)

@app.route('/confirmation')
def conf():
    return render_template("conf.html")

if __name__ == '__main__':
 app.run(debug=True)
