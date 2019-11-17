#ifndef COMP_OR
  #define COMP_OR
  
  //#include <iostream>
  #include "series.h"
  //#include <algorithm>
  #include <Arduino.h>

  //#include <string>
  
  class Comp_or
  {
  protected:
  	// parametres normalistion
  	float MINI;					//plage mini et maxi des mesures prise en compte(�cr�tage sinon)
  	float MAXI;					//plage mini et maxi des mesures prise en compte(�cr�tage sinon)
  								// param�tres echantillon
  	int TAILLE_ECH;				//nombre de valeurs � compresser
  								// param�tres internes
  	int BITS;
  	int BITECT;					// nb de bits pour l'�cart-type ex. 8
  	float* y0i;					// valeurs � compresser
  	float* yr0;					// r�sultat non normalis�
  	bool calculKo;
  	// param�tres codage
  	int* payl;
  	int* paylEct;
  	int* paylYp;
  
  public:
  	//Comp_or();
  	Comp_or( float mini,  float maxi,  int bits,  int bitEct,  int tailleEch);
  	~Comp_or();
  
  	int taillePayload();
  	String check();
  	float* simul();
  	float ecartTypeSimul(bool codec);
  	int* compressEct();
  	int* compress();
  	
  	float decompressEct(int* payl);
  };
#endif
