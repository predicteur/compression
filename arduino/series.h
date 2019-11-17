//#pragma once
//#include <iostream>

float*		regx		  (float* serie, int len, int p);
float*		estim		  (float* yp, int len, int p);

float*		ecart		  (float* yp, int p, float* serie, int len);
float*		adds		  (float* serie1, float* serie2, int len);
float*		diff		  (float* serie1, float* serie2, int len);
float*		copie	  	(float* serie1, int len);
float		  ec		  	(float* ecart, int len);
float		  et			  (float* ecart, int len);
float		  moy			  (float* serie, int len);
float*		ecretage	(float* serie, float mini, float maxi, int len);
float*		sousSerie	(float* serie, int indice, int len2);
int*		  sousSerieInt(int* serie, int indice, int len2);
int*		  ajoute		(int* serie1, int len1, int* serie2, int len2);

void		  addbin		(long param, int* payl, int lon, int rang);
long	    decbin		(int* payl, int lon, int rang);
int			  conversion      (float valeur, float mini, float maxi, int bits);
float		  conversionb	    (int valeurb, float mini, float maxi, int bits);
float*		normalisation   (float* serie, float mini, float maxi, int len);
float*		denormalisation	(float* serie, float mini, float maxi, int len);
int*		  codage		(float* yp0, int nbreg0, int bitc);
float*		decodage	(int* payl, int nbreg0, int bitc);
