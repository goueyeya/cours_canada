class Produit:
    def __init__(self, numero, quantite, prixunitaire, tax):
        self.numero = numero
        self.quantite = quantite
        self.prixunitaire = prixunitaire
        self.tax = tax
        self.total = 0

    def getNumero(self):
        return self.numero

    def getQuantite(self):
        return self.quantite

    def getPrixUnitaire(self):
        return self.prixunitaire

    def setTotal(self, total):
        self.total = total

    def getTotal(self):
        if self.tax == "F\n":
            self.setTotal(round((float(self.prixunitaire) + float(self.prixunitaire) * 5 / 100) * float(self.quantite), 2))
        elif self.tax == "P\n":
            self.setTotal(round((float(self.prixunitaire) + float(self.prixunitaire) * 9.975 / 100) * float(self.quantite), 2))
        elif self.tax == "FP\n":
            self.setTotal(round((float(self.prixunitaire) + float(self.prixunitaire) * 14.975 / 100) * float(self.quantite), 2))
        else:
            self.setTotal(round((float(self.prixunitaire) * int(self.quantite)), 2))
        return self.total

    def getTax(self):
        return self.tax
