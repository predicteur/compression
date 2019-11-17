//#include "stdafx.h"
#include "series.h"
//#include <cmath>
//#include <algorithm>
#include "MatrixMath.h"
//#include <iostream>

using namespace std;

float * regx(float* serie, int len, int p)
{
	double* s    = new double[2 * p];
	double* matX = new double[p*p];
	double* matS = new double[p*p];
	double* matP = new double[p*p];
	double* matT = new double[p];
	double* matY = new double[p];
	float*  yp   = new float[p];
	//cout << " serie : "; for (int i = 0; i<len; i++) cout << serie[i] << ", "; cout << endl;
	for (int j = 0; j < 2 * p; j++) {
		s[j] = 0.0;
		for (int i = 0; i < len; i++) s[j] += pow(i, j);
	}
	for (int j = 0; j < p; j++) {
		matT[j] = 0.0;
		for (int i = 0; i < len; i++) matT[j] += serie[i] * pow(i, j);
	}
	for (int i = 0; i < p; i++) for (int j = 0; j < p; j++) matS[j + i * p] = s[i + j];
	for (int i = 0; i < p; i++) for (int j = 0; j < p; j++) {
		if (p == 1) matX[j + i * p] = float(1);
		else matX[j + i * p] = float(pow((len - 1)*(p - 1 - i) / (p - 1), j));
	}
	int resOk = Matrix.Invert(matS, p);
	if (resOk == 0) return yp;
	Matrix.Multiply(matS, matT, p, p, 1, matP);
	Matrix.Multiply(matX, matP, p, p, 1, matY);
	for (int i = 0; i < p; i++) yp[i] = (float)matY[i];

	delete[] s, matX, matS, matP, matT, matY;
	return yp;
}

