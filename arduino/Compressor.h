//#pragma once
#ifndef COMPRESSOR
  #define COMPRESSOR
  
  #include <Arduino.h>
  #include "Comp_or.h"
  //#include "Compactor.h"
  //#include <iostream>
  #include "series.h"
  //#include <algorithm>
  
  //#include <string>
  class Compressor : public Comp_or
  {
  protected:
    // parametres compression
    int NBREG;          // nombre de régression de niveau 1 ex. 8, 0 si aucune
    int NBREG0;         // nombre de points de la regression de niveau 0 (entre 2 et 10)
    int NBREG1;         // nombre de points de la regression de niveau 1 (entre 2 et 10)
                  // parametres codage
    int BIT_0;
    int BIT_1;
  public:
    Compressor(const int nbreg, const int nbreg0, const int nbreg1, const float mini, const float maxi, 
               const int bit0, const int bit1, const int bitEct, const int tailleEch);
    ~Compressor();
    String check();
    String calcul(float* y, bool codec);
    
    // fonctions à utiliser uniquement en mode récepteur
    float* decompressY0(int* payload);
  };
#endif
