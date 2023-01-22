from Client import Client
import os

print("Ceci est un programme permettant de creer la facture de clients")

try:
    path = input("Entrez un nom pour le dossier ou mettre les clients :")
    os.mkdir(path)
except(IOError, OSError) as why:
    print(why)
else:
    print("Les fichiers disponibles sont : test2.txt et test.txt")

    try:
        file = input("Quel fichier voulez vous lire :")
        # creation des fichiers contenant les factures des clients
        clients = Client.creationClientsByFile(file)

        for client in clients:
            client.facture(path)
    except (IOError, OSError) as why:
        print(why)

