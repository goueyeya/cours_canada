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
        log = "log{}.txt".format(request.form['fnom'])
        data_cont = {"nom": request.form['fnom'],"prenom": request.form['fprenom'],
                     "Language de programmation": request.form['fav_language'],"Langue Maternelle": request.form['langue'],}
        with open("logs/"+log, "w") as file:
            file.write(str(data_cont))
            print("Fichier {} cree !".format(log))    
        return redirect('/merci')
    else:
        return redirect('/erreur')

@app.route('/merci')
def merci():
    return render_template('merci.html')

@app.route('/erreur')
def erreur():
    return render_template('erreur.html')

if __name__ == '__main__':
    app.run()