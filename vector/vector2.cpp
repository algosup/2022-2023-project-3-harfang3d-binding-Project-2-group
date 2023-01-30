#include "Vector2.h"
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <math.h>

extern "C"
{

    Vector2::Vector2(double x, double y) : x(x), y(y) {} 
    double Vector2::distanceTo(Vector2 pos)
    {
        return sqrt(pow(x - pos.x, 2) + pow(y - pos.y, 2));
    }
    void Vector2::vectorMovement(double plusx, double plusy)
    {
        x += plusx;
        y += plusy;
    }
    Vector2 Vector2::midpoint(Vector2 pos)
    {
        return Vector2((x + pos.x) / 2, (y + pos.y) / 2);
    }
    double Vector2::percentDistance(Vector2 pos, double percentOfDistance)
    {
        return distanceTo(pos) * percentOfDistance;
    }

    double distanceTo(double x1, double y1, double x2, double y2)
    {
        return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
    }

    double percentDistance(double x, double y, double percentOfDistance)
    {
        return distanceTo(x, y, 0, 0) * percentOfDistance;
    }

}