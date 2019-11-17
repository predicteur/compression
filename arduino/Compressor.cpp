//#inclu	de "stdafx.h"
#include "Compressor.h"
#include "Compactor.h"
//#include <iostream>
//#include <ESP8266WiFi.h>

using namespace std;

Compressor::Compressor(const int nbreg, const int nbreg0, const int nbreg1, const float mini, const float maxi,
					   const int bit0, const int bit1, const int bitEct, const int tailleEch) : Comp_or(mini, maxi, bitEct, bitEct, tailleEch) {
	// parametres compression
	NBREG  = nbreg;
	NBREG0 = nbreg0;
	NBREG1 = nbreg1;
	// parametres codage
	BIT_0 = bit0;
	BIT_1 = bit1;
	if		  (nbreg0 < 1) BITS = nbreg  * nbreg1 * BIT_1 + bitEct;
	else if (nbreg  < 1) BITS = nbreg0 * BIT_0 + bitEct;
	else				         BITS = nbreg0 * BIT_0 + nbreg * nbreg1 * BIT_1 + 2 * bitEct;
	
	//cout << "compressor " << MAXI << " " << BITS << endl;
	//Comp_or(mini, maxi, BITS, bitEct, tailleEch);
	delete payl, paylYp;
	payl = new int[BITS];
	paylYp = new int[BITS - bitEct];

}
Compressor::~Compressor() {}
//-----------------------------------------------------------------------------------------------------------------------------
String Compressor::check(){
	String resultat = Comp_or::check();
	if (NBREG0 > TAILLE_ECH)						resultat = "nombre de points de la compression sup�rieur � celui de l'�chantillon";
	if (NBREG > 0) if (NBREG1 > TAILLE_ECH / NBREG)	resultat = "nombre de points de la compression sup�rieur � celui de l'�chantillon";
	if (BIT_0 < 1 or BIT_1 < 1)						resultat = "nombre de bits insuffisant";
	return resultat;
}
String Compressor::calcul(float* y, bool codec) {
	float* y0fo = new float[TAILLE_ECH];
	float* y1fo = new float[TAILLE_ECH];
	float* y1   = new float[TAILLE_ECH];
	int indPay = 0;
	float mini1 = MINI;
	float maxi1 = MAXI;
	if (check() != "ok")  return check();
	y0i = copie(y, TAILLE_ECH);
	for (int i = 0; i < TAILLE_ECH; i++) y0fo[i] = 0;
	// compression initiale
	if (NBREG0 > 0) {
		Compactor comp0(NBREG0, MINI, MAXI, BIT_0, BITECT, TAILLE_ECH);
		String res = comp0.calcul(y0i, codec);
		//if (res != "ok") cout << res;
		y0fo = comp0.simul();
		float ect0 = comp0.ecartTypeSimul(true);
		paylYp = comp0.compressYp();
		if (NBREG > 0) for (int i = 0; i < BITECT; i++) paylYp[NBREG0 * BIT_0 + i] = comp0.compressEct()[i];
		mini1 = -2 * ect0;
		maxi1 = 2 * ect0;
		indPay = NBREG0 * BIT_0 + BITECT;
	}
	//cout << " y0fo : "; for (int i = 0; i<TAILLE_ECH; i++) cout << y0fo[i] << ", "; cout << endl;
	// compression compl�mentaire
	y1 = diff(y0i, y0fo, TAILLE_ECH);
	//cout << " y1 : "; for (int i = 0; i<TAILLE_ECH; i++) cout << y1[i] << ", "; cout << endl;
	if (NBREG > 0) {
		int tailleEch2 = TAILLE_ECH / NBREG;
		Compactor comp1(NBREG1, mini1, maxi1, BIT_1, BITECT, tailleEch2);
		for (int i = 0; i < NBREG; i++) {
			String res = comp1.calcul(sousSerie(y1, tailleEch2 * i, tailleEch2), codec);
			//if (res != "ok") cout << res;
			for (int j = 0; j < tailleEch2   ; j++) y1fo  [tailleEch2 * i + j]             = comp1.simul()     [j];
			for (int j = 0; j < NBREG1 * BIT_1; j++) paylYp[indPay + NBREG1 * BIT_1 * i + j] = comp1.compressYp()[j];
		}
		indPay += NBREG1 * BIT_1 * NBREG;
	}
	// donnees de sortie
	if (NBREG > 0) yr0 = ecretage(adds(y0fo, y1fo, TAILLE_ECH), MINI, MAXI, TAILLE_ECH);
	else yr0 = copie(y0fo, TAILLE_ECH);
	calculKo = false;
	payl = ajoute(paylYp, indPay, compressEct(), BITECT);
	delete y0fo, y1fo, y1;
	return "ok";
}

// fonctions � utiliser uniquement en mode r�cepteur
float* Compressor::decompressY0(int* payl) {
	float* yr1 = new float[TAILLE_ECH];
	float* yr = new float[TAILLE_ECH];
	int indYp1 = 0;
	float ect0 = 0;
	float mini1 = MINI;
	float maxi1 = MAXI;
	for (int i = 0; i < TAILLE_ECH; i++) yr0[i] = 0;
	if (NBREG0 > 0) {
		indYp1 = NBREG0 * BIT_0 + BITECT;
		Compactor comp0(NBREG0, MINI, MAXI, BIT_0, BITECT, TAILLE_ECH);
		yr0  = comp0.decompressY0 (sousSerieInt(payl, 0, indYp1));
		ect0 = comp0.decompressEct(sousSerieInt(payl, 0, indYp1));
		mini1 = -2 * ect0;
		maxi1 =  2 * ect0;
		//cout << " yr0 (decompY0) : "; for (int i = 0; i<TAILLE_ECH; i++) cout << yr0[i] << ", "; cout << endl;
	}
	if (NBREG > 0) {
		int tailleEch2 = TAILLE_ECH / NBREG;
		Compactor comp1(NBREG1, mini1, maxi1, BIT_1, BITECT, tailleEch2);
		for (int i = 0; i < NBREG; i++) for (int j = 0; j < tailleEch2; j++)
			yr1[tailleEch2 * i + j] = comp1.decompressY0(sousSerieInt(payl, indYp1 + i * NBREG1 * BIT_1, NBREG1 * BIT_1 + BITECT))[j];
		yr = adds(yr0, yr1, TAILLE_ECH);
	}
	else yr = copie(yr0, TAILLE_ECH);
	delete yr1;
	return yr;
}
