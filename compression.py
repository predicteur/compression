
"""
Created on Sun Aug 11 21:49:49 2019

Fonctions liées à l'algorithme de compression d'une série de données

"""

from series import estim, ecart, add, et, ecretage, diff, conversion, \
                   conversionb, addbin, decbin

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
    minic = mini**c
    maxic = maxi**c
    return [((min(maxi, max(mini, val)))**c - minic)/(maxic-minic) for val in serie]

def denormalisation(serie, mini, maxi, c) :
    minic = mini**c
    maxic = maxi**c
    return [min(maxi, max(mini, (minic+(maxic-minic)*val)**(1.0/c))) for val in serie]

def codage(coef, leny0, bit, bitc, pla, plb, nbreg) :
    coefc = {'a0':0, 'b0':0, 'a1':[], 'b1':[], 'et0':0, 'et':0}
    et0 = coef['et0']
    coefc['a0']  = conversion(coef['a0'] , -1.0/float(leny0), 1.0/float(leny0), bit, 'a0')
    coefc['b0']  = conversion(coef['b0'] , 0                 , 2.0              , bit, 'b0')
    coefc['et0'] = conversion(coef['et0'], 0                 , 0.5              , bit, 'et0')
    coefc['et']  = conversion(coef['et'] , 0                 , 0.5              , bit, 'et')
    for i in range(nbreg):
        coefc['a1'].append(conversion(coef['a1'][i], -pla*et0/leny0*2.0, pla*et0/leny0*2.0, bitc, 'a1'+str(i)))
        coefc['b1'].append(conversion(coef['b1'][i], -plb*et0         , plb*et0         , bitc, 'b1'+str(i)))
    return coefc

def decodage(coefc, leny0, bit, bitc, pla, plb, nbreg) :
    coef = {'a0':0, 'b0':0, 'a1':[], 'b1':[], 'et0':0, 'et':0}
    coef['a0'] = conversionb(coefc['a0'] , -1.0/float(leny0), 1.0/float(leny0), bit)
    coef['b0'] = conversionb(coefc['b0'] , 0                 , 2.0              , bit)
    coef['et0']= conversionb(coefc['et0'], 0                 , 0.5              , bit)
    coef['et'] = conversionb(coefc['et'] , 0                 , 0.5              , bit)
    for i in range(nbreg):
        coef['a1'].append(conversionb(coefc['a1'][i], -pla*coef['et0']/leny0*2.0, pla*coef['et0']/leny0*2.0, bitc))
        coef['b1'].append(conversionb(coefc['b1'][i], -plb*coef['et0']         , plb*coef['et0']         , bitc))
    return coef

def codbin(coef, bit, bitc, nbreg, taillepay) :
    bits = 4 * bit + nbreg * 2 * bitc
    nbpay = bits // taillepay + (bits % 8 > 0)
    mespay = 0
    payl = []
    payload = []
    addbin(coef['a0'],  payl, bit)
    addbin(coef['b0'],  payl, bit)
    addbin(coef['et0'], payl, bit)
    addbin(coef['et'],  payl, bit)
    for i in range(nbreg):
        addbin(coef['a1'][i], payl, bitc)
        addbin(coef['b1'][i], payl, bitc)
    for i in range(nbpay*taillepay-bits): payl.append(0)
    for i in range(nbpay):
        mespay = decbin(payl, taillepay, i*taillepay)
        payload.append(mespay)
    return payload

def decodbin(payload, bit, bitc, nbreg, taillepay) :
    payl = []
    coef = {'a0':0, 'b0':0, 'a1':[], 'b1':[], 'et0':0, 'et':0}
    for param in payload:
        addbin(param, payl, taillepay)
    coef['a0']  = decbin(payl, bit, 0)
    coef['b0']  = decbin(payl, bit, 1*bit)
    coef['et0'] = decbin(payl, bit, 2*bit)
    coef['et']  = decbin(payl, bit, 3*bit)
    for i in range(nbreg):
        coef['a1'].append(decbin(payl, bitc, 4*bit+(i*2  )*bitc))
        coef['b1'].append(decbin(payl, bitc, 4*bit+(i*2+1)*bitc))
    return coef

def compression(y0, nbreg, ecret) :
    coefc = {'a0':reg(y0)['a'], 'b0':reg(y0)['b'], 'a1':[], 'b1':[], 'et0':reg(y0)['et'], 'et':0}
    if (len(y0)%nbreg > 0) :
        print("taille échantillon incohérente")
        return coefc
    y1 = ecretage(ecart(coefc['a0'], coefc['b0'], y0), -ecret*coefc['et0'], ecret*coefc['et0'])
    for i in range(nbreg):
        coefc['a1'].append(reg(y1[len(y1)*i//nbreg:len(y1)*(i+1)//nbreg])['a'])
        coefc['b1'].append(reg(y1[len(y1)*i//nbreg:len(y1)*(i+1)//nbreg])['b'])
    return coefc

def decompression(coef, leny0, nbreg) :
    y1 = []
    for j in range(nbreg):
        y1 += estim(coef['a1'][j], coef['b1'][j], leny0//nbreg)
    return add(estim(coef['a0'], coef['b0'], leny0), y1)
    
def optimisation(coefp, y0, nbreg) :
    coefo = {'a0':coefp['a0'], 'b0':0, 'a1':coefp['a1'], 'b1':[], 'et0':0.0, 'et':coefp['et']}
    coefo['b0'] = rega(y0, coefp['a0'])
    y1 = ecart(coefo['a0'], coefo['b0'], y0)
    coefo['et0'] = et(y1)
    for i in range(nbreg):
        coefo['b1'].append(rega(y1[len(y1)*i//nbreg:len(y1)*(i+1)//nbreg], coefp['a1'][i]))
    return coefo

def compress(y0, ecret, nbreg, racine, mini, maxi, pla, plb, bit, bitc, taillepay):
    # compression et optimisation
    y0n = normalisation(y0, mini, maxi, racine)
    coefc  = compression(y0n, nbreg, ecret)
    coefi = codage(coefc, len(y0), bit, bitc, pla, plb, nbreg)
    coefp = decodage(coefi, len(y0), bit, bitc, pla, plb, nbreg)        
    coefc  = optimisation(coefp, y0n, nbreg)
    # calcul de l'écart-type final
    coefi = codage(coefc,len(y0), bit, bitc, pla, plb, nbreg)    
    coefp = decodage(coefi, len(y0), bit, bitc, pla, plb, nbreg)
    y0fon = decompression(coefp, len(y0), nbreg)
    y0fo  = denormalisation(y0fon, mini, maxi, racine)
    ecartType = et(diff(y0, y0fo))
    # codage et envoio des données
    coefc['et'] = normalisation([ecartType], mini, maxi, racine)[0]
    coefi = codage(coefc,len(y0), bit, bitc, pla, plb, nbreg)   
    return codbin(coefi, bit, bitc, nbreg, taillepay)

def decompress(payload, leny0, nbreg, racine, mini, maxi, pla, plb, bit, bitc, taillepay):
    coefi = decodbin(payload, bit, bitc, nbreg, taillepay)
    coefp = decodage(coefi, leny0, bit, bitc, pla, plb, nbreg)
    et = denormalisation([coefp['et']], mini, maxi, racine)[0]
    y0fon  = decompression(coefp, leny0, nbreg)
    y0fo   = denormalisation(y0fon, mini, maxi, racine)
    return (y0fo, et)
