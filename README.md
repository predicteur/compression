# Compression
compression de données pour envoi sur réseau LPWAN
# Objectifs
Envoi de données issues d'un capteur en utilisant un nombre d'octets limités.
Exemple : utilisation de Sigfox avec limitation à 140 messages par jour et 12 octets par message.
-> avec une mesure toutes les 15 secondes, cela revient à envoyer 32 valeurs toutes les 8 minutes sur 12 octets
# Principes
Traitement de séquence de plusieurs valeurs :
## Etape 1 : Normalisation
Mise à une échelle de \[0, 1\] des mesures de la séquence avec application éventuelle d'une fonction exponentielle à partir des seuils mini, maxi autorisés.
## Etape 2 : Régression linéaire globale
Première estimation globale des valeurs de la séquence par régression linéaire. La séquence est alors représentée sous la forme de trois paramètres : les deux premiers sont les coefficients a et b de la droite (y = a * x + b) minimisant l'écart quadratique entre les points de mesure et la droite. Le troisième paramètre est l'écart-type entre les mesures et l'estimation ainsi réalisée.
## Etape 3 : Régression linéaire complémentaire
Une deuxième régression linéaire est effectuée pour valeurs correspondantes à l’écart entre la valeur réelle et la première estimation. Cette deuxième régression est effectuée par tranche de la séquence. Pour chaque tranche deux paramètres sont mémorisés (coefficient de la droite).
## Étape 4 : Codage des paramètres 
Les paramètres ( 3 + 2 * nb_tranches) sont codés sur un nombre de bits choisis à partir de valeurs mini/maxi définies (mini/maxi des mesures pour la 1ère régression et en fonction des écart-types liés à la première estimation.
Par exemple pour une séquence de 32 mesures découpées en 8 tranches et codées sur 8 bits pour la première régression et en 4 bits pour la seconde, on aura la séquence codée sur 11 octets ( 3 * 8 bits + 2 * 8 * 4 bits)
## Étape 5 : Optimisation
Ajustement des paramètres par recalcul des paramètres « b » issus des valeurs décodées de « a ».
## Étape 6 : écart-type
Ajout et codage d’un dernier paramètre correspondant à l’ecaet-type global.
