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
        nb = cursor.execute("select count(id_art) from article").fetchone()[0]
        return nb

    def get_article_by_identifiant(self, identifiant):
        cursor = self.get_connection().cursor()
        article = cursor.execute("select titre, auteur, date_publication, paragraphe from article "
                                 "where identifiant = ?", [identifiant]).fetchone()
        return article

    def get_article_by_search(self, search):
        cursor = self.get_connection().cursor()
        articles = cursor.execute("select titre, identifiant, date_publication from article where date_publication "
                                  "<= date() and titre in (select titre from article where titre like '%'||?||'%' or "
                                  "paragraphe like '%'||?||'%')",
                                  (search, search)).fetchall()
        return [(i[0], i[1], i[2]) for i in articles]

    def get_last_insert(self):
        cursor = self.get_connection().cursor()
        articles = cursor.execute("select titre, identifiant, auteur, date_publication, paragraphe from article "
                                  "where date_publication <= date() order by date_publication "
                                  "desc limit 5 ").fetchall()
        return [(i[0], i[1], i[2], i[3], i[4]) for i in articles]

    def get_all_articles(self):
        cursor = self.get_connection().cursor()
        articles = cursor.execute("select titre, identifiant, date_publication from article").fetchall()
        return [(i[0], i[1], i[2]) for i in articles]

    def update_article(self, id_art, new_titre, new_paragraphe):
        cursor = self.get_connection().cursor()
        cursor.execute("update article set titre = ?, paragraphe = ? where identifiant = ?", (new_titre, new_paragraphe,
                                                                                              id_art))
        self.get_connection().commit()

    def create_article(self, titre, identifiant, auteur, date_publication, paragraphe):
        cursor = self.get_connection().cursor()
        article = (titre, identifiant, auteur, date_publication, paragraphe)
        cursor.execute("INSERT INTO article (titre, identifiant, auteur, date_publication, paragraphe) "
                       "VALUES (?, ?, ?, ?, ?)", article)
        self.get_connection().commit()
