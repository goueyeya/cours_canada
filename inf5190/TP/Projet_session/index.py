from flask import Flask
from flask import g
from flask import render_template

from database import Database

app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        g._database = Database()
    return g._database


@app.route("/", methods=["GET"])
def display_index_page():
    return render_template("index.html")


# permet de lancer flask sur windows
if __name__ == '__main__':
    app.run(debug=True)
