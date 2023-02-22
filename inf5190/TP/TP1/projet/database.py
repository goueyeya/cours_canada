import sqlite3


class Article:

    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect("database/database.db")
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def get_article_by_id(self, id_article):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article where id = ?", [id_article])
        return (i[0], i[1], i[2], i[3], i[4], i[5] for i in cursor)

    def get_article_by_search(self, search):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article like %?%", [search])
        articles = cursor.fetchall()
        return[(i[0], i[1], i[2], i[3], i[4], i[5]) for i in articles]

    