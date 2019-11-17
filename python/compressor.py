
"""
test de compression sur une serie
"""
from series2 import add, diff, ecretage
import compactor as comp
from comp_or import Comp_or

class Compressor(Comp_or):
    
    def __init__(self, nbreg = 8, nbreg0 = 4, nbreg1 = 4, mini = 0, maxi = 50, 
                 bit0 = 8, bit1 = 8, bitEct = 8, tailleEch = 32):
        # parametres compression
        self.nbreg  = nbreg   # nombre de régression de niveau 1 ex. 8, 0 si aucune
        self.nbreg0 = nbreg0  # nombre de points de la regression de niveau 0 (entre 2 et 10)
        self.nbreg1 = nbreg1  # nombre de points de la regression de niveau 1 (entre 2 et 10)
        # parametres codage
        self.bit0 = bit0      # nb de bits pour les coeff de niveau 0 ex. 8
        self.bit1 = bit1      # nb de bits pour les coeff de niveau 1 ex. 4
        if (nbreg0 < 1) : bits = nbreg * nbreg1 * bit1 + bitEct # longueur totale
        elif (nbreg < 1) : bits = nbreg0 * bit0 + bitEct # longueur totale
        else : bits = nbreg0 * bit0 + nbreg * nbreg1 * bit1 + 2 * bitEct # longueur totale
        Comp_or.__init__(self, mini, maxi, bits, bitEct, tailleEch)

   
    def check(self):
        resultat = Comp_or.check(self)
        if (self.nbreg0 > self.tailleEch) : resultat = "nombre de points de la compression supérieur à celui de l'échantillon"
        if (self.nbreg > 0) and (self.nbreg1 > self.tailleEch//self.nbreg) : resultat = "nombre de points de la compression supérieur à celui de l'échantillon"
        if (self.bit0 < 1 or self.bit1 < 1): resultat = " nombre de bits insuffisant"
        return resultat

    def calcul(self, y0, codec=True):
        if (self.check() != "ok") : return self.check()
        self.y0 = y0
        self.paylYp = []
        y0fo = [0 for i in range(len(y0))]
        mini1 = self.mini
        maxi1 = self.maxi
        y1fo = []
        # compression initiale
        if (self.nbreg0 > 0) :
            comp0  = comp.Compactor(self.nbreg0, self.mini, self.maxi, self.bit0, self.bitEct, len(y0))
            res = comp0.calcul(y0, codec)
            if (res != "ok") : print(res)
            y0fo = comp0.simul()
            ect0 = comp0.ecartTypeSimul(True)
            self.paylYp = comp0.compressYp()
            if (self.nbreg > 0) : self.paylYp += comp0.compressEct()
            mini1 = -2*ect0
            maxi1 =  2*ect0
        # compression complémentaire
        y1 = diff(y0, y0fo)
        if (self.nbreg > 0) :
            comp1 = comp.Compactor(self.nbreg1, mini1, maxi1, self.bit1, self.bitEct, len(y0)//self.nbreg)
            for i in range(self.nbreg):
                 res = comp1.calcul(y1[len(y1)*i//self.nbreg:len(y1)*(i+1)//self.nbreg], codec)
                 if (res != "ok") : print(res)
                 y1fo += comp1.simul()
                 self.paylYp += comp1.compressYp()
        # donnees de sortie
        if (self.nbreg > 0) : self.yr0 = ecretage(add(y0fo, y1fo), self.mini, self.maxi)
        else : self.yr0 = y0fo
        self.calculKo = False        
        self.payl = self.paylYp + self.compressEct()
        return "ok"

# fonctions à utiliser uniquement en mode récepteur
    def decompressY0(self, payl): 
        indYp1 = 0
        yr0 = [0 for i in range(self.tailleEch)]
        mini1 = self.mini
        maxi1 = self.maxi
        if (self.nbreg0 > 0) :
            indYp1 = self.nbreg0 * self.bit0 + self.bitEct 
            comp0  = comp.Compactor(self.nbreg0, self.mini, self.maxi, self.bit0, self.bitEct, self.tailleEch)
            yr0  = comp0.decompressY0 (payl[0 : indYp1])
            ect0 = comp0.decompressEct(payl[0 : indYp1])
            mini1 = -2*ect0
            maxi1 =  2*ect0
            print("yr0 (decompY0) : ", yr0)
        if (self.nbreg > 0) :
            yr1 = []
            print (self.nbreg1, mini1, maxi1, self.bit1, self.bitEct, self.tailleEch//self.nbreg)
            comp1 = comp.Compactor(self.nbreg1, mini1, maxi1, self.bit1, self.bitEct, self.tailleEch//self.nbreg)
            for i in range(self.nbreg):
                yr1 += comp1.decompressY0(payl[indYp1 + i * self.nbreg1 * self.bit1 : indYp1 + (i+1) * self.nbreg1 * self.bit1 + self.bitEct])
            print("yr1 (decompY0) : ", yr1)
            yr = add(yr0, yr1)
        else : yr = yr0
        return yr
     