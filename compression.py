# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 21:49:49 2019
@author: a179227

Fonctions liées à l'algorithme de compression d'une série de donées
"""

from series import estim, ecart, add, et, ecretage

def reg(serie) :
    sx = sy = sxy = sx2 = 0.0
    coef = {'a' : 0.0, 'b' : 0.0, 'et': 0.0}
    if (len(serie)==1):
        coef['b'] = serie[0]
        coef['a'] = 0.0
    elif (len(serie)==2):
        coef['b'] = 2.0 * serie[0] - serie[1]
        coef['a'] = serie[1]-serie[0]
    else :
        for i in range(len(serie)) :
            sx += (i+1)
            sy += serie[i]
            sxy += (i+1) * serie[i]
            sx2 += (i+1) * (i+1)
        coef['a'] = (sx * sy - len(serie) * sxy) / (sx * sx - len(serie) * sx2)
        coef['b'] = sy / len(serie) - coef['a'] * sx / len(serie)
    coef['et'] = et(ecart(coef['a'], coef['b'], serie))
    return coef

def rega(serie, a) :   # a fixé, calcul de b (b = moyenne(yi) - a * moyenne(xi))
    sx = sy = 0.0
    if (len(serie)==1):
        b = serie[0]
    else :
        for i in range(len(serie)) :
            sx += (i+1)
            sy += serie[i]
        b = sy / len(serie) - a * sx / len(serie)
    return b

def normalisation(serie, mini, maxi, c) :
    return [((min(maxi, max(mini, val)))**c - mini**c)/(maxi**c-mini**c) for val in serie]

def denormalisation(serie, mini, maxi, c) :
    return [min(maxi, max(mini,mini+(maxi-mini)*val**(1/c))) for val in serie]

def conversion(valeur, mini, maxi, bits, nom) :
    minib = 0
    maxib = 2**bits
    val = minib + round((maxib - minib) * (valeur - mini) / (maxi - mini))
    #if (val>maxib) : print("erreurb : ", nom, valeur, mini, maxi)
    return max(minib, min(maxib, val))

def conversionb(valeurb, mini, maxi, bits) :
    minib = 0
    maxib = 2**bits
    return mini + (maxi - mini) * float(valeurb - minib) / float(maxib - minib)

def codage(coef, nombre, bit, bitc, pla, plb, nbreg) :
    coefc = {'a0':0, 'b0':0, 'a1':[], 'b1':[], 'et0':0}
    coefc['a0']  = conversion(coef['a0'] , -1.0/float(nombre), 1.0/float(nombre), bit, 'a0')
    coefc['b0']  = conversion(coef['b0'] , 0                 , 2                , bit, 'b0')
    coefc['et0'] = conversion(coef['et0'], 0                 , 0.5              , bit, 'et0')
    et0 = coef['et0']
    for i in range(nbreg):
        coefc['a1'].append(conversion(coef['a1'][i], -pla*et0/nombre*2, pla*et0/nombre*2, bitc, 'a1'+str(i)))
        coefc['b1'].append(conversion(coef['b1'][i], -plb*et0         , plb*et0         , bitc, 'b1'+str(i)))
    return coefc

def decodage(coefc, nombre, bit, bitc, pla, plb, nbreg) :
    coef = {'a0':0, 'b0':0, 'a1':[], 'b1':[], 'et0':0,}
    coef['a0'] = conversionb(coefc['a0'] , -1.0/float(nombre), 1.0/float(nombre), bit)
    coef['b0'] = conversionb(coefc['b0'] , 0                 , 2                , bit)
    coef['et0']= conversionb(coefc['et0'], 0                 , 0.5              , bit)
    for i in range(nbreg):
        coef['a1'].append(conversionb(coefc['a1'][i], -pla*coef['et0']/nombre*2, pla*coef['et0']/nombre*2, bitc))
        coef['b1'].append(conversionb(coefc['b1'][i], -plb*coef['et0']         , plb*coef['et0']         , bitc))
    return coef

def decompression(coef, nombre, nbreg) :
    y1 = []
    for j in range(nbreg):
        y1 += estim(coef['a1'][j], coef['b1'][j], nombre//nbreg)
    return add(estim(coef['a0'], coef['b0'], nombre), y1)
    
def compression(y0, nbreg, ecret) :
    coef = {'a0':reg(y0)['a'], 'b0':reg(y0)['b'], 'a1':[], 'b1':[], 'et0':reg(y0)['et']}
    if (len(y0)%nbreg > 0) :
        print("taille échantillon incohérente")
        return coef
    y1 = ecretage(ecart(coef['a0'], coef['b0'], y0), -ecret*coef['et0'], ecret*coef['et0'])
    for i in range(nbreg):
        coef['a1'].append(reg(y1[len(y1)*i//nbreg:len(y1)*(i+1)//nbreg])['a'])
        coef['b1'].append(reg(y1[len(y1)*i//nbreg:len(y1)*(i+1)//nbreg])['b'])
    return coef

def optimisation(coefp, y0, nbreg) :
    coefo = {'a0':coefp['a0'], 'b0':0, 'a1':coefp['a1'], 'b1':[], 'et0':0.0}
    coefo['b0'] = rega(y0, coefp['a0'])
    y1 = ecart(coefo['a0'], coefo['b0'], y0)
    coefo['et0'] = et(y1)
    for i in range(nbreg):
        coefo['b1'].append(rega(y1[len(y1)*i//nbreg:len(y1)*(i+1)//nbreg], coefp['a1'][i]))
    return coefo

def compress(y0, ecret, nbreg, racine, mini, maxi, pla, plb, bit, bitc):
    coef = compression(normalisation(y0, mini, maxi, racine), nbreg, ecret)
    coefi =codage(coef,len(y0), bit, bitc, pla, plb, nbreg)
    coefp = decodage(coefi, len(y0), bit, bitc, pla, plb, nbreg)        
    coefo = optimisation(coefp, normalisation(y0, mini, maxi, racine), nbreg)
    coefio =codage(coefo,len(y0), bit, bitc, pla, plb, nbreg)
    return coefio

def decompress(coef, leny0, nbreg, racine, mini, maxi, pla, plb, bit, bitc):
    coefpo = decodage(coef, leny0, bit, bitc, pla, plb, nbreg)
    y0fo = denormalisation(decompression(coefpo, leny0, nbreg), mini, maxi, racine)
    return y0fo
