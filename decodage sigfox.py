
"""
test de decodage d'un message sigfox
"""

from compression import decompress

def decSigfox(message):
    sigfox2 = ""
    payload = []
    for i in range(12):
        sigfox2 += message[(11-i)*2]
        sigfox2 += message[(11-i)*2+1]
    payload.append(int(sigfox2[16:24], 16))
    payload.append(int(sigfox2[8:16], 16))
    payload.append(int(sigfox2[0:8], 16))
    return payload


taille_ech = 4
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

# exemple
sigfox = "3f95174c58a8a858bffdffff"
''' résultat attendu :
payload : [1276613951, 1487448152, 4294966719]
0fo, ect : [100, 95.8095501730104, 72.650553633218, 40.409703960015385] 2.2206843521722415    
'''

payload = decSigfox(sigfox)
print(payload)
(y0fo, ect) = decompress(payload, taille_ech, nbreg, racine, mini, maxi, pla, plb, bit, bitc, taillepay)
print(y0fo, ect)

