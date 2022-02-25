// Author Sean Davis
#include "router.h"
#include <cstring>
#include <iostream>
#include "BinaryHeap.h"
using namespace std;

Path::Path()
{
    cost = 1215752190;
}

Pathptr::Pathptr(){}

bool operator<(const Pathptr& a, Pathptr& b)
{
  //cout << "first: " << a.person2->getdv() << " and second: " << b.person2->getdv() << endl;
  if (a.points->cost <= b.points->cost)
    return true;
  else
    return false;
}


Router::Router(const Map1000 *map, int width)
{
    new_map = (Map1000*) malloc(sizeof(Map1000));
    memcpy(new_map->map1000, map, sizeof(Map1000));
    length = width;
    points = new Path*[length];
    ptr = new Pathptr*[length];
    for (int i = 0; i < length; i++)
    {
        points[i] = new Path[length];
        ptr[i] = new Pathptr[length];
    }
} // Router()

Router::~Router()
{
}  // ~Router()


void Router::findRoutes(const CityPos *cityPos, int cityCount, Edge *paths, int &pathCount)
{
    for (int i = 0; i < cityCount; i++)
    {
        points[cityPos[i].x][cityPos[i].y].city = true;
        //points[cityPos[i].x][cityPos[i].y].city_known = false;
    }
    points[cityPos[0].x][cityPos[0].y].x = cityPos[0].x;
    points[cityPos[0].x][cityPos[0].y].y = cityPos[0].y;
    points[cityPos[0].x][cityPos[0].y].cost = 0;
    ptr[cityPos[0].x][cityPos[0].y].points = &points[cityPos[0].x][cityPos[0].y];

    BinaryHeap <Pathptr> heap(3*length*length);
    heap.insert(ptr[cityPos[0].x][cityPos[0].y]);
    pathCount = 0;
    int known_city = 0; //keep track of how many cities are known
    int elevation_change;
    int cost;
    Path insert_path;
    Pathptr placeholder;
    int px;
    int py;
    while (known_city < cityCount)
    {
        placeholder = heap.findMin();
        heap.deleteMin();
        if (placeholder.points->done == true)
            continue;
        px = placeholder.points->x;
        py = placeholder.points->y;
        //cout << px << " " << py << " " << placeholder.points->cost << endl;
        if (placeholder.points->city == true)
        {
            known_city++;
            if (known_city > 1)
            {
                insert_path = points[px][py];
                while (insert_path.city_known == false)
                {
                    paths[pathCount].endX = insert_path.x;
                    paths[pathCount].endY = insert_path.y;
                    insert_path = *insert_path.prv;
                    paths[pathCount].startX = insert_path.x;
                    paths[pathCount].startY = insert_path.y;
                    pathCount++;
                }
            }
            if (known_city == cityCount)
                break;
            placeholder.points->city_known = true;
            placeholder.points->cost = 0;    
        }
        for (int i = px - 1; i < px + 2; i++)
        {
            if (i < 0 || i > length - 1)
                continue;
            for (int j = py - 1; j < py + 2; j++)
            {
                if (px == i && py == j)
                    continue;
                if (j < 0 || j > length - 1)
                    continue;
                elevation_change = abs(new_map->map1000[px][py] - new_map->map1000[i][j]);
                cost = placeholder.points->cost + elevation_change*elevation_change + 10;
                if (cost >= points[i][j].cost)
                    continue;
                points[i][j].x = i;
                points[i][j].y = j;
                points[i][j].prv = &points[px][py];
                points[i][j].cost = cost;
                points[i][j].done = false;
                ptr[i][j].points = &points[i][j];
                heap.insert(ptr[i][j]);
                if (points[i][j].city == true)
                    break;
            }
        }
        ptr[px][py].points->done = true;
    }
    free(new_map);
    for (int i = 0; i < length; i++)
    {
        delete [] points[i];
        delete [] ptr[i];
    }
    delete [] points;
    delete [] ptr;
} // findRoutes()

