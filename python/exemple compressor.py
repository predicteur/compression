
"""
test de compression sur une serie
"""
import numpy as np
import matplotlib.pyplot as plt
from series2 import diff, et
import compressor as comp
#from compression import normalisation, denormalisation
'''from compression import compress, decompress'''
#from series import pr

# parametres normalistion
mini = 0.0 # plage mini et maxi des mesures prise en compte (écrétage sinon)
maxi = 50.0 # plage mini et maxi des mesures prise en compte (écrétage sinon)
# parametres compression
nbreg = 8 # nombre de régression de niveau 1 ex. 8, 0 si aucune
nbreg0 = 2 # nombre de points de la regression de niveau 0 (entre 2 et 10)
nbreg1 = 2 # nombre de points de la regression de niveau 1 (entre 2 et 10)
# parametres codage
bit0 = 4 # nb de bits pour les coeff de niveau 0 ex. 8
bit1 = 4 # nb de bits pour les coeff de niveau 1 ex. 4
bitEct = 8 # nb de bits pour l'écart-type ex. 8

totalBits =  nbreg0 * bit0 + nbreg * nbreg1 * bit1 + 2 * bitEct # longueur totale

'''y0 =[2, 3.5, 5, 15, 20, 12, 18, 2, 8, 3.5, 5, 15, 20, 10, 12, 18, 
     2, 3.5, 5, 11, 20, 12, 18, 12, 8, 3.5, 5, 10, 2, 10, 12, 18]
'''
#y0 =[2, 3.5, 5, 15, 20, 12, 18, 2]
#y0 =[100.0, 98.07, 92.38, 83.14, 70.71, 55.55, 38.26, 19.50]
#y0 =[100.0, 92.38, 70.71, 38.26]
y0 =[2, 3.5, 5, 15, 20, 12, 18, 2, 8, 3.5, 5, 15, 20, 10, 12, 18]
'''y0 = [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0,
      19.8, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 
      19.0, 19.0, 19.0, 19.0, 19.0, 19.0 ]
'''
'''#exemple 1 : estimation unique, un seul point (moyenne)
nbreg = 0
nbreg0 = 1
bit0 = 3
combo  = comp.Compressor(nbreg, nbreg0, nbreg1, mini, maxi, bit0, bit1, bitEct, len(y0))
print('1 bits : ', combo.taillePayload(), ' taux : ', combo.taillePayload()/len(y0))
res = combo.calcul(y0, True)
y2 = combo.simul()
ectc = combo.ecartTypeSimul(False)
print('ectc : ', ectc, combo.decompressEct(combo.compress()) )
print(combo.decompressY0(combo.compress()))
'''
'''
#exemple 2 : estimation unique, deux points (régression linéaire)
nbreg = 0
nbreg0 = 2
combo  = comp.Compressor(nbreg, nbreg0, nbreg1, mini, maxi, bit0, bit1, bitEct, len(y0))
print('2 bits : ', combo.taillePayload(), ' taux : ', combo.taillePayload()/len(y0))
res = combo.calcul(y0, True)
y2 = combo.simul()
ectc = combo.ecartTypeSimul(False)
print('ectc : ', ectc, combo.decompressEct(combo.compress()) )
print(combo.decompressY0(combo.compress()))

#exemple 3 : estimation unique, cinq points (régression polynomiale)
nbreg = 0
nbreg0 = 4
bit0 = 5
combo  = comp.Compressor(nbreg, nbreg0, nbreg1, mini, maxi, bit0, bit1, bitEct, len(y0))
print('3 bits : ', combo.taillePayload(), ' taux : ', combo.taillePayload()/len(y0))
res = combo.calcul(y0, True)
y2 = combo.simul()
ectc = combo.ecartTypeSimul(False)
print('ectc : ', ectc, combo.decompressEct(combo.compress()) )
print(combo.decompressY0(combo.compress()))

#exemple 4 : estimation unique, seize points (codage de chaque point)
nbreg = 16
nbreg0 = 0
nbreg1 = 1
bit1 = 3
combo  = comp.Compressor(nbreg, nbreg0, nbreg1, mini, maxi, bit0, bit1, bitEct, len(y0))
print('4 bits : ', combo.taillePayload(), ' taux : ', combo.taillePayload()/len(y0))
res = combo.calcul(y0, True)
print(y0)
print(res)
y2 = combo.simul()
print(y2)

ectc = combo.ecartTypeSimul(False)
print('ectc : ', ectc, combo.decompressEct(combo.compress()) )
print(combo.decompressY0(combo.compress()))

#exemple 5 : estimation mixte, deux points (linéaire) puis quatre linéaire 
nbreg = 4
nbreg0 = 2
nbreg1 = 2
combo  = comp.Compressor(nbreg, nbreg0, nbreg1, mini, maxi, bit0, bit1, bitEct, len(y0))
print('5 bits : ', combo.taillePayload(), ' taux : ', combo.taillePayload()/len(y0))
res = combo.calcul(y0, True)
y2 = combo.simul()
ectc = combo.ecartTypeSimul(False)
print('ectc : ', ectc, combo.decompressEct(combo.compress()) )
print('yr0 : ',combo.decompressY0(combo.compress()))

#exemple 6 : estimation mixte, trois points (poly) puis quatre poly 
nbreg = 4
nbreg0 = 1
nbreg1 = 3
bit1 = 2
bit0 = 3
combo  = comp.Compressor(nbreg, nbreg0, nbreg1, mini, maxi, bit0, bit1, bitEct, len(y0))
print('6 bits : ', combo.taillePayload(), ' taux : ', combo.taillePayload()/len(y0))
res = combo.calcul(y0, True)
y2 = combo.simul()
ectc = combo.ecartTypeSimul(False)
print('ectc : ', ectc, combo.decompressEct(combo.compress()) )
print(combo.decompressY0(combo.compress()))

#exemple 7 : estimation mixte, trois points (poly) puis quatre poly 
nbreg = 8
nbreg0 = 1
nbreg1 = 2
bit1 = 2
bit0 = 3
combo  = comp.Compressor(nbreg, nbreg0, nbreg1, mini, maxi, bit0, bit1, bitEct, len(y0))
print('7 bits : ', combo.taillePayload(), ' taux : ', combo.taillePayload()/len(y0))
res = combo.calcul(y0, True)
y2 = combo.simul()
ectc = combo.ecartTypeSimul(False)
print('ectc : ', ectc, combo.decompressEct(combo.compress()) )
print(combo.decompressY0(combo.compress()))

#exemple 8 : estimation mixte, trois points (poly) puis quatre poly 
nbreg = 16
nbreg0 = 1
nbreg1 = 1
bit1 = 2
bit0 = 3
combo  = comp.Compressor(nbreg, nbreg0, nbreg1, mini, maxi, bit0, bit1, bitEct, len(y0))
print('8 bits : ', combo.taillePayload(), ' taux : ', combo.taillePayload()/len(y0))
res = combo.calcul(y0, True)
y2 = combo.simul()
ectc = combo.ecartTypeSimul(False)
print('ectc : ', ectc, combo.decompressEct(combo.compress()) )
print(combo.decompressY0(combo.compress()))

#exemple 9 : estimation mixte, trois points (poly) puis quatre poly 
nbreg = 4
nbreg0 = 1
nbreg1 = 2
bit1 = 2
bit0 = 3
combo  = comp.Compressor(nbreg, nbreg0, nbreg1, mini, maxi, bit0, bit1, bitEct, len(y0))
print('9 bits : ', combo.taillePayload(), ' taux : ', combo.taillePayload()/len(y0))
res = combo.calcul(y0, True)
y2 = combo.simul()
ectc = combo.ecartTypeSimul(False)
print('ectc : ', ectc, combo.decompressEct(combo.compress()) )
print(combo.decompressY0(combo.compress()))
'''
#exemple 10 : estimation mixte, trois points (poly) puis quatre poly 
nbreg = 8
nbreg0 = 1
nbreg1 = 2
bit1 = 2
bit0 = 3
combo  = comp.Compressor(nbreg, nbreg0, nbreg1, mini, maxi, bit0, bit1, bitEct, len(y0))
print('10 bits : ', combo.taillePayload(), ' taux : ', combo.taillePayload()/len(y0))
res = combo.calcul(y0, True)
y2 = combo.simul()
ectc = combo.ecartTypeSimul(False)
print('ectc : ', ectc, combo.decompressEct(combo.compress()) )
print(combo.decompressY0(combo.compress()))
'''
'''
'''
#exemple 1 : estimation unique, un seul point
nbreg = 4
nbreg0 = 2
combo  = comp.compressor(nbreg, nbreg0, nbreg1, mini, maxi, bit0, bit1, bitEct, len(y0))
print('bits : ', combo.taillePayload())
res = combo.calcul(y0, True)
if (res != "ok") : print(res)
y2 = combo.simul()
ectc = combo.ecartTypeSimul(False)
print('ectc : ', ectc)
print('y2 : ',y2)
payl = combo.compress()
print('payl :', payl)
yr = combo.decompressY0(payl)
ect = combo.decompressEct(payl)
print('ect : ', ectc, ect)
print('y : ',y2, yr)
print('total bits : ', combo.taillePayload(), totalBits)
'''
ectc2 = et(diff(y0, y2))

y3 = diff(y0, y2)
x = np.linspace(0, len(y0)-1, len(y0))
if (len(y0) >0) : plt.plot(x, y0, color='black')
if (len(y2) >0) : plt.plot(x, y2, color='red')
plt.show() 
#if (len(y3) >0) : plt.plot(x, y3, color='red')
#plt.show() 
