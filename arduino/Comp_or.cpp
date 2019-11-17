//#include "stdafx.h"
#include "Comp_or.h"
#include "series.h"

using namespace std;

Comp_or::Comp_or(float mini,  float maxi,  int bits,  int bitEct,  int tailleEch)
{
		// parametres normalistion
	MINI = mini;					//plage mini et maxi des mesures prise en compte(�cr�tage sinon)
	MAXI = maxi;					//plage mini et maxi des mesures prise en compte(�cr�tage sinon)
	// param�tres echantillon
	TAILLE_ECH = tailleEch;				//nombre de valeurs � compresser
	// param�tres internes
	BITS = bits;
	BITECT = bitEct;					// nb de bits pour l'�cart-type ex. 8
	y0i = new float[tailleEch];					// valeurs � compresser
	yr0 = new float[tailleEch];					// r�sultat non normalis�
	calculKo = true;
	// param�tres codage
	payl = new int[bits];
	paylEct = new int[bitEct];
	paylYp = new int[bits - bitEct];
}


Comp_or::~Comp_or()
{
	delete y0i, yr0, payl, paylEct, paylYp;
}

int Comp_or::taillePayload() {
	return BITS;
}	
String Comp_or::check() {
	String resultat = "ok";
	//cout << MINI << MAXI << BITECT << BITS << endl;
	if (MINI > MAXI)	resultat = " seuils mini - maxi incoh�rents";
	if (BITECT < 1)		resultat = " nombre de bits insuffisant";
	if (BITS < BITECT)resultat = " nombre de bits incoh�rents";
	return resultat;
}
float* Comp_or::simul() { 
	float* ptr(0); if (calculKo) return ptr;
	return yr0;
}
float Comp_or::ecartTypeSimul(bool codec) {
	float* ect = new float[1];
	float* ects = new float[1];
	if (calculKo) return 0;
	ect[0] = et(diff(y0i, simul(), TAILLE_ECH), TAILLE_ECH);
	if (codec) ects = denormalisation(decodage(codage(normalisation(ect, MINI, MAXI, 1), 1, BITECT), 1, BITECT), MINI, MAXI, 1);
	else ects = copie(ect, 1);
	delete ect;
	return ects[0];
}
int* Comp_or::compressEct() {
	float* ect = new float[1];
	int* ptr(0); if (calculKo) return ptr;
	ect[0] = ecartTypeSimul(false);
	paylEct = codage(normalisation(ect, MINI, MAXI, 1), 1, BITECT);
  delete ect, ptr;
	return paylEct;
}
int* Comp_or::compress() {
	int* ptr(0); if (calculKo) return ptr;
	payl = ajoute(paylYp, BITS - BITECT, paylEct, BITECT);
	return payl;
}
//# fonctions � utiliser uniquement en mode r�cepteur
float Comp_or::decompressEct(int* payl) {
	return denormalisation(decodage(sousSerieInt(payl, BITS - BITECT, BITECT), 1, BITECT), MINI, MAXI, 1)[0];
}