//-----------------------------------------------------------------------------------------------------------------------------
float* estim(float* yp, int len, int p) {
	float*  y1    = new float [len];
	double* Xn    = new double[p*p];
	double* Yn    = new double[p];
	double* matP  = new double[p];
	double* x     = new double[p*len];
	double* y     = new double[len];

	for (int i = 0; i < p; i++) for (int j = 0; j < p; j++) {
		if (p == 1) Xn[j + i * p] = float(1);
		else	Xn[j + i * p] = float(pow((len - 1)*(p - 1 - i) / (p - 1), j));
	}
	for (int i = 0; i < p; i++) Yn[i] = (double)yp[i];
	if (p==1) for (int i = 0; i < p; i++)  matP[i] = Yn[i] / Xn[0, 0];	
	else {
		int resOk = Matrix.Invert(Xn, p);
		if (resOk == 0) return y1;
		Matrix.Multiply(Xn, Yn, p, p, 1, matP);
	}
	for (int i = 0; i < len; i++) for (int j = 0; j < p; j++) x[j + i * p] = pow(i, j);
	Matrix.Multiply(x, matP, len, p, 1, y);
	for (int i = 0; i < len; i++) y1[i] = (float)y[i];
	delete[] Xn, Yn, matP, x, y ;
	return y1;
}
//-----------------------------------------------------------------------------------------------------------------------------
float* ecart(float* yp, int p, float* serie, int len) {
	return diff(serie, estim(yp, len, p), len);
}
//-----------------------------------------------------------------------------------------------------------------------------
float* adds(float* serie1, float* serie2, int len) {
	float* sserie = new float[len];
	for (int i = 0; i < len; i++) sserie[i] = serie1[i] + serie2[i];
	return sserie;
}
//-----------------------------------------------------------------------------------------------------------------------------
int* ajoute(int* serie1, int len1, int* serie2, int len2) {
	int* sserie = new int[len1 + len2];
	for (int i = 0; i < len1; i++) sserie[i] = serie1[i];
	for (int i = 0; i < len2; i++) sserie[i + len1] = serie2[i];
	return sserie;
}
//-----------------------------------------------------------------------------------------------------------------------------
float* diff(float* serie1, float* serie2, int len) {
	float* sserie = new float[len];
	for (int i = 0; i<len; i++) sserie[i] = serie1[i] - serie2[i];
	return sserie;
}
//-----------------------------------------------------------------------------------------------------------------------------
float* copie(float* serie1, int len) {
	float* sserie = new float[len];
	for (int i = 0; i<len; i++) sserie[i] = serie1[i];
	return sserie;
}
//-----------------------------------------------------------------------------------------------------------------------------
float ec(float* ecart, int len) {
	float ecartAbs = 0;
	for (int i = 0; i<len; i++) ecartAbs += fabs(ecart[i]) / len;
	return ecartAbs;
}
//-----------------------------------------------------------------------------------------------------------------------------
float et(float* ecart, int len) {
	float ecartType = 0;
	for (int i = 0; i<len; i++) ecartType += pow(ecart[i], 2) / len;
	ecartType = sqrt(ecartType);
	return ecartType;
}
//-----------------------------------------------------------------------------------------------------------------------------
float moy(float* serie, int len) {
	float moyenne = 0;
	for (int i = 0; i<len; i++) moyenne += serie[i] / len;
	return moyenne;
}
//-----------------------------------------------------------------------------------------------------------------------------
float* ecretage(float* serie, float mini, float maxi, int len) {
	float* sserie = new float[len];
	for (int i = 0; i<len; i++) sserie[i] = min(maxi, max(mini, serie[i]));
	return sserie;
}
//-----------------------------------------------------------------------------------------------------------------------------
float* sousSerie(float* serie, int indice, int len2) {
	float* sous = new float[len2];
	for (int i = 0; i<len2; i++) sous[i] = serie[indice + i];
	return sous;
}
//-----------------------------------------------------------------------------------------------------------------------------
int* sousSerieInt(int* serie, int indice, int len2) {
	int* sous = new int[len2];
	for (int i = 0; i<len2; i++) sous[i] = serie[indice + i];
	return sous;
}
//-----------------------------------------------------------------------------------------------------------------------------
void addbin(long param, int* payl, int lon, int rang) {
	//for (int i = 0; i<lon; i++) payl[rang + i] = bitRead(param, i);
	//cout << "param, lon, rang : " << param << " " << lon << " " << rang << endl;
	for (int i = 0; i < lon; i++) {
		payl[rang + i] = (param % 2);
		param /= 2;
	}
}
//-----------------------------------------------------------------------------------------------------------------------------
long decbin(int* payl, int lon, int rang) {
	long param = 0;
	//for (int i = 0; i<lon; i++) bitWrite(param, i, payl[rang + i]);
	for (int i = 0; i < lon; i++) param += (long)(payl[rang + i] * pow(2, i));
	//cout << "payl(i+rang) : " << lon << " : "; for (int i = 0; i < lon; i++) cout << payl[rang + i]; cout << endl;
	//cout << " param, lon, rang (decbin) : " << param << " " << lon << " " << rang << endl;
	return param;
}
//-----------------------------------------------------------------------------------------------------------------------------
int conversion(float valeur, float mini, float maxi, int bits) {
	int maxib = (int)pow(2, bits) - 1;
	int val = (int)round(float(maxib * (valeur - mini) / (maxi - mini)));
	return max(0, min(maxib, val));
}
//-----------------------------------------------------------------------------------------------------------------------------
float conversionb(int valeurb, float mini, float maxi, int bits) {
	int maxib = (int)pow(2, bits) - 1;
	return mini + (maxi - mini) * float(valeurb) / float(maxib);
}
float* normalisation(float* serie, float mini, float maxi, int len) {
	float* sserie = new float[len];
	//cout << mini << maxi;
	//cout << " serie : "; for (int i = 0; i<len; i++) cout << serie[i] << ", "; cout << endl;
	for (int i = 0; i < len; i++)  sserie[i] = (min(maxi, max(mini, serie[i])) - mini) / (maxi - mini) - 0.5;
	//cout << " sserie : "; for (int i = 0; i<len; i++) cout << sserie[i] << ", "; cout << endl;
	return sserie;
}
//-----------------------------------------------------------------------------------------------------------------------------
float* denormalisation(float* serie, float mini, float maxi, int len) {
	float* sserie = new float[len];
	for (int i = 0; i < len; i++)  sserie[i] = min(maxi, max(mini, float(mini + (maxi - mini) * (serie[i] + 0.5))));
	return sserie;
}
//-----------------------------------------------------------------------------------------------------------------------------
//SigfoxMessage codage(float* yp0, int nbreg0, int bitc) {
int* codage(float* yp0, int nbreg0, int bitc) {
	int* payl = new int[nbreg0 * bitc];
	//SigfoxMessage payload;
	for (int i = 0; i < nbreg0; i++) addbin(conversion(yp0[i], -0.5, 0.5, bitc), payl, bitc, i*bitc);
	/*payload.msg1 = decbin(payl, TAILLE_MSG, 0);
	payload.msg2 = decbin(payl, TAILLE_MSG, TAILLE_MSG);
	payload.msg3 = decbin(payl, TAILLE_MSG, 2 * TAILLE_MSG);
	delete[] payl;
	return payload;*/
	return payl;
}
//-----------------------------------------------------------------------------------------------------------------------------
//float* decodage(SigfoxMessage payload) {
float* decodage(int* payl, int nbreg0, int bitc) {
	/*addbin(payload.msg1, payl, TAILLE_MSG, 0);
	addbin(payload.msg2, payl, TAILLE_MSG, 32);
	addbin(payload.msg3, payl, TAILLE_MSG, 64);
	*/
	float* yp0 = new float[nbreg0];
	for (int i = 0; i < nbreg0; i++) yp0[i] = conversionb(decbin(payl, bitc, i * bitc), -0.5, 0.5, bitc);
	return yp0;
}
