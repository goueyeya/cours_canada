from Produit import Produit

class Client:
    def __init__(self, numero):
        self.numero = numero
        self.produits = []

    def ajouterProduit(self, produit):
        self.produits.append(produit)

    def facture(self):
        text = "Client numéro " + self.numero + "\n\n             N° de produit  Qte      Prix  Total (tx)\n"
        j = 0
        qte = 0
        total_fac = 0
        for i in self.produits:# pour chaque produits dans la liste de produits
            # on affiche le produit
            text = text + "Produit #" + str(j + 1) + "   " + str(i.getNumero()) + "       " + str(i.getQuantite()) \
                   + "     " + str(i.getPrixUnitaire()) + "      " + str(i.getTotal()) + "\n"
            qte += int(i.getQuantite())
            total_fac += float(i.getTotal())
            j += 1

        if qte >= 100:
            text = text + "\nTotal avant rabais : " + str(round(total_fac, 2)) \
                   + "\nRabais : " + str(round((total_fac * 15 / 100), 2)) \
                   + "\nTotal : " + str(round((total_fac - total_fac * 15 / 100), 2)) + "\n"
        else:
            text = text + "Total avant rabais : " + str(round(total_fac, 2)) \
                   + "\nRabais : 0" \
                     "\nTotal : " + str(round(total_fac, 2))

        new_file = "Client{}.txt".format(self.getNumero())
        with open(new_file, "w") as file:
            file.write(text)
            print("Fichier {} cree !".format(new_file))

    def getNumero(self):
        return self.numero

    @classmethod
    def creationClientsByFile(cls, file_name):
        # récuperation du contenu du fichier en entrée
        with open(file_name, 'r') as fp:
            file = fp.readlines()

        # creation d'une liste temporaire de numero de client par ligne
        tmp_num_clients = []
        for line in file:
            num_c = line.split(' ')[0]
            tmp_num_clients.append(num_c)
        # selection unique par clients
        sort_num_clients = list(set(tmp_num_clients))

        # creation d'une liste de clients
        clients = []
        for i in range(len(sort_num_clients)):
            c = Client(sort_num_clients[i])
            clients.append(c)

        # ajout des produits aux clients
        for line in file:  # creation des variables des produits
            try:
                num_c = line.split(' ')[0]
                num_p = line.split(' ')[1]
                qte = line.split(' ')[2]
                pri = line.split(' ')[3]
                tax = line.split(' ')[4]
            except IndexError:
                tax = " "

            for client in clients:
                if num_c == client.getNumero():
                    p = Produit(num_p, qte, pri, tax)
                    client.ajouterProduit(p)

        return clients
