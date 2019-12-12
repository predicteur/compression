# Objectifs de la compression
Compression de données pour des séries temporelles (ex envoi sur réseau LPWAN)

1 - Remplacement d'un ensemble de points codés sur 16 bits (ex. entier) ou 32 bits (ex.réel) en un ensemble réduit de points et codés sur un nombre de bits réduits.

Exemple : 16 points réels (64 octets) compressés en 12 octets

2 - Utilisation d'algorithmes facilement implémentables sur des micro-controleurs.

Exemple : utilisation de Sigfox (limitation à 140 messages par jour et 12 octets par message).
-> avec une mesure toutes les 15 secondes, on peut envoyer 32 valeurs toutes les 8 minutes sur 12 octets
# Principes de compression
La compression s'effectue par un envoi de paramètres permettant de reconstruire une séquence de plusieurs valeurs (séquence de 32 valeurs dans l'exemple ci-dessus). 

Les paramètres sont issus de plusieurs estimations par régression polynomiale et sont ensuite codés sur un nombre de bits défini ([voir compression de courbe](https://fr.wikipedia.org/wiki/Compression_de_courbe)).

L'erreur de compression (écart-type entre les valeurs de départ et les valeurs reconstruites) est également intégrée à la compression.
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
    * decompressYp()        : valeurs des paramètres issus de la régression (Compactor uniquement)
    * decompressEcartType() : écart-type des valeurs simulées / valeurs d'origine
# Principe de la compression simple (classe : Compactor)
## Etape 1 : Normalisation
Mise à une échelle de \[-0,5  0,5\] des valeurs de la séquence à partir des seuils mini, maxi imposés ou libres.
## Etape 2 : Régression
Calcul des p paramètres du polynome représentant la séquence.

Un paramètre supplémentaire est calculé pour représenter la performance de la compression (y compris les écarts liés au codage) : l'écart-type entre les points initiaux et les points estimés.
## Étape 3 : Codage des paramètres 
Les paramètres ( points + écart-type) sont codés sur le nombre de bits défini.

Le résultat est un tableau de bit (qui peut ensuite être converti en variables de longueur donnée).
# Principe de la compression avancée (classe : Compressor)
Une deuxième méthode combinant deux niveaux de régression est implémentée. Elle permet notamment de s'affranchir des limites mini/maxi qui pénalisent le codage :

1 - Réalisation d'une première régression sur la séquence fournie.

2 - Réalisation d'une deuxième série de régressions sur des sous-séquences constituée des écarts entre les valeurs initiales et celles issues de la première régression. Les points de la deuxième régression sont codés dans l'enveloppe \[-2 * écart-type, 2 * écart-type\] ce qui permet de réduire le nombre de bits de codage nécessaire.

*Exemple d'une séquence de 32 points* : On effectue une première régression avec un point (moyenne). Pour les 32 écarts à la moyenne, on effectue 4 régressions (polynomiales sur 3 points) sur les 4 sous-séquences de 8 points. On a donc représenté nos 32 points initiaux par 1 + 4 * 3 points. Le codage des 4 * 3 points peut se faire sur un nombre de bits faible (codage sur la plage de 4 écart-type), par exemple 3 ou 4 alors que le codage du point de moyenne ou de l'écart-type initial doit se faire en fonction de la plage mini-maxi définie.

Cette compression avancée s'appuie sur la classe de compression simple.
# Principe de mise en oeuvre de la décompression
La décompression consiste à calculer les valeurs à partir des paramètres codés avec les étapes inverses à celles de la compression :
## Etape 1 : Décodage des paramètres
Reconstitution des valeurs réelles à partir de la valeur codée.
## Etape 2 : Décompression
Reconstitution des valeurs estimées à partir des paramètres du polynome.
## Etape 3 : Dénormalisation
Mise à l'échelle des estimations à partir des seuils mini/maxi définis
## Etape 4 : Ecart-type
Reconstitution de l'indicateur de compression (écart-type).
# Algorithmes utilisés
[voir compression de courbe](https://fr.wikipedia.org/wiki/Compression_de_courbe)
# Utilisation
Voir les exemples donnés sur les deux types de régressions.
