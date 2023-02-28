from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import g
from database import Database

app = Flask(__name__)

def get_db():
    db = getattr(g,"_database",None)
    if db is None:
        g._database = Database()
    return g._database


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.route("/",methods=["GET"])
def index():
    nb_articles = get_db().nb_articles()
    if nb_articles < 1:
        return render_template("index.html",msg="Aucun article pour le moment...")
    else:
        articles= get_db().get_last_insert()
        results=({"titre": i[0], "identifiant": i[1], "auteur": i[2],"date_publi": i[3],"paragraphe": i[4]} for i in articles)
        return render_template("index.html", args=results)
        

@app.route("/recherche/<search>", methods=["GET"])
def search_article(search):
    search_db = get_db().get_article_by_search(search)
    if search_db is None:
        return render_template("recherche.html", no_args="")
    else:
        results=({"titre": i[0], "identifiant": i[1], "auteur": i[2],"date_publi": i[3],"paragraphe": i[4]} for i in search_db)
        return render_template("recherche.html",args=results)


@app.route("/article/<identifiant>", methods=["GET"])
def display_article(identifiant):
    article_db = get_db().get_article_by_id(identifiant)
    article = {"titre": article_db[0], "identifiant":article_db[1], "auteur": article_db[2],"date_publi": article_db[3],
              "paragraphe": article_db[4]}
    return render_template("un_article.html", livre=article)


"""
@app.route("/admin",methods=["GET"])
def admin():
    if request.method == "GET":


@app.route("/admin-nouveau",methods=["GET"])
def admin_nouveau():
    if request.method == "GET":
"""


if __name__ == '__main__':
    app.run(debug=True)

