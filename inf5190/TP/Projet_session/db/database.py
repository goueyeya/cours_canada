# classe qui gère les connexion et les récupération de
# données de la bd
import sqlite3
import requests
import csv

from db.get_data import convert_to_iso

# url des données libres de Montreal
csv_url = " https://data.montreal.ca/dataset/05a9e718-6810-4e73-" \
          "8bb9-5955efeb91a0/resource" \
          "/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"

upsert = "insert into contrevenant (id_poursuite,business_id,date," \
         "description,adresse,date_jugement,etablissement,montant," \
         "proprietaire,ville,statut,date_statut,categorie) " \
         "VALUES (?, ?, ?, ?, ?, ?, ?," \
         "?, ?, ?, ?, ?, ?) on conflict(id_poursuite) do update " \
         "set id_poursuite=excluded.id_poursuite, " \
         "business_id=excluded.business_id,date=excluded.date," \
         "description=excluded.description," \
         "adresse=excluded.adresse,date_jugement=excluded.date_jugement," \
         "etablissement=excluded.etablissement," \
         "montant=excluded.montant,proprietaire=excluded.proprietaire," \
         "ville=excluded.ville," \
         "statut=excluded.statut,date_statut=excluded.date_statut," \
         "categorie=excluded.categorie;"


class Database:

    def __init__(self):
        self.connection = None

# récupère la connexion
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/db.db')
        return self.connection

# déconnecte la connexion
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

# recherche d'un contrevenant avec un filtre
    def recherche_by(self, recherche, filtre):
        cursor = self.get_connection().cursor()
        if recherche == "":
            resultats = []
            return resultats
        if filtre == "adresse":
            cursor.execute("select id_poursuite,business_id,date,"
                           "description,adresse,date_jugement,etablissement,"
                           "montant,proprietaire,ville,statut,"
                           "date_statut,categorie from contrevenant"
                           " where adresse like '%'||?||'%'", (recherche,))
        elif filtre == "etablissement":
            cursor.execute("select id_poursuite,business_id,date,"
                           "description,adresse,date_jugement,etablissement,"
                           "montant,proprietaire,ville,statut,"
                           "date_statut,categorie from contrevenant"
                           " where etablissement like "
                           "'%'||?||'%'", (recherche,))
        else:
            cursor.execute("select id_poursuite,business_id,date,"
                           "description,adresse,date_jugement,etablissement,"
                           "montant,proprietaire,ville,statut,"
                           "date_statut,categorie from contrevenant"
                           " where adresse like '%'||?||'%'", (recherche,))
        resultats = cursor.fetchall()
        return resultats

# met à jour la bd
    def update_bd(self):
        cursor = self.get_connection().cursor()
        with requests.get(csv_url, stream=True) as response:
            data = (line.decode('utf-8') for line in response.iter_lines())
            reader = csv.reader(data)
            next(reader)  # échappe la 1ere ligne du csv
            for row in reader:
                row[2] = convert_to_iso(row[2])
                row[5] = convert_to_iso(row[5])
                row[11] = convert_to_iso(row[11])
                cursor.execute(upsert, row)  # insertion des valeurs dans la bd
        self.get_connection().commit()

# récupère les contrevenants entre deux dates
    def get_contrevenants_by_dates(self, date_debut, date_fin):
        cursor = self.get_connection().cursor()
        cursor.execute("select id_poursuite,business_id,date,"
                       "description,adresse,date_jugement,etablissement,"
                       "montant,proprietaire,ville,statut,"
                       "date_statut,categorie from contrevenant"
                       " where date between ? and ?", (date_debut, date_fin))
        results = cursor.fetchall()
        return results

# récupère les contrevenants par nom d'établissements
    def get_contrevenant_by_name(self, nom):
        cursor = self.get_connection().cursor()
        cursor.execute("select id_poursuite,business_id,date,"
                       "description,adresse,date_jugement,etablissement,"
                       "montant,proprietaire,ville,statut,"
                       "date_statut,categorie from contrevenant"
                       " where etablissement=?", (nom,))
        results = cursor.fetchall()
        return results

