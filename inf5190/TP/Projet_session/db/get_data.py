import requests
import csv
import sqlite3
import datetime

# transformer les dates en dates standards
def convert_to_iso(date_no_iso):
    date_obj = datetime.datetime.strptime(date_no_iso, "%Y%m%d")
    return date_obj.strftime("%Y-%m-%d")

# url des données libres de Montreal
CSV_URL = " https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource" \
          "/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"

# insertion des valeurs dans la bd
insert = "insert into contrevenant (id_poursuite,business_id,date,description,adresse,date_jugement,etablissement," \
         "montant,proprietaire,ville,statut,date_statut,categorie) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

# code qui permet de récupérer les donnees de Montreal
# (avec l'encodage correct) et de creer la base de données
with requests.get(CSV_URL, stream=True) as reponse:
    data = (line.decode('utf-8') for line in reponse.iter_lines())
    reader = csv.reader(data)
    next(reader)  # échappe la 1ere ligne du csv
    co = sqlite3.connect("db.db")
    cursor = co.cursor()
    for row in reader:
        row[2] = convert_to_iso(row[2])
        row[5] = convert_to_iso(row[5])
        row[11] = convert_to_iso(row[11])
        cursor.execute(insert, row)
    co.commit()
