
"""
test de compression sur une serie
"""
import numpy as np
import matplotlib.pyplot as plt
from series2 import add, diff, et, normalisation
import compactor as comp
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
bit = 3 # nb de bits pour les coeff de niveau 0 ex. 8
bitc = 3 # nb de bits pour les coeff de niveau 1 ex. 4
bitEct = 4 # nb de bits pour l'écart-type ex. 8

bits = (nbreg0 + 1) * bit + nbreg * nbreg1 * bitc # 4*8 + 8*2*4 = 96 

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
ect=ect2=ect3=ect4=ect5=0
#y0n = normalisation(y0, mini, maxi)

comp0  = comp.compactor(nbreg0, mini, maxi, bit, bitEct, len(y0))
res = comp0.calcul(y0, True)
if (res != "ok") : print(res)
y0fo = comp0.simul()
ectc = comp0.ecartTypeSimul(False)
payl = comp0.compressYp()
payl += comp0.compressEct()
print('ect : ', ectc, comp0.decompressEct(comp0.compressEct())[0], comp0.ecartTypeSimul(True))

y1 = diff(y0, y0fo)
min1 = -2*ectc
max1 = 2*ectc
y1fo = []
comp1 = comp.compactor(nbreg1 , min1, max1, bitc, bitEct, len(y0)//nbreg)
for i in range(nbreg):
     res = comp1.calcul(y1[len(y1)*i//nbreg:len(y1)*(i+1)//nbreg], True)
     if (res != "ok") : print(res)
     y1fo += comp1.simul()
     payl += comp1.compressYp()
y2 = add(y0fo, y1fo)
ectc2 = et(diff(y0, y2))
payl += comp0.compressEct()

y3 = diff(y0, y2)
print('bits : ', bits)
print('ect : ', ectc, ectc2, ect2, ect3, ect4, ect5)
print('y2 : ', y2)
#print(y0foc)
#print(y0fo2)

x = np.linspace(0, len(y0)-1, len(y0))
if (len(y0) >0) : plt.plot(x, y0, color='black')
if (len(y0fo) >0) : plt.plot(x, y0fo, color='red')
if (len(y2) >0) : plt.plot(x, y2, color='blue')
plt.show() 
'''if (len(y1) >0) : plt.plot(x, y1, color='black')
if (len(y1fo) >0) : plt.plot(x, y1fo, color='red')
plt.show() 
#if (len(y3) >0) : plt.plot(x, y3, color='red')
#plt.show() 
'''