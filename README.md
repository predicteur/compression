# Compression
compression de données pour envoi sur réseau LPWAN
# Objectifs
Envoi de données issues d'un capteur en utilisant un nombre d'octets limités et avec des alogorithmes facilement implémentables sur des micro-controleurs.
Exemple : utilisation de Sigfox avec limitation à 140 messages par jour et 12 octets par message.
-> avec une mesure toutes les 15 secondes, cela revient à envoyer 32 valeurs toutes les 8 minutes sur 12 octets
# Principes de compression
La compression s'effectue par un envoi de paramètres permettant de reconstruire une séquence de plusieurs valeurs (séquence de 32 valeurs dans l'exemple ci-dessus). Les paramètres sont issus de plsuieurs estimations par régression linéaire.
## Etape 1 : Normalisation
Mise à une échelle de \[0, 1\] des valeurs de la séquence avec application éventuelle d'une fonction exponentielle à partir des seuils mini, maxi autorisés.
## Etape 2 : Régression linéaire principale
Première estimation globale des valeurs de la séquence par régression linéaire. La séquence est alors représentée sous la forme de trois paramètres : les deux premiers sont les coefficients a et b de la droite (y = a * x + b) minimisant l'écart quadratique entre les valeurs et la droite. Le troisième paramètre est l'écart-type entre les mesures et l'estimation ainsi réalisée.
## Etape 3 : Régression linéaire complémentaire
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
Minimisation de l'erreur quadratique :
- a optimal : (somme (xi) * somme (yi) - n * somme (xi * yi)) / (somme (xi) * somme (xi) - n * somme(xi * xi))
- b optimal : somme (yi) / n - a * somme (xi) / n
## Optimisation
Calcul du b optimal pour a fixé :
- b optimal : somme (yi) / n - a * somme (xi) / n
## codage
