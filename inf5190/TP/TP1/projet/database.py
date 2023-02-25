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
        cursor.execute("select count(id) from article")
        return cursor.fetchone()[0]

    def get_article_by_id(self, identifiant):
        cursor = self.get_connection().cursor()
        cursor.execute("select titre, identifiant, auteur, date_publication, paragraphe from article where identifiant"
                       " = ?", [identifiant])
        return (i[0], i[1], i[2], i[3], i[4] for i in cursor)

    def get_article_by_search(self, search):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article like %?%", [search])
        articles = cursor.fetchall()
        return[(i[0], i[1], i[2], i[3], i[4], i[5]) for i in articles]

    def get_last_insert(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article order by date_publication desc limit 5 ")
        articles = cursor.fetchall()
        return[(i[0], i[1], i[2], i[3], i[4], i[5]) for i in articles]

