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

    def get_livre_by_id(self, id_book):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from livre where id = ?", (id_book,))
        return [(i[0], i[1], i[2], i[3], i[4], i[5]) for i in cursor]

    def nb_livres(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select count(id) from livre")
        nb = cursor.fetchone()
        return nb[0]

    def add_book(self, titre, auteur, annee, nb_pages, nb_chap):
        cursor = self.get_connection().cursor()
        cursor.execute("insert into livre (titre, auteur, annee_publi, nb_pages, nb_chap) VALUES (?, ?, ?, ?, ?)",
                       (titre, auteur, annee, nb_pages, nb_chap))
        self.get_connection().commit()

    def del_book(self, id_book):
        cursor = self.get_connection().cursor()
        cursor.execute("delete from livre where id = ?", [id_book])
        self.get_connection().commit()
