# Compression
compression de données pour des séries temporelles (ex envoi sur réseau LPWAN)

# Objectifs
1 - Remplacement d'un ensemble de points codés sur 16 bits (ex. entier) ou 32 bits (ex.réel) en un ensemble réduit de points et codés sur un nombre de bits réduits.
Exemple : 16 points réels (64 octets) compressés en 14 octets

2 - Implémentation avec des algorithmes facilement implémentables sur des micro-controleurs.
Exemple : utilisation de Sigfox (imitation à 140 messages par jour et 12 octets par messag).
-> avec une mesure toutes les 15 secondes, cela revient à envoyer 32 valeurs toutes les 8 minutes sur 12 octets

# Principes de compression
La compression s'effectue par un envoi de paramètres permettant de reconstruire une séquence de plusieurs valeurs (séquence de 32 valeurs dans l'exemple ci-dessus). Les paramètres sont issus de plusieurs estimations par régression polynomiale et sont ensuite codés sur un nombre de bits défini.
L'erreur de compression (écart-type entre les valeurs de départ et les valeurs reconstruites) est également intégrée à la compression.
# Principe de la régression polynomiale
Une séquence de n points est représentée sous la forme de p points appartenant à une courbe : y = a0 + a1 * x + a2 * x2 + a3 * x3 + .. + a(p-1) * x(p-1) obtenue en minimisant l'écart quadratique entre les valeurs à compresser et celles de la courbe. Les p coefficients (a0, ... a(p-1)) ou p points de la courbe suffisent à reconstruire les n points de départ (voir https://fr.wikipedia.org/wiki/R%C3%A9gression_polynomiale).
L'obtention des p points s'effectue par calcul matriciel (produit + inversion de matrice). La reconstruction des n points à partir des p points s'obtient également par calcul mtriciel (produit uniquement).
## Etape 1 : Normalisation
Mise à une échelle de \[0, 1\] des valeurs de la séquence à partir des seuils mini, maxi imposés ou libres.
## Etape 2 : Régression polynomiale principale
Première estimation globale des valeurs de la séquence par régression linéaire.  Un paramètre supplémentaire est l'écart-type entre les mesures et l'estimation ainsi réalisée.
## Etape 3 : Régression polynomiale complémentaire
Une deuxième régression linéaire est effectuée pour valeurs correspondantes à l’écart entre la valeur réelle et la première estimation. Cette deuxième régression est effectuée par tranche de la séquence. Pour chaque tranche deux paramètres sont mémorisés (coefficient de la droite).
## Étape 4 : Codage des paramètres 
Les paramètres ( 3 + 2 * nb_tranches) sont codés sur un nombre fixés de bits à partir de valeurs mini/maxi définies (mini/maxi des mesures pour la 1ère régression et mini/maxi liés aux écart-types de la première estimation.
Par exemple pour une séquence de 32 mesures découpées en 8 tranches et codées sur 8 bits pour la première régression et en 4 bits pour la seconde, on aura la séquence codée sur 11 octets ( 3 * 8 bits + 2 * 8 * 4 bits)
## Étape 5 : Optimisation
Ajustement des paramètres par recalcul des paramètres « b » optimaux associés aux paramètres « a » après codage / décodage.
## Étape 6 : écart-type
Ajout et codage d’un dernier paramètre correspondant à l’ecart-type global.

# Principes de décompression
La décompression consiste à calculer les valeurs à partir des paramètres codés avec les étapes inverses à celles de la compression :
## Etape 1 : Décodage des paramètres
Reconstitution des valeurs réelles à partir des valeurs mini/maxi et de la valeur codée.
## Etape 2 : Décompression
Reconstitution des valeurs principales issues de la première régression (équation linéaire) ajoutées aux valeurs complémentaires issues de la deuxième régression.
## Etape 3 : Dénormalisation
Mise à l'échelle des mesures à partir des seuils mini/maxi définis

# Algorithmes utilisés
## Régression linéaire
Minimisation de l'erreur quadratique pour une estimation par y = a * x + b :
- a optimal : (somme (xi) * somme (yi) - n * somme (xi * yi)) / (somme (xi) * somme (xi) - n * somme(xi * xi))
- b optimal : somme (yi) / n - a * somme (xi) / n
## Optimisation
Calcul du b optimal pour a fixé :
- b optimal : somme (yi) / n - a * somme (xi) / n
## codage
Utilisation d'une échelle linéaire pour transformer une valeur en un nombre codé sur plusieurs bits : 

  valBit - MinBit = (MaxBit - MinBit) / (MaxRéel - MinRéel) * (ValRéel - MinRéel)

