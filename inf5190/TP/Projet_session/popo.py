from xml.dom import minidom

from db.database import Database
import db.database
from index import post_tweet
db = Database()
"""
contrevenants = [["Jean Dupont", "555-1234"], ["Marie Tremblay", "555-5678"], ["Luc Deschamps", "555-9876"]]
token = "AAAAAAAAAAAAAAAAAAAAAFXhmQEAAAAAHfpL36mDEQGOQphkAnwTsO2lQXs%3DUR9ouxUVOPEqjbhOTIf70WQwQ0HrPQx7xEgADKoXILJ1L1drjw"  # Mettez votre token d'authentification ici
response = post_tweet(contrevenants, token)
print(response.text)
"""
 def get_listeeta(liste):
    # Créer un document XML vide
    doc = minidom.Document()

    # Créer l'élément racine
    liste = doc.createElement("liste")
    doc.appendChild(liste)

    for etablissement in liste:
        # Créer l'élément enfant et l'ajouter à l'élément racine
        etab = doc.createElement("etablissement")
        doc.appendChild(etab)
        # Ajouter des attributs à l'élément livre
        etab.setAttribute("Etablissement", liste[0])
        etab.setAttribute("Nombre d'infractions", liste[1])

    # Écrire le document XML dans un fichier encodé en UTF-8
    xml_string =
