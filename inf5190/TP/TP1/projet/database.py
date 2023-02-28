import sqlite3


class Database:

    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect("database/database.db")
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def nb_articles(self):
        cursor = self.get_connection().cursor()
        nb = cursor.execute("select count(id) from article").fetchone()[0]
        return nb

    def get_article_by_id(self, identifiant):
        cursor = self.get_connection().cursor()
        article = cursor.execute("select titre, identifiant, auteur, date_publication, paragraphe from article "
                                 "where identifiant = ?", [identifiant]).fetchone()
        return article

    def get_article_by_search(self, search):
        cursor = self.get_connection().cursor()
        articles = cursor.execute("select * from article like %?%", [search]).fetchall()
        return[(i[0], i[1], i[2], i[3], i[4], i[5]) for i in articles]

    def get_last_insert(self):
        cursor = self.get_connection().cursor()
        articles = cursor.execute("select * from article where date_publication <= date('now','localtime')"
                                  "order by date_publication desc limit 5 ").fetchall()
        return[(i[0], i[1], i[2], i[3], i[4], i[5]) for i in articles]

