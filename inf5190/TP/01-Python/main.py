from Client import Client
from Produit import Produit

# creation des fichiers contenant les factures des clients
clients = Client.creationClientsByFile("test.txt")

for client in clients:
    client.facture()

