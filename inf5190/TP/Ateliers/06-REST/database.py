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

    def get_livres(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, titre from livre")
        livres = cursor.fetchall()
        return [(livre[0], livre[1]) for livre in livres]

    def get_livre_by_id(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from livre where id = ?", id)
        return [i for i in cursor]
