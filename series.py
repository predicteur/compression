# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 21:49:49 2019

fonctions de traitement des series 

"""

def pr(serie, nom = 'serie') :
    stri = nom +' : [ '
    for x in serie:
        stri += "{:6.3f} ".format(x)
    stri +=']'
    return stri

def estim(a, b, taille) :
    return [a*(i+1)+b for i in range(taille)]

def ecart(a, b, serie) :
    return [serie[i] - a*(i+1) - b for i in range(len(serie))]

def add(serie1, serie2) :
    return [serie1[i] + serie2[i] for i in range(min(len(serie1), len(serie2)))]

def diff(serie1, serie2) :
    return [serie1[i] - serie2[i] for i in range(min(len(serie1), len(serie2)))]

def et(ecart) :
    return (sum(ec**2 for ec in ecart)/len(ecart))**0.5

def moy(serie) :
    return sum(se for se in serie)/len(serie)

def ecretage(serie, mini, maxi) :
    return [min(maxi, max(mini, val)) for val in serie]

def addbin(param, payl, long) :
    for i in range(long):
        payl.append(param%2)
        param //= 2
    return

def decbin(payl, long, rang) :
    param = 0    
    for j in range(long):
        param += payl[rang+j]*2**j
    return param

def conversion(valeur, mini, maxi, bits, nom) :
    minib = 0
    maxib = 2**bits-1
    val = minib + round((maxib - minib) * (valeur - mini) / (maxi - mini))
    #if (val>maxib) : print("saturation : ", nom, valeur, mini, maxi)
    return max(minib, min(maxib, val))

def conversionb(valeurb, mini, maxi, bits) :
    minib = 0
    maxib = 2**bits-1
    return mini + (maxi - mini) * float(valeurb - minib) / float(maxib - minib)