import sqlite3
import random

# Connexion à la base de données
conn = sqlite3.connect('db.db')
c = conn.cursor()

# Liste de valeurs pour chaque champ
noms = ["Dupont", "Garcia", "Smith", "Nguyen", "Sato", "Silva", "Kumar", "Lee", "Wang", "Kim"]
prenoms = ["Jean", "Maria", "John", "Hanh", "Yoshiko", "João", "Rajesh", "Seung", "Xiaoyun", "Ji-eun"]
sexes = ["M", "F"]
ages = [random.randint(18, 50) for i in range(10)]
pays_naissances = ["France", "Espagne", "USA", "Vietnam", "Japon", "Brésil", "Inde", "Corée du Sud", "Chine", "Corée du Nord"]
villes_naissances = ["Paris", "Madrid", "New York", "Hanoi", "Tokyo", "São Paulo", "New Delhi", "Séoul", "Pékin", "Pyongyang"]

# Insertion de 10 personnes dans la table
for i in range(10):
    nom = noms[i]
    prenom = prenoms[i]
    sexe = random.choice(sexes)
    age = random.choice(ages)
    pays_naissance = pays_naissances[i]
    ville_naissance = villes_naissances[i]
    c.execute("INSERT INTO personne(nom, prenom, sexe, age, pays_naissance, ville_naissance) VALUES (?, ?, ?, ?, ?, ?)",
              (nom, prenom, sexe, age, pays_naissance, ville_naissance))

# Enregistrement des modifications et fermeture de la connexion
conn.commit()
conn.close()
