from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import g
from .database import Database
import sqlite3
import hashlib
import uuid
import re

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
    if request.method =="GET":

    else:
        o

@app.route("/article/<id_article>", methods=["GET"])
def article(id_article):
    nb_articles = get_db().nb_articles()
    if request.method == "GET":
        if id_article.isnumeric() or int(id_article) > nb_articles:
            return 404
        else:
            livre = get_db().get_article_by_id(id_article)
            return render_template("un_article.html", livre=livre)



@app.route("/admin",methods=["GET"])
def admin():
    if request.method == "GET":
        o

@app.route("/admin-nouveau",methods=["GET"])
def admin_nouveau():
    if request.method == "GET":
        o
if __name__ == '__main__':
    app.run(debug=True)

