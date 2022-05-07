#include <iostream>  // for debugging
#include <cstring>
#include <cstdlib>
#include "spreader.h"
#include "BinaryHeap.h"
using namespace std;

Person2ptr::Person2ptr(){}

Person2ptr::Person2ptr(Person2 *ptr)
{
  person2 = ptr;
}

bool operator<(const Person2ptr& a, Person2ptr& b)
{
  //cout << "first: " << a.person2->getdv() << " and second: " << b.person2->getdv() << endl;
  if (a.person2->dv <= b.person2->dv)
    return true;
  else
    return false;
}

Spreader::Spreader(const Person* people, int population)
{
  speople = new Person2[population];
  ptr = new Person2ptr[population];
  no_people = population;
  for (int i = 0; i < population; i++)
  {
    ptr[i].person2 = &speople[i];
    ptr[i].person2->dv = 900000000;
    ptr[i].person2->ID = people[i].ID;
    ptr[i].person2->peopleMet = people[i].peopleMet;
    ptr[i].person2->visitors = (Visitor *) malloc(ptr[i].person2->peopleMet*sizeof(Visitor));
    memcpy(ptr[i].person2->visitors, people[i].visitors, ptr[i].person2->peopleMet*sizeof(Visitor));
  }
  // Students write this. 
  // Note that people will be deleted before simulate() is called.
} // Spreader()


int Spreader::simulate(int starterIDs[], int starterCount, int commandLineOption)
{
  Dijkstra(starterCount, starterIDs);
  // commandLineOption may be used to signal the program to do whatever the students 
  // want, or nothing at all.

  // Students write this.  Returns days until of last person catches the virus
  return day; // to avoid warnings for now.
}

void Spreader::Dijkstra(int starterCount, int starterIDs[])
{
  BinaryHeap <Person2ptr> heap(no_people * 5);
  for (int i = 0; i < starterCount; i++)
  {
    (ptr[starterIDs[i]]).person2->dv = 0;
    heap.insert(ptr[starterIDs[i]]);
  }
  int inf_date;
  while (!heap.isEmpty())
  {
    const Person2ptr placeholder = heap.findMin();
    heap.deleteMin();
    if (ptr[placeholder.person2->ID].person2->known == true)
      continue;
    day = placeholder.person2->dv;
    ptr[placeholder.person2->ID].person2->known = true;
    for (int i = 0; i < placeholder.person2->peopleMet; i++)
    {
      if (ptr[placeholder.person2->visitors[i].ID].person2->known == true)
        continue;
      if ((placeholder.person2->dv + 3)%placeholder.person2->visitors[i].period == 0)
        inf_date = placeholder.person2->dv + 3;
      else
        inf_date = ((placeholder.person2->dv + 3)/placeholder.person2->visitors[i].period)*placeholder.person2->visitors[i].period + placeholder.person2->visitors[i].period;
      if (inf_date < ptr[placeholder.person2->visitors[i].ID].person2->dv)
      {
        ptr[placeholder.person2->visitors[i].ID].person2->dv = inf_date;
        heap.insert(ptr[placeholder.person2->visitors[i].ID]);
      }
    }
  }
}