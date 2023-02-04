from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

app = Flask(__name__)

@app.route('/')
def formulaire():
    return render_template("form.html")

@app.route('/envoyer', methods=['POST'])
def envoyer():
    if request.form['fnom']!= '' and request.form['fprenom']!= '':
        return redirect('/merci')
    else:
        return redirect('/erreur')

@app.route('/merci')
def merci():
    return render_template('merci.html')

@app.route('/erreur')
def erreur():
    return render_template('erreur.html')
