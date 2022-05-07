#ifndef SPREADER_H
#define SPREADER_H

#include "spreaderRunner.h"
#include "StackAr.h"

class Person2
{
  public: 
    const Person *person;
    int ID;
    int peopleMet;
    Visitor *visitors;
    int dv; //day of infection
    bool known;
};
class Person2ptr
{
  public:
    Person2 *person2;
    Person2ptr();
    Person2ptr(Person2 *ptr);
    friend bool operator<(const Person2ptr& a, Person2ptr& b);
};
class Spreader
{
  Person2 *speople;
  Person2ptr *ptr;
  int day;
  int no_people;
public:
  Spreader(const Person* people, int population);
  int simulate(int starterIDs[], int starterCount, int commandLineOption);
  void Dijkstra(int starterCount, int starterIDs[]);
};

#endif /* SPREADER_H */

