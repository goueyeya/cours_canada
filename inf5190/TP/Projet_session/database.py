import sqlite3


class Database:

    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/location.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def recherche_by(self, recherche, by):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from contrevenant where ? = ?", (by, recherche))
        resultats = cursor.fetchall()
        return resultats
