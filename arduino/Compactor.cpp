//#include "stdafx.h"
#include "Compactor.h"

using namespace std;

Compactor::Compactor(const int nbreg0, const float mini, const float maxi, const int bitc, const int bitEct, const int tailleEch) : Comp_or(mini, maxi, bitEct, bitEct, tailleEch) {
	NBREG0 = nbreg0;
	BIT = bitc;
	BITS = nbreg0 * bitc + bitEct;
	delete payl, paylYp;
	payl = new int[BITS];
	paylYp = new int[BITS - bitEct];
	yp0 = new float[nbreg0];					// param�tres non normalis�
}
Compactor::~Compactor() {
	delete yp0;
}
String Compactor::check(){
	String resultat = Comp_or::check();
	if (NBREG0 > TAILLE_ECH)	resultat = "nombre de points de la compression sup�rieur � celui de l'�chantillon";
	if (NBREG0 < 1)				    resultat = "nombre de points doit �tre sup�rieur � 1";
	if (BIT < 1)				      resultat = "nombre de bits insuffisant";
	return resultat;
}
String Compactor::calcul(float* y, bool codec){
	float* yp = new float[NBREG0];
	if (check() != "ok")  return check();
	y0i = copie(y, TAILLE_ECH);
	//cout << " y0 : "; for (int i = 0; i<TAILLE_ECH; i++) cout << y0[i] << ", "; cout << endl;
	//cout << " param : " << MINI << MAXI << TAILLE_ECH << NBREG0 << endl;
	yp = regx(normalisation(y0i, MINI, MAXI, TAILLE_ECH), TAILLE_ECH, NBREG0);
	//cout << " yp : "; for (int i = 0; i<NBREG0; i++) cout << yp[i] << ", "; cout << endl;
	if (codec) for (int i = 0; i < NBREG0; i++) yp0[i] = conversionb(conversion(yp[i], -0.5, 0.5, BIT), -0.5, 0.5, BIT);
	else yp0 = copie(yp, NBREG0);
	yr0 = denormalisation(estim(yp0, TAILLE_ECH, NBREG0), MINI, MAXI, TAILLE_ECH);
	//cout << " yr0 : "; for (int i = 0; i<TAILLE_ECH; i++) cout << yr0[i] << ", "; cout << endl;
	calculKo = false;
	payl = ajoute(compressYp(), NBREG0, compressEct(), 1);
	delete yp;
	return "ok";
}
float* Compactor::param(){
	float* ptr(0); if (calculKo) return ptr;
  delete ptr;
	return yp0;
}
int* Compactor::compressYp(){
	int* ptr(0); if (calculKo) return ptr;
	paylYp = codage(yp0, NBREG0, BIT);
  delete ptr;
	return paylYp;
}
int* Compactor::compress(){
	return 0;
}

// fonctions � utiliser uniquement en mode r�cepteur
float* Compactor::decompressYp(int* payload){
	return decodage(sousSerieInt(payload, 0, BITS - BITECT), NBREG0, BIT);
}
float* Compactor::decompressY0(int* payload){
	return denormalisation(estim(decompressYp(payload), TAILLE_ECH, NBREG0), MINI, MAXI, TAILLE_ECH);
}
