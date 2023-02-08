import sqlite3
import random


def get_maisons():
    liste = []
    "on recupere les maisons de disques"
    cursor.execute("select id from maison_disque")
    for maison in cursor:
        liste.append(maison[0])
    return liste

def get_id_artiste(nom_artiste):

    cursor.execute("select id from artiste where nom = ?", [nom_artiste])
    for row in cursor:
        nom = row[0]
    return nom

def artist_exist(nom_artiste):
    """ on verifie que l'artsite existe """
    exist = "select * from artiste where nom = ?"
    cursor.execute(exist,[nom_artiste])
    if cursor.fetchone() is None:
        return False
    else:
        return True

def create_artiste(nom):
    nb = random.randint(1, 5)
    solo = 1 if (nb == 1) else 0
    artiste = (nom, solo, nb)
    script = "insert into artiste(nom, est_solo, nombre_individus) values(?, ?, ?)"
    cursor.execute(script, artiste)
    co.commit()

def add_album():
    try:
        with open("input.txt",'rt') as file:
            text = file.readlines()
            for line in text:
                line = line.replace('\n',"")
                "on recupere les les valeurs du fichier en input"
                nom, titre, annee = str(line).split("|")

                "on verifie que l'artiste existe ou non"
                est_present = artist_exist(nom)
                "si non on le creer"
                if est_present is False:
                    create_artiste(nom)

                "on creer l'album"
                album = (titre, int(annee), random.choice(maisons_d), get_id_artiste(nom))
                cursor.execute("insert into album (titre, annee, maison_disque_id, artiste_id) values(?, ?, ?, ?)", album)
                co.commit()

    except(IOError, OSError) as why:
        print(why)


co = sqlite3.connect("musique.db")
cursor = co.cursor()
maisons_d = get_maisons()
add_album()