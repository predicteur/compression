# Objectifs de la compression
Compression de données pour des séries temporelles (ex envoi sur réseau LPWAN)

1 - Remplacement d'un ensemble de points codés sur 16 bits (ex. entier) ou 32 bits (ex.réel) en un ensemble réduit de points et codés sur un nombre de bits réduits.
Exemple : 16 points réels (64 octets) compressés en 12 octets

2 - Utilisation d'algorithmes facilement implémentables sur des micro-controleurs.
Exemple : utilisation de Sigfox (limitation à 140 messages par jour et 12 octets par message).
-> avec une mesure toutes les 15 secondes, on peut envoyer 32 valeurs toutes les 8 minutes sur 12 octets
# Principes de compression
La compression s'effectue par un envoi de paramètres permettant de reconstruire une séquence de plusieurs valeurs (séquence de 32 valeurs dans l'exemple ci-dessus). 

Les paramètres sont issus de plusieurs estimations par régression polynomiale et sont ensuite codés sur un nombre de bits défini.

L'erreur de compression (écart-type entre les valeurs de départ et les valeurs reconstruites) est également intégrée à la compression.
# Principe de la régression polynomiale
Une séquence de n points est représentée par une courbe polynomiale : y = a0 + a1 * x + a2 * x*\*2 + a3 * x*\*3 + .. + a(p-1) * x*\*(p-1). 

Les paramètres du polynome sont obtenus en minimisant l'écart quadratique entre les valeurs à compresser et celles de la courbe. 

Les p coefficients de la courbe suffisent à reconstruire les n points de départ.

L'obtention des p points s'effectue par calcul matriciel (produit + inversion de matrice). La reconstruction des n points à partir des p points s'obtient également par calcul matriciel (produit + inversion de matrice également).
* Lorsque p = 1, la courbe est constante -> la séquence est représentée par sa moyenne
* Lorsque p = 2, la courbe est une droite -> on obtient une régression linéaire
* Lorsque p = n, la courbe passe par tous les points -> la compression s'effectue uniquement sur le codage. 
# Mise en oeuvre
Deux types d'algorithmes sont mis en place (classe : Compactor et classe : Compressor), ils présentent les fonctions suivantes :
* fonctions indépendantes d'un jeu de données : 
    * check()               : vérification des paramètres d'entrée
    * taillePayload()       : nombre de bits des données compressées
    * precisionCodage()     : précision du codage utilisé
* fonctions liées au jeu de données : 
    * calcul()              : génération des principales sorties
    * simul()               : valeurs simulées après compression / décompression (utilisable après calcul)
    * ecartTypeSimul()      : écart-type des valeurs simulées / valeurs d'origine - fonction (utilisable après calcul)
    * compress()            : valeurs compressées (utilisable après calcul)
* fonctions liées à la décompression d'un jeu de données :
    * decompressY0()        : valeurs reconstituées par la décompression
    * decompressEcartType() : écart-type des valeurs simulées / valeurs d'origine
# Principe de mise en oeuvre de la compression simple \s\s (classe : Compactor)
## Etape 1 : Normalisation
Mise à une échelle de \[-0,5  0,5\] des valeurs de la séquence à partir des seuils mini, maxi imposés ou libres.
## Etape 2 : Régression
Calcul des p paramètres du polynome représentant la séquence.

Un paramètre supplémentaire est calculé pour représenter la performance de la compression (y compris les écarts liés au codage) : l'écart-type entre les points initiaux et les points estimés.
## Étape 3 : Codage des paramètres 
Les paramètres ( points + écart-type) sont codés sur le nombre de bits défini.

Le résultat est un tableau de bit (qui peut ensuite être converti en variables de longueur donnée).
# Principe de mise en oeuvre de la compression avancée \s\s (classe : Compressor)
Une deuxième méthode combinant deux niveaux de régression est implémentée :

1 - Réalisation d'une première régression sur la séquence fournie.

