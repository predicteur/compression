
"""
Created on Sun Aug 11 21:49:49 2019

Fonctions liées à l'algorithme de compression d'une série de données

"""

from series2 import et, diff, normalisation, denormalisation, codage, decodage

class Comp_or:
    
    def __init__(self, mini = 0, maxi = 50, bits = 32, bitEct = 8, tailleEch = 32):
        # parametres normalistion
        self.mini = mini      # plage mini et maxi des mesures prise en compte (écrétage sinon)
        self.maxi = maxi      # plage mini et maxi des mesures prise en compte (écrétage sinon)
        # paramètres echantillon
        self.tailleEch = tailleEch # nombre de valeurs à compresser
        # paramètres internes
        self.y0 = [] # valeurs à compresser
        self.yr0 = [] # résultat non normalisé
        self.bitEct = bitEct  # nb de bits pour l'écart-type ex. 8
        self.bits = bits
        self.calculKo = True
        # paramètres codage
        self.payl = [] # payload global
        self.paylEct = [] # payload écart-type
        self.paylYp = [] # payload global sans écart-type
        
    def taillePayload(self):       
        return self.bits
        
    def check(self):
        resultat = "ok"
        if (self.mini > self.maxi): resultat = " seuils mini - maxi incohérents"
        if (self.bitEct < 1): resultat = " nombre de bits insuffisant"
        if (self.bits < self.bitEct): resultat = " nombre de bits incohérents"
        return resultat

    def simul(self):
        if self.calculKo : return []
        return self.yr0

    def ecartTypeSimul(self, codec=True):
        if self.calculKo : return 0.0
        ect = [et(diff(self.y0, self.simul()))]
        print("ect[0] : ", ect)
        if codec :
            ectPayl = codage(normalisation(ect, self.mini, self.maxi), 1, self.bitEct)
            ect = denormalisation(decodage(ectPayl, 1, self.bitEct), self.mini, self.maxi)
        return ect[0]

    def compressEct(self):
        if self.calculKo : return []
        self.paylEct = codage(normalisation([self.ecartTypeSimul(False)], self.mini, self.maxi), 1, self.bitEct)
        return self.paylEct

    def compress(self):
        if self.calculKo : return []
        self.payl = self.paylYp + self.paylEct
        print("payl : ", self.payl)
        return self.payl

# fonctions à utiliser uniquement en mode récepteur

    def decompressEct(self, payl): 
        return denormalisation(decodage(payl[self.bits - self.bitEct : self.bits], 1, self.bitEct), self.mini, self.maxi)[0]

