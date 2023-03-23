import csv

import requests

# url des données libres de Montreal
csv_url = " https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource" \
          "/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"

with requests.get(csv_url, stream=True) as reponse:
    data = (line.decode('utf-8') for line in reponse.iter_lines())
    reader = csv.reader(data)
    next(reader)  # échappe la 1ere ligne du csv
    for row in reader:
        print(len(row))
        print(len((row,)))
