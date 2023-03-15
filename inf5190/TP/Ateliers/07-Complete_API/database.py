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
        cursor.execute("select id, description from grade")
        grades = cursor.fetchall()
        return [(grade[0], grade[1]) for grade in grades]

    def create_person(self, person):
        co = self.get_connection()
        co.execute("insert into person(prenom, nom, age, date_naissance) values(?, ?, ?, ?)",
                   (person.prenom, person.nom, person.age, person.date_naissance))
        cursor = co.cursor()
        cursor.execute("select last_insert_rowid()")
        person.id = cursor.fetchall()[0][0]
        for gp in person.grades:
            co.execute("insert into grade(description) values(?)", [gp, ])
            cursor.execute("select last_insert_rowid()")
            id_grade = cursor.fetchall()[0][0]
            co.execute("insert into gradePerson(idPerson, idGrade) values (?, ?)", (person.id, id_grade))
        co.commit()
        return person

    def update_person(self, person):
        cursor = self.get_connection().cursor()
        cursor.execute("update person set prenom = ?, nom = ?, age = ?, date_naissance = ? where id = ?",
                       (person.prenom, person.nom, person.age, person.date_naissance, person.id))
        person2 = self.search_person(person.id)
        for grade in person2.grades:
            cursor.execute("delete from grade where description = ?", (grade[0],))
        for gp in person.grades:
            cursor.execute("insert into grade(description) values(?)", [gp[0], ])
            cursor.execute("select last_insert_rowid()")
            id_grade = cursor.fetchall()[0][0]
            cursor.execute("insert into gradePerson(idPerson, idGrade) values (?, ?)", (person.id, id_grade))
        self.get_connection().commit()
        return person

    def search_person(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, prenom, nom, "
                       "age, date_naissance from person where id = ?", (id,))
        persons = cursor.fetchall()
        cursor.execute("select distinct description from grade natural join gradePerson where idPerson = ?", (id,))
        grades = cursor.fetchall()
        if len(persons) is 0:
            return None
        else:
            person = persons[0]
            return Person(person[0], person[1], person[2], person[3], person[4], grades)

    def count_persons(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select count(id) from person")
        return cursor.fetchone()[0]

    def get_persons(self):
        nb_per = self.count_persons()
        persons = []
        for i in range(nb_per):
            persons.append(self.search_person(i+1))
        return persons
