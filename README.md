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
Une deuxième régression linéaire est effectuée 
 