# récupère le nom des contrevenants par nom
    def get_contrevenant_names(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select distinct etablissement from contrevenant")
        results = cursor.fetchall()
        return results

# récupère les nouveaux contrevenants
    def get_new_contrevenants(self):
        cursor = self.get_connection().cursor()
        bd = cursor.execute("select id_poursuite,business_id,date,"
                            "description,adresse,date_jugement,etablissement,"
                            "montant,proprietaire,ville,statut,"
                            "date_statut,categorie from "
                            "contrevenant").fetchall()
        new_bd = []
        with requests.get(csv_url, stream=True) as response:
            data = (line.decode('utf-8') for line in response.iter_lines())
            reader = csv.reader(data)
            next(reader)  # échappe la 1ere ligne du csv
            for row in reader:
                row[0], row[1], row[7] = int(row[0]), int(row[1]), int(row[7])
                row[2] = convert_to_iso(row[2])
                row[5] = convert_to_iso(row[5])
                row[11] = convert_to_iso(row[11])
                new_bd.append(tuple(row))
        # créer une liste des nouveaux éléments sans doublons
        new_contrevenants = list(set([cont for cont in new_bd
                                      if cont[0] not in
                                      [cont2[0] for cont2 in bd]]))
        return ([c[6], c[4]] for c in new_contrevenants)

# recupère le nom des établissments et leur nombre de contravention
    def get_liste_etablissement(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select etablissement, count(*) AS "
                       "nb_infractions from contrevenant "
                       "group by etablissement order "
                       "by nb_infractions DESC;")
        liste = cursor.fetchall()
        return liste

# créé une nouvelle entrée dans la table demande
    def create_demande(self, demande):
        co = self.get_connection()
        co.execute("insert into demande(nom_etablissement, "
                   "adresse, ville, date_visite, nom, prenom, "
                   "description_probleme) values(?, ?, ?, ?, ?, ?, ?)",
                   (demande.nom_etablissement, demande.adresse,
                    demande.ville, demande.date_visite, demande.nom,
                    demande.prenom, demande.description_probleme))
        cursor = co.cursor()
        cursor.execute("select last_insert_rowid()")
        demande.id_demande = cursor.fetchall()[0][0]
        co.commit()
        return demande

# cherche une demande par id de demande
    def search_demande(self, id_demande):
        cursor = self.get_connection().cursor()
        cursor.execute("select id from demande where id = ?", (id_demande, ))
        id_demande = cursor.fetchone()
        return id_demande

# supprime une demande par id
    def delete_demande(self, id_demande):
        cursor = self.get_connection().cursor()
        cursor.execute("delete from demande where id = ?", (id_demande, ))
        self.get_connection().commit()

# créé un utilisateur
    def create_user(self, nom_complet, email, liste, hashed_password, salt):
        cursor = self.get_connection().cursor()
        cursor.execute("insert into user(nom_complet,email, etablissements, "
                       "password, salt) values(?, ?, ?, ?, ""?)",
                       (nom_complet, email, liste, hashed_password, salt))
        self.get_connection().commit()

# récupère les emails de tous les utilisateurs
    def get_email_users(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select email from user")
        emails = cursor.fetchall()
        liste_emails = []
        for email in emails:
            liste_emails.append(email[0])
        return liste_emails

# récupère un utilisateur par son email
    def get_user_by_email(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from user where email = ?", (email, ))
        user = cursor.fetchone()
        return user

# sauvegarde une nouvelle session dans la bd
    def save_session(self, id_session, username):
        connection = self.get_connection()
        connection.execute("insert into session(id_session, "
                           "utilisateur_email) values(?, ?)",
                           (id_session, username))
        connection.commit()

# supprime une session de la bd
    def delete_session(self, id_session):
        connection = self.get_connection()
        connection.execute("delete from session where id_session=?",
                           (id_session,))
        connection.commit()

# récupère un utilisateur par son identifiant de session
    def get_user_by_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from user inner join session "
                       "on user.email = session.utilisateur_email where "
                       "session.id_session = ?", (id_session, ))
        user = cursor.fetchone()
        return user[0], user[1], user[2], user[3], user[4], user[5]

# sauvegarde une image dans la bd
    def save_img(self, id_image, email, image):
        cursor = self.get_connection().cursor()
        cursor.execute("insert into image (id, email_user,image) "
                       "VALUES (?, ?, ?) on conflict(email_user) do update "
                       "set id = excluded.id, image=excluded.image;",
                       (id_image, email, sqlite3.Binary(image.read())))
        self.get_connection().commit()

# récupère une image de la bd
    def load_img(self, id_image):
        cursor = self.get_connection().cursor()
        cursor.execute("select image from image where id=?", (id_image,))
        image = cursor.fetchone()
        if image is None:
            return None
        else:
            blob_data = image[0]
            return blob_data

# sauvegarde les établissements à surveiller d'un utilisateur
    def save_etablissements(self, etablissements):
        cursor = self.get_connection().cursor()
        cursor.execute("update user set etablissements = ?;",
                       (etablissements, ))
        self.get_connection().commit()
        return etablissements

# récupère l'id de l'image par l'email de l'utilisateur
    def get_id_img_by_email(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute("select image.id from image inner join user "
                       "on image.email_user = user.email where email = ?;",
                       (email, ))
        id_img = cursor.fetchone()
        return id_img[0]
