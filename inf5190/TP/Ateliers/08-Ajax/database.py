import sqlite3

class Database:

    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect("db/db.db")
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def get_persons(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, nom, prenom from personne")
        persons = cursor.fetchall()
        return [(person[0], person[1], person[2]) for person in persons]

    def get_person_by_nom(self, id_person):
        cursor = self.get_connection().cursor()
        cursor.execute("select sexe, age, pays_naissance, ville_naissance from personne where id = ?", (id_person, ))
        person = cursor.fetchone()
        return person[0], person[1], person[2], person[3]
