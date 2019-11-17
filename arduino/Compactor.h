//#pragma once
#ifndef COMPACTOR
  #define COMPACTOR
  #include "Comp_or.h"
  #include <Arduino.h>

  class Compactor : public Comp_or
  {
  protected:
  	int    NBREG0;				// nombre de points de la regression
  	int    BIT;				    // nombre de bits de codage de chaque point de r�gression
  	float* yp0;				    // liste des points de r�gression (normalis�)
  
  public:
  	Compactor(const int nbreg0, const float mini, const float maxi, const int bitc, const int bitEct, const int tailleEch);
  	~Compactor();
  	String check();
  	String calcul(float* y, bool codec);
  	float* param();
  	int* compressYp();
  	int* compress();
  
  // fonctions � utiliser uniquement en mode r�cepteur
  	float* decompressYp(int* payload);
  	float* decompressY0(int* payload);
  
  };
#endif
