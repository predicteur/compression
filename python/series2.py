# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 21:49:49 2019

fonctions de traitement des series 

"""
import numpy as np

def ec(ecart) :
    return (sum(abs(ec) for ec in ecart)/len(ecart))

def regx(serie, n, p) :
    s = [0.0 for i in range(2*p)]
    matX = np.zeros((p,p))
    matS = np.zeros((p,p))
    matT = np.zeros((p))
    print("serie ", serie)
    for j in range(2*p) :
        for i in range(n) :
            s[j] += i**j
    for j in range(p) :
        for i in range(n) :      
            matT[j] += serie[i] * i**j
    for i in range(p) :
        for j in range(p) :
            matS[i, j] = s[i+j]
    for i in range(p) :
        for j in range(p) :
            if (p==1) : matX[i,j] = float(1)
            else : matX[i,j] = float(((n-1)*(p-1-i)//(p-1))**j)
    #print("matX : ", matX)
    #print("matS : ", matS)
    return matX.dot(np.linalg.inv(matS).dot(matT)).tolist()

def estim(yp, n, p) :
    y1 = []
    if (p==0) : return y1
    l = []
    c = []
    for i in range(p) :
        for j in range(p) :
            if (p==1): l.append(float(1))
            else: l.append(float(((n-1)*(p-1-i)//(p-1))**j))
        c.append(l.copy())
        l.clear()
    Xn =np.array(c)
    Yn = np.array(yp)
    if (p==1): P = Yn / Xn[0,0]
    else: P = np.linalg.inv(Xn).dot(Yn)
    for i in range(n) :
        l = []
        for j in range(p) :
            l.append(i**j)
        x= np.array(l)
        y1.append(x.dot(P))
    return y1

def ecart(yp, serie) :
    return diff(serie, estim(yp, len(serie), len(yp)))

def pr(serie, nom = 'serie') :
    stri = nom +' : [ '
    for x in serie:
        stri += "{:6.3f} ".format(x)
    stri +=']'
    return stri

def add(serie1, serie2) :
    return [serie1[i] + serie2[i] for i in range(min(len(serie1), len(serie2)))]

def diff(serie1, serie2) :
    return [serie1[i] - serie2[i] for i in range(min(len(serie1), len(serie2)))]

def et(ecart) :
    if (len(ecart) < 1) : return -1
    return (sum(ec**2 for ec in ecart)/len(ecart))**0.5

def moy(serie) :
    return sum(se for se in serie)/len(serie)

def ecretage(serie, mini, maxi) :
    return [min(maxi, max(mini, val)) for val in serie]

def addbin(param, payl, long) :
    for i in range(long):
        payl.append(int(param%2))
        param //= 2
    return

def decbin(payl, long, rang) :
    param = 0    
    for j in range(long):
        param += payl[rang+j]*2**j
    return param

def conversion(valeur, mini, maxi, bits) :
    maxib = 2**bits-1
    val = round(maxib * (valeur - mini) / (maxi - mini))
    return max(0, min(maxib, val))

def conversionb(valeurb, mini, maxi, bits) :
    maxib = 2**bits-1
    return mini + (maxi - mini) * float(valeurb) / float(maxib)

def normalisation(serie, mini, maxi) :
    print("minmax :", mini, maxi)
    print("normalis :", [((min(maxi, max(mini, val))) - mini)/(maxi-mini) - 0.5 for val in serie])
    return [((min(maxi, max(mini, val))) - mini)/(maxi-mini) - 0.5 for val in serie]
    #return [(pow(val, c) - minic)/(maxic-minic) for val in serie]
    #return [(math.sqrt(val) - minic)/(maxic-minic) for val in serie]

def denormalisation(serie, mini, maxi) :
    return [min(maxi, max(mini, (mini+(maxi-mini)*(val + 0.5)))) for val in serie]
    #return [pow(minic+(maxic-minic)*val, 1.0/c) for val in serie]
    #return [pow(minic+(maxic-minic)*val, 2) for val in serie]

def codage(yp0, nbreg0, bit) :
    payl = []
    for i in range(nbreg0): addbin(conversion(yp0[i], -0.5, 0.5, bit), payl, bit)
    return payl

def decodage(payl, nbreg0, bit) :
    yp0 = []
    for i in range(nbreg0): yp0.append(conversionb(decbin(payl, bit, i * bit), -0.5, 0.5, bit))
    return yp0

#y0 =[2, 3.5, 5, 15, 20, 12, 18, 2, 8, 3.5, 5, 15, 20, 10, 12, 18, 
#     2, 3.5, 5, 11, 20, 12, 18, 12, 8, 3.5, 5, 10, 2, 10, 12, 18]

#y0 =[2, 3.5, 5, 15, 20, 12, 18, 2]
#y0 =[2, 3.5, 5, 15, 20, 12, 18, 2, 8, 3.5, 5, 15, 20, 10, 12, 18]
#y0 =[100.0, 98.07, 92.38, 83.14, 70.71, 55.55, 38.26, 19.50]
'''y0 = [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0,
      19.8, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 19.0, 
      19.0, 19.0, 19.0, 19.0, 19.0, 19.0 ]
'''
#from series import diff
"""p = 1
mini = 0.0
maxi = 50.0
c = 0.5
yn = normalisation(y0, mini, maxi)
yp = regx(yn, len(y0), p)
y1 = estim(yp, len(y0), p)
#ye = ecart(yp, y0)
#yn = normalisation(y0, mini, maxi, c)
yd = denormalisation(y1, mini, maxi)
print("yp : ", yp)
print("y0 : ", y1)
#print("ye : ", ye)
#print("yn : ", yn)
print("yd : ", yd)
#print(coef['ys'])
#print(estim3(coef['yp'], len(y0)))
"""

'''coef = reg5(y0)
n = len(y0)
y3 = []
Xn = np.array(([1, 0, 0, 0], [1, n-1, (n-1)**2, (n-1)**3], [1, n//3, (n//3)**2, (n//3)**3], [1, n*2//3, (n*2//3)**2, (n*2//3)**3]))
Yn = np.array(([coef['yd'], coef['yf'], coef['ym1'], coef['ym2']]))
P = np.linalg.inv(Xn).dot(Yn)
for i in range(len(y0)) :
    x= np.array(([1, i, i**2, i**3]))
    y3.append(x.dot(P))
print("ec5 : ", ec2(diff(y0, y3)), " et : ", et(diff(y0, y3)))

coef = reg4(y0)
n = len(y0)
y1 = []
Xn = np.array(([1, 0, 0], [1, n-1, (n-1)**2], [1, n/2, (n/2)**2]))
Yn = np.array(([coef['yd'], coef['yf'], coef['ym']]))
P = np.linalg.inv(Xn).dot(Yn)
for i in range(len(y0)) :
    x= np.array(([1, i, i**2]))
    y1.append(x.dot(P))
print("ec4 : ", ec2(diff(y0, y1)), " et : ", et(diff(y0, y1)))

coef = reg3(y0)
y2 =[]
Xn = np.array(([1, 0], [1, n-1]))
Yn = np.array(([coef['yd'], coef['yf']]))
P = np.linalg.inv(Xn).dot(Yn)
for i in range(len(y0)) :
    x= np.array(([1, i]))
    y2.append(x.dot(P))
print("ec3 : ", ec2(diff(y0, y2)), " et : ", et(diff(y0, y2)))

import matplotlib.pyplot as plt
x = np.linspace(0, len(y0)-1, len(y0))
plt.plot(x, y0, color='black')
plt.plot(y1, color='red')
plt.plot(y2, color='blue')
plt.plot(y3, color='green')
plt.plot(ys, color='purple')
plt.show() 
'''