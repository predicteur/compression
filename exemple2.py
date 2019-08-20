
"""
test de compression sur une serie
"""

from compression import compress, decompress
from series import pr

nbreg = 4
ecret = 10
mini = 0
maxi = 100
racine = 0.5
bit = 8
bitc = 4
pla = 12
plb = 3
taillepay = 32

#y0 =[2, 3.5, 5, 15, 20, 12, 18, 2, 8, 3.5, 5, 15, 20, 10, 12, 18, 
#    2, 3.5, 5, 11, 20, 12, 18, 12, 8, 3.5, 5, 10, 2, 10, 12, 18]
#y0 =[2, 3.5, 5, 15, 20, 12, 18, 2]
#y0 =[100.0, 98.07, 92.38, 83.14, 70.71, 55.55, 38.26, 19.50]
y0 =[100.0, 92.38, 70.71, 38.26]
#y0 =[2, 3.5, 5, 15, 20, 12, 18, 2, 8, 3.5, 5, 15, 20, 10, 12, 18]

'''y0n = normalisation(y0, mini, maxi, racine)
coefc  = compression(y0n, nbreg, ecret)
coefi = codage(coefc, len(y0), bit, bitc, pla, plb, nbreg)
coefp = decodage(coefi, len(y0), bit, bitc, pla, plb, nbreg)        
coefc  = optimisation(coefp, y0n, nbreg)
print(coefc)
# calcul de l'écart-type final
coefi = codage(coefc,len(y0), bit, bitc, pla, plb, nbreg)  
payload = codbin(coefi, bit, bitc, nbreg, taillepay)
coefi = decodbin(payload, bit, bitc, nbreg, taillepay)
coefp = decodage(coefi, len(y0), bit, bitc, pla, plb, nbreg)
y0fon = decompression(coefp, len(y0), nbreg)
y0fo  = denormalisation(y0fon, mini, maxi, racine)
ecartType = et(diff(y0, y0fo))'''

payload = compress(y0, ecret, nbreg, racine, mini, maxi, pla, plb, bit, bitc, taillepay)
(y0fo, ect) = decompress(payload, len(y0), nbreg, racine, mini, maxi, pla, plb, bit, bitc, taillepay)
print(payload)
print(pr(y0fo))
print(ect)