2 - Réalisation d'une deuxième série de régressions sur des sous-séquences constituée des écarts entre les valeurs initiales et celles issues de la première régression. Les points de la deuxième régression sont codés dans l'enveloppe de la moyenne de l'écart +/- deux écart-type, ce qui permet de réduire le nombre de bits de codage nécessaire.

*Exemple d'une séquence de 32 points* : On effectue une première régression avec un point (moyenne). Pour les 32 écarts à la moyenne, on effectue 4 régressions (polynomiales sur 3 points) sur les 4 sous-séquences de 8 points. On a donc représenté nos 32 points initiaux par 1 + 4 * 3 points. Le codage des 4 * 3 points peut se faire sur un nombre de bits faible en fonction de la plage de 4 écart-type (3 ou 4) alors que le codage du point de moyenne ou de l'écart-type initial doiot se faire en fonction de la plage mini-maxi définie

Cette compression avancée s'appuie sur la classe de compression simple.
# Principe de mise en oeuvre de la décompression
La décompression consiste à calculer les valeurs à partir des paramètres codés avec les étapes inverses à celles de la compression :
## Etape 1 : Décodage des paramètres
Reconstitution des valeurs réelles à partir de la valeur codée.
## Etape 2 : Décompression
Reconstitution des valeurs initiales à partir du polynome.
## Etape 3 : Dénormalisation
Mise à l'échelle des estimations à partir des seuils mini/maxi définis
## Etape 4 : Ecart-type
Reconstitution de l'indicateur de compression (écart-type).
# Algorithmes utilisés
## Régression polynomiale
*Notations* : 
* Séquence : pour les instants successifs x0, x1, ... , xn-1 les valeurs sont : Yn =(y0, y1, ... , yn-1) (valeurs correspondantes)
* Polynome : y = a0 * x\*\*0 + a1 * x*\*1 + ... + ap-1 * x*\*(p-1) = X * P avec X = (x*\*0, ... , x*\*(p-1)) et P = (a0, ... , ap-1)

La solution P qui minimise l'écart avec la séquence fournie est donnée par : S * P = T [voir Wikipedia](https://fr.wikipedia.org/wiki/R%C3%A9gression_polynomiale) avec :
    
    S matrice de dimension p x p : S[i, j] = SOM(i+j)   avec SOM(j) = somme(xi ** j) de i = 0 à n-1
    T matrice de dimension p     : T[i]    = somme(yi * xi ** j) de i = 0 à n-1
La matrice P s'obtient donc par P = inv(S) * T

Les points de la courbe (xp(i), yp(i)) vérifient l'équation : Yp = Xp * P avec :

    Yp matrice de dimension p     : Yp = (yp(1), yp(2), ... , yp(p-1))
    XP matrice de dimension p x p : Xp[i, j] = xp(i)**j
Plutôt que d'utiliser pour la compression le paramètre P, on utilise le paramètre Yp qui correspond aux valeurs de p points équi-répartis sur la séquence : 

    Yp = Xp * inv(S) * T     (dimensions : Xn : p x p, S : p x p, T :  p)
Pour la décompression, on reconstitue les valeurs Yn à partir du paramètre Yp : 

    Yn = Xn * inv(Xp) * Yp   (dimensions : Yn : n, Xn : n x p, Xp : p x p, Yp :  p)
## codage
Utilisation d'une échelle linéaire pour transformer une valeur en un nombre codé sur plusieurs bits : 
    
    valBit =  MinBit + (MaxBit - MinBit) / (MaxRéel - MinRéel) * (ValRéel - MinRéel)
La précision du codage est donné par :
    
    précision = (MaxRéel - MinRéel) / (2**bit - 1)
    ex. si Max = 1000, Min = 0, bit = 4 --> précision = 66,7
Dans le cas de la compression avancée, la deuxième régression s'effectue sur un intervalle entre -2 * écart-type et 2 * écart-type, la précision de cette deuxième régression est donc de : écart-type / (2**(bit-2)-0,25)

# Utilisation
Voir les exemples donnés sur les deux types de régressions.
