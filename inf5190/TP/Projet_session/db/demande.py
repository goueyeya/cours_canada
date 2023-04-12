# classe qui gère les demande
class Demande:
    def __init__(self, id_demande, nom_etablissement, adresse,
                 ville, date_visite, nom, prenom, description_probleme):
        self.id_demande = id_demande
        self.nom_etablissement = nom_etablissement
        self.adresse = adresse
        self.ville = ville
        self.date_visite = date_visite
        self.nom = nom
        self.prenom = prenom
        self.description_probleme = description_probleme

# retourne la demande sous forme normalisée
    def asDictionnary(self):
        return {"id": self.id_demande,
                "nom_etablissement": self.nom_etablissement,
                "adresse": self.adresse,
                "ville": self.ville,
                "date_visite": self.date_visite,
                "nom": self.nom,
                "prenom": self.prenom,
                "description_probleme": self.description_probleme
                }
