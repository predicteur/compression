# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 21:49:49 2019

@author: a179227
"""

def pr(serie) :
    stri ='[ '
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

