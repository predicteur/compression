# Compression
Compression de données pour des séries temporelles (ex envoi sur réseau LPWAN)

# Objectifs
1 - Remplacement d'un ensemble de points codés sur 16 bits (ex. entier) ou 32 bits (ex.réel) en un ensemble réduit de points et codés sur un nombre de bits réduits.
Exemple : 16 points réels (64 octets) compressés en 14 octets

2 - Utilisation d'algorithmes facilement implémentables sur des micro-controleurs.
Exemple : utilisation de Sigfox (imitation à 140 messages par jour et 12 octets par messag).
-> avec une mesure toutes les 15 secondes, on peut envoyer 32 valeurs toutes les 8 minutes sur 12 octets

# Principes de compression
La compression s'effectue par un envoi de paramètres permettant de reconstruire une séquence de plusieurs valeurs (séquence de 32 valeurs dans l'exemple ci-dessus). 

Les paramètres sont issus de plusieurs estimations par régression polynomiale et sont ensuite codés sur un nombre de bits défini.

L'erreur de compression (écart-type entre les valeurs de départ et les valeurs reconstruites) est également intégrée à la compression.
# Principe de la régression polynomiale
Une séquence de n points est représentée par une courbe polynomiale : y = a0 + a1 * x + a2 * x*\*2 + a3 * x*\*3 + .. + a(p-1) * x*\*(p-1). 

Les paramètres du polynome sont obtenus en minimisant l'écart quadratique entre les valeurs à compresser et celles de la courbe. 

Les p coefficients de la courbe suffisent à reconstruire les n points de départ.

L'obtention des p points s'effectue par calcul matriciel (produit + inversion de matrice). La reconstruction des n points à partir des p points s'obtient également par calcul matriciel (produit uniquement).
* Lorsque p = 1, la courbe est constante -> la séquence est représentée par sa moyenne
* Lorsque p = 2, la courbe est une droite -> on obtient une régression linéaire
* Lorsque p = n, la courbe passe par tous les points -> la compression s'effectue uniquement sur le codage. 
# Principe de mise en oeuvre de la compression simple (classe : Compactor)
## Etape 1 : Normalisation
Mise à une échelle de \[-0,5  0,5\] des valeurs de la séquence à partir des seuils mini, maxi imposés ou libres.
## Etape 2 : Régression
Calcul des p paramètres du polynome représentant la séquence.

Un paramètre supplémentaire est calculé pour représenter la performance de la compression (y compris les écarts liés au codage) : l'écart-type entre les points initiaux et les points estimés.
## Étape 3 : Codage des paramètres 
Les paramètres ( points + écart-type) sont codés sur le nombre de bits défini.

Le résultat est un tableau de bit (qui peut ensuite être converti en variables de longueur donnée).
# Principe de mise en oeuvre de la décompression simple (classe : Compactor)
La décompression consiste à calculer les valeurs à partir des paramètres codés avec les étapes inverses à celles de la compression :
## Etape 1 : Décodage des paramètres
Reconstitution des valeurs réelles à partir de la valeur codée.
## Etape 2 : Décompression
Reconstitution des valeurs initiales à partir du polynome.
## Etape 3 : Dénormalisation
Mise à l'échelle des estimations à partir des seuils mini/maxi définis
## Etape 4 : Ecart-type
Reconstitution de l'indicateur de compression (écart-type).
# Principe de mise en oeuvre de la compression avancée (classe : Compressor)
Une deuxième méthode combinant deux niveaux de régression est implémentée :

1 - Réalisation d'une première régression sur la séquence fournie.

2 - Réalisation d'une deuxième série de régressions sur des sous-séquences constituée des écarts entre les valeurs initiales et celles issues de la première régression. 

*Exemple d'une séquence de 32 points* : On effectue une première régression avec deux points (linéaire). Pour les 32 écarts résiduels, on effectue 4 régressions (linéaire de 2 points) sur les 4 sous-séquences de 8 points. On a donc représenté nos 32 points initiaux par 2 + 4 * 2 points.

Cette compression avancée s'appuie sur la classe de compression simple.

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
Plutôt que d'utiliser pour la compression le paramètre P, on utilise le paramètre Yp qui correspond aux valeurs de p points équi-répartis sur la séquence : Yp = Xp * inv(S) * T.

Pour la décompression, on reconstitue les valeurs Yn à partir du paramètre Yp : Yn = Xn * inv(Xp) * Yp (Yn : dimension n, Xn : dimension n x p, Xp : dimension p x p, Yp : dimension p)



## codage
Utilisation d'une échelle linéaire pour transformer une valeur en un nombre codé sur plusieurs bits : 
    
    valBit =  MinBit + (MaxBit - MinBit) / (MaxRéel - MinRéel) * (ValRéel - MinRéel)


# Utilisation
