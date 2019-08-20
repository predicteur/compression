// test de compression de données sur Arduino (conversion programme python)

// parametres compression
const int   ECRET   = 10;       // coef d'écrétage des écarts pour la régression initiale ex. 2 (coef multiplié à l'écart-type)
const int   NBREG   = 8;        // nombre de régression de niveau 1 ex. 8
const float RACINE  = 0.5;      // fonction de normalisation des données (données ** racine) ex. racine = 0.5
const float MINI    = 0.0;      // plage mini et maxi des mesures prise en compte (écrétage sinon)
const float MAXI    = 50.0;     // plage mini et maxi des mesures prise en compte (écrétage sinon)
// parametres codage
const float PLA     = 12.0;     // plage pour les coefficients a de niveau 1 : abs(a) < pla * ecart-type ex. 10.0
const float PLB     = 3.0;      // plage pour les coefficients b de niveau 1 : abs(b) < plb * ecart-type ex. 3.0
const int   BITS    = 8;        // nb de bits pour les coeff de niveau 0 ex. 8
const int   BITC    = 4;        // nb de bits pour les coeff de niveau 1 ex. 4
// paramètres de l'échantillon
const int   TAILLE_ECH  = 32;                             // nombre de mesures d'un échantillon de la régression principale ex.32
const int   TAILLE_ECH2 = TAILLE_ECH / NBREG;             // nombre de mesures des échantillons de la régression complémentaire
// paramètres de l'envoi
const int   TAILLE_MSG  = 32;                             // nombre de bit des messages composant le "payload" (3 messages pour un payload Sigfox de 12 octets)
const int   TAILLE_PAY  = 96;                             // nombre de bit du "payload" (Sigfox 12 octets)
const int   TOTAL_BIT   = (4 * BITS + NBREG * 2 * BITC);  // nombre de bit à envoyer

struct CoefReg {
  float   a;   // coef a régression linéaire y = a * x + b
  float   b;   // coef b régression linéaire y = a * x + b
  float   ect; // écart-type entre la valeut y et l'estimation y = a x + b
} coef = {0.0, 0.0, 0.0};                                 // paramètre de chaque régression unitaire

struct CoefComp {
  float   a0;         // coef a régression linéaire principale
  float   b0;         // coef b régression linéaire principale
  float   et0;        // écart-type entre la valeut y et l'estimation principale
  float   a1[NBREG];  // coef a régression linéaire secondaire
  float   b1[NBREG];  // coef b régression linéaire secondaire
  float   ect;        // écart-type global entre la valeut y et l'estimation complète
} coefc = {0.0, 0.0, 0.0, {}, {}, 0.0},  coefp = {0.0, 0.0, 0.0, {}, {}, 0.0};    // coefc : paramètres issue de la compression ou de l'optimisation, coefp : paramètres issus du decodage

struct CoefCode {
  int   a0;         // coef a régression linéaire principale
  int   b0;         // coef b régression linéaire principale
  int   et0;        // écart-type entre la valeut y et l'estimation principale
  int   a1[NBREG];  // coef a régression linéaire secondaire
  int   b1[NBREG];  // coef b régression linéaire secondaire
  int   ect;        // écart-type global entre la valeut y et l'estimation complète
} coefi = {0, 0, 0.0, {}, {}, 0.0};                       // paramètres issus du codage

/*typedef struct __attribute__ ((packed)) sigfox_message {
  uint32_t msg1;
  uint32_t msg2;
  uint32_t msg3;
} SigfoxMessage;
SigfoxMessage payload;*/

struct sigfox_message {
  uint32_t msg1;
  uint32_t msg2;
  uint32_t msg3;
} payload = {0, 0, 0};


float /*y0init[TAILLE_ECH],*/ y0n[TAILLE_ECH], y0fon[TAILLE_ECH];

float y0init[TAILLE_ECH] = {2, 3.5, 5, 15, 20, 12, 18, 2, 8, 3.5, 5, 15, 20, 10, 12, 18, 2, 3.5, 5, 11, 20, 12, 18, 12, 8, 3.5, 5, 10, 2, 10, 12, 18};

void setup() {
  float ecartType;
  // liaison série
  Serial.begin(115200);     // Start the Serial communication to send messages to the computer
  delay(10);
  Serial.println('\n');
  
  compress();
  ecartType = decompress();
  prSerie(y0fon, TAILLE_ECH, "y0fon");
  Serial.print("ecart-type : "); Serial.println(ecartType);
}

void loop() {
  // put your main code here, to run repeatedly:

}
