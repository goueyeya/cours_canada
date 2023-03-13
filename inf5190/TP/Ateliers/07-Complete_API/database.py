import sqlite3
from .person import Person

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

    def getGrades(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select description from grade")
        grades = cursor.fetchall()
        return [(grade[0], grade[1]) for grade in grades]


    def create_person(self, person):
        co = self.get_connection()
        co.execute("insert into person(prenom, nom, age, date_naissance) values(?, ?, ?, ?)",
                           (person.prenom, person.nom, person.age, person.date_naissance))
        co.commit()
        cursor = co.cursor()
        cursor.execute("select last_insert_rowid()")
        person.id = cursor.fetchall()[0][0]
        grades = self.getGrades()
        for grade in grades:
            for g in person.grades:
                if grade[1] == g:
                    co.execute("insert into gradePerson(idPersonne, idGrade) values (?)", (person.id,grade[0]))
                    co.commit()
                else:
                    co.execute("inser into grade(description) values(?)", [grade[1],])
                    cursor = connection.cursor()
                    cursor.execute("select last_insert_rowid()")
                    id_grade = cursor.fetchall()[0][0]
                    co.execute("insert into gradePerson(idPersonne, idGrade) values (?)", (person.id,id_grade))
                    co.commit()
        return person
