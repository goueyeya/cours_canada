from flask import Flask, abort, url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import g
from database import Database
from datetime import date

app = Flask(__name__)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        g.database = Database()
    return g.database


@app.errorhandler(404)
def display_page_not_found(e):
    return render_template("404.html", error=e), 404


@app.route("/", methods=["GET"])
def display_index_page():
    articles = get_db().get_last_insert()
    results = ({"titre": i[0], "identifiant": i[1], "auteur": i[2], "date_publi": i[3],
                "paragraphe": i[4]} for i in articles)
    return render_template("index.html", articles=results)


@app.route("/recherche", methods=["GET"])
def search_article():
    search_db = get_db().get_article_by_search(request.args['search'])
    results = ({"titre": i[0], "identifiant": i[1], "date_publi": i[2]} for i in search_db)
    return render_template("recherche.html", articles=results, search=request.args['search'])


@app.route("/article/<identifiant>", methods=["GET"])
def display_article(identifiant):
    article_db = get_db().get_article_by_identifiant(identifiant)
    if article_db is None:
        abort(404)
    article = {"titre": article_db[0], "auteur": article_db[1], "date_publi": article_db[2],
               "paragraphe": article_db[3]}
    return render_template("un_article.html", article=article)


@app.route("/admin", methods=["GET"])
def display_admin_page():
    article_db = get_db().get_all_articles()
    results = ({"titre": i[0], "identifiant": i[1], "date_publi": i[2]} for i in article_db)
    return render_template("page_admin.html", articles=results)


@app.route("/admin-modification/<identifiant>", methods=["GET", "POST"])
def update_article(identifiant):
    article_db = get_db().get_article_by_identifiant(identifiant)
    results = {"titre": article_db[0], "auteur": article_db[1], "date_publi": article_db[2],
               "paragraphe": article_db[3], "identifiant": identifiant}
    if request.method == 'POST':
        titre = request.form['titre']
        paragraphe = request.form['paragraphe']
        if not titre or not paragraphe:
            return render_template("modif_article.html", article=results, error='Tous les champs sont requis !')
        if len(paragraphe) > 500:
            return render_template("modif_article.html", article=results, errorlen='Limite de 500 caractères !')
        else:
            get_db().update_article(identifiant, titre, paragraphe)
            return redirect(url_for('display_admin_page'))
    return render_template("modif_article.html", article=results)


@app.route("/admin-nouveau", methods=["GET", "POST"])
def create_article():
    if request.method == 'POST':
        titre = request.form['titre']
        identifiant = request.form['identifiant']
        auteur = request.form['auteur']
        date_publi = request.form['date_publi']
        paragraphe = request.form['paragraphe']
        article_bak = {"titre": request.form['titre'], "identifiant": request.form['identifiant'],
                       "auteur": request.form['auteur'], "date_publi": request.form["date_publi"],
                       "paragraphe": request.form['paragraphe']}
        if not titre or not identifiant or not auteur or not date_publi or not paragraphe:
            return render_template("ajout_article.html", article=article_bak, error='Tous les champs sont requis !')
        elif len(titre) > 100:
            return render_template("ajout_article.html", article=article_bak, errorti='Limite de 100 caractères !')
        elif len(identifiant) > 500:
            return render_template("ajout_article.html", article=article_bak, errorpid='Limite de 50 caractères !')
        elif len(auteur) > 100:
            return render_template("ajout_article.html", article=article_bak, erroraut='Limite de 100 caractères !')
        elif len(paragraphe) > 500:
            return render_template("ajout_article.html", article=article_bak, errorpar='Limite de 500 caractères !')
        elif not date.fromisoformat(date_publi):
            return render_template("ajout_article.html", article=article_bak, errordat='Format de date incorrect !')
        else:
            get_db().create_article(titre, identifiant, auteur, date_publi, paragraphe)
            return redirect(url_for('display_admin_page'))
    return render_template("ajout_article.html", article="")


# permet de lancer flask sur windows
if __name__ == '__main__':
    app.run(debug=True)
