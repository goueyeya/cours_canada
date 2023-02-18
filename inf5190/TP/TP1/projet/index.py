from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import sqlite3
import hashlib
import uuid
import re

app = Flask(__name__)

@app.route("/",methods=["GET"])
def index():
    if request.method =="GET":

    else:


@app.route("/article/<identifiant>", methods=["GET"])
def article():

@app.route("/admin",methods=["GET"])
def admin():

@app.route("/admin-nouveau",methods=["GET"])
def admin_nouveau():


if __name__ == '__main__':
    app.run(debug=True)