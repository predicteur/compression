
"""
Created on Sun Aug 11 21:49:49 2019

Fonctions liées à l'algorithme de compression d'une série de données

"""

from series2 import regx, estim, et, diff, conversion, conversionb, \
                    normalisation, denormalisation, codage, decodage
from comp_or import Comp_or

class Compactor(Comp_or):
    
    def __init__(self, nbreg0 = 4, mini = 0, maxi = 50, bit = 8, bitEct = 8, tailleEch = 32):
        self.nbreg0 = nbreg0
        self.bit = bit
        self.yp0 = [] # paramètres normalisés
        bits = nbreg0 * bit + bitEct
        Comp_or.__init__(self, mini, maxi, bits, bitEct, tailleEch)
        
        
    def check(self):
        resultat = Comp_or.check(self)
        if (self.nbreg0 > self.tailleEch) : resultat = "nombre de points de la compression supérieur à celui de l'échantillon"
        if (self.nbreg0 < 1) : resultat = "nombre de points doit être supérieur à 1"
        if (self.bit < 1): resultat = " nombre de bits insuffisant"
        return resultat

    def calcul(self, y0, codec=True):
        if (self.check() != "ok") : return self.check()
        self.y0 = y0
        self.yp0 = []
        print("y0 :", y0 )
        print(self.mini, self.maxi, self.tailleEch, self.nbreg0)
        yp = regx(normalisation(y0, self.mini, self.maxi), self.tailleEch, self.nbreg0)
        print('yp : ', yp)
        if (codec) :            
            for i in range(self.nbreg0):
                self.yp0.append(conversionb(conversion(yp[i], -0.5, 0.5, self.bit), -0.5, 0.5, self.bit))
        else: self.yp0 = yp
        self.yr0 = denormalisation(estim(self.yp0, self.tailleEch, self.nbreg0), self.mini, self.maxi)
        self.calculKo = False        
        self.payl = self.compressYp() + self.compressEct()
        return "ok"

    def param(self):
        if self.calculKo : return []
        return self.yp0

    def compressYp(self):
        if self.calculKo : return []
        self.paylYp = codage(self.yp0, self.nbreg0, self.bit)
        return self.paylYp
    
# fonctions à utiliser uniquement en mode récepteur
    def decompressYp(self, payl): 
        return decodage(payl[0 : self.bits - self.bitEct], self.nbreg0, self.bit)

    def decompressY0(self, payl): 
        return denormalisation(estim(self.decompressYp(payl), self.tailleEch, self.nbreg0), self.mini, self.maxi)

