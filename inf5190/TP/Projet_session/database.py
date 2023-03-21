import sqlite3


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
