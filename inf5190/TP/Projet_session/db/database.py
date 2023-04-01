import sqlite3
import requests
import csv
from db.get_data import convert_to_iso


class Database:

    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/db.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def recherche_by(self, recherche, filtre):
        cursor = self.get_connection().cursor()
        if recherche == "":
            resultats = []
            return resultats
        if filtre == "adresse":
            cursor.execute("select id_poursuite,business_id,date,description,adresse,date_jugement,etablissement,"
                           "montant,proprietaire,ville,statut,date_statut,categorie from contrevenant"
                           " where adresse like '%'||?||'%'", (recherche,))
        elif filtre == "etablissement":
            cursor.execute("select id_poursuite,business_id,date,description,adresse,date_jugement,etablissement,"
                           "montant,proprietaire,ville,statut,date_statut,categorie from contrevenant"
                           " where etablissement like '%'||?||'%'", (recherche,))
        else:
            cursor.execute("select id_poursuite,business_id,date,description,adresse,date_jugement,etablissement,"
                           "montant,proprietaire,ville,statut,date_statut,categorie from contrevenant"
                           " where adresse like '%'||?||'%'", (recherche,))
        resultats = cursor.fetchall()
        return resultats

    def update_bd(self):
        cursor = self.get_connection().cursor()
        # url des données libres de Montreal
        csv_url = " https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource" \
                  "/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"

        upsert = "insert into contrevenant (id_poursuite,business_id,date,description,adresse,date_jugement," \
                 "etablissement,montant,proprietaire,ville,statut,date_statut,categorie) VALUES (?, ?, ?, ?, ?, ?, ?," \
                 "?, ?, ?, ?, ?, ?) on conflict(id_poursuite) do update set id_poursuite=excluded.id_poursuite, " \
                 "business_id=excluded.business_id,date=excluded.date,description=excluded.description," \
                 "adresse=excluded.adresse,date_jugement=excluded.date_jugement,etablissement=excluded.etablissement," \
                 "montant=excluded.montant,proprietaire=excluded.proprietaire,ville=excluded.ville," \
                 "statut=excluded.statut,date_statut=excluded.date_statut,categorie=excluded.categorie;"

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

    def get_contrevenants_by_dates(self, date_debut, date_fin):
        cursor = self.get_connection().cursor()
        cursor.execute("select id_poursuite,business_id,date,description,adresse,date_jugement,etablissement," \
                       "montant,proprietaire,ville,statut,date_statut,categorie from contrevenant" \
                       " where date between ? and ?", (date_debut, date_fin))
        results = cursor.fetchall()
        return results

    def get_contrevenant_by_name(self, nom):
        cursor = self.get_connection().cursor()
        cursor.execute("select id_poursuite,business_id,date,description,adresse,date_jugement,etablissement," \
                       "montant,proprietaire,ville,statut,date_statut,categorie from contrevenant" \
                       " where etablissement=?", (nom, ))
        results = cursor.fetchall()
        return results

    def get_contrevenant_names(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select etablissement from contrevenant")
        results = cursor.fetchall()
        return results