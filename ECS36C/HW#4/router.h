// Author: Sean Davis

#ifndef ROUTER_H
  #define ROUTER_H

#include "RouterRunner.h"

class Path
{
  public:
  int x;
  int y;
  int cost;
  bool city;
  bool city_known;
  bool done;
  Path *prv;
  Path();
};

class Pathptr
{
   public:
	Path *points;
	Pathptr();
	friend bool operator<(const Pathptr& a, Pathptr&b);
};

class Router
{
public:
  Map1000* new_map;
  int length;
  Path **points;
  Pathptr **ptr;
  
  
  Router(const Map1000 *map, int width);
  ~Router();
  void findRoutes(const CityPos *cityPos, int cityCount, Edge *paths, int &pathCount);
};



#endif
