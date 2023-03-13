class Person:
    def __init__(self, id, prenom, nom, age, date_naissance, grades):
        self.id = id
        self.prenom = prenom
        self.nom = nom
        self.age = age
        self.date_naissance = date_naissance
        self.grades = grades

    def asDictionnary(self):
        return {"prenom": self.prenom,
                "nom": self.nom,
                "age": self.age,
                "date_naissance": self.date_naissance,
                "grades": ({"grade": grade} for grade in self.grades)}