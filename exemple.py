
"""
Created on Sun Aug 11 22:10:43 2019

test sur une serie complete

140 messages par jour 
12 octets par message

5mn -> 11,6 heures
6mn -> 14 heures
8mn -> 18 heures
10mn -> 23,3 heures

15 secondes -> 20 pour 5mn, 24 pour 6 mn, 32 pour 8 mn, 40 pour 10 mn
1 interpol pour  -> 1,25mn,   1,5 mn    ,   2 mn       ,     2,5 mn

test effectué pour 18h / j soit un envoi de 32 valeurs toutes les 8 minutes
"""
import csv
import json

from compression import compress, decompress
from series import et, diff, moy


# parametres compression
ecret = 2 # coef d'écrétage des écarts pour la régression initiale ex. 2 (coef multiplié à l'écart-type)
nbreg = 8 # nombre de régression de niveau 1 ex. 8
racine = 1 # fonction de normalisation des données (données ** racine) ex. racine = 0.5
mini = 0.0 # plage mini et maxi des mesures prise en compte (écrétage sinon)
maxi = 700.0 # plage mini et maxi des mesures prise en compte (écrétage sinon) ex. 700.0
# parametres codage
pla = 10.0 # plage pour les coefficients a de niveau 1 : abs(a) < pla * ecart-type ex. 10.0
plb = 3.0 # plage pour les coefficients b de niveau 1 : abs(b) < plb * ecart-type ex. 3.0
bit = 8 # nb de bits pour les coeff de niveau 0 ex. 8
bitc = 4 # nb de bits pour les coeff de niveau 1 ex. 4
taillepay = 8 # nb de messages qui composent le payload

taille_ech = 32 # nombre de mesures d'un échantillon à coder ex. 32
totalOctet = (4*bit + nbreg * 2 * bitc)/8
totalPointParRegression =  taille_ech//nbreg

chemin = "C:\\Users\\a179227\\OneDrive - RENAULT\\perso Wx\\AiForGood\\test_mesures"
data = chemin+'\\data06-08.json'
res = chemin+'\\compression06-08.txt'

with open(data) as json_data:
    data_dict = json.load(json_data)
with open(res, 'w', newline='') as csvfile:
    fieldnames = ['PM25', 'PM25_codé']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    pm25 =[]
    pm25_estim = []

    for x in data_dict:
        if (x['device'] == 'sensor7') :
            pm25.append(float(x['PM2_5']))
    print(pm25[0:30])
    
    nb_ech = len(pm25)//taille_ech
    for i in range(nb_ech):
        y0 = pm25[i*taille_ech:(i+1)*taille_ech]
    
        payload = compress(y0, ecret, nbreg, racine, mini, maxi, pla, plb, bit, bitc, taillepay)
        (y0fo, ecartType) = decompress(payload, taille_ech, nbreg, racine, mini, maxi, pla, plb, bit, bitc, taillepay)

        #print('et final et estimé', et(diff(y0, y0fo)), ecartType)
        for i in range(len(y0)):
            writer.writerow({'PM25':y0[i], 'PM25_codé':y0fo[i]})
        pm25_estim += y0fo
    
    erreur_type = et(diff(pm25, pm25_estim))
    biais = moy(pm25) - moy(pm25_estim)
    print(' Total octet : ', totalOctet, ' Moyenne : ', moy(pm25))
    print('erreur type global: ', erreur_type, ' biais: ', biais, ' moyenne: ', moy(pm25_estim))
