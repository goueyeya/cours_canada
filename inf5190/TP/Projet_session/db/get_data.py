import requests
import csv

# url des données libres de Montreal
CSV_URL = " https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource" \
          "/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"

# insertion des valeurs dans la bd
insert = "insert into livre () VALUES ();"

# code qui permet de récupérer les donnees de Montreal
# (avec l'encodage correct) et de creer la base de données
with requests.get(CSV_URL, stream=True) as data:
    entries = (line.decode('utf-8') for line in data.iter_lines())
    for row in csv.reader(entries):
        print(row)
