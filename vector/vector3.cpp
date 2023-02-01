#include "vector3.h"
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <math.h>

extern "C"
{

    Vector3::Vector3(double x, double y, double z) : x(x), y(y), z(z) {}
    double Vector3::distanceTo(Vector3 pos) {
        return sqrt((pos.y - y) * (pos.y - y) + (pos.x - x) * (pos.x - x) + (pos.z - z) * (pos.z - z));
    }
    void Vector3::vectorMovement(double plusx, double plusy, double plusz) {
        x += plusx;
        y += plusy;
        z += plusz;
    }

    Vector3 Vector3::midpoint(Vector3 pos) {
        return Vector3((x + pos.x) / 2, (y + pos.y) / 2, (z + pos.z) / 2);
    }

    double Vector3::percentDistance(Vector3 pos, double percentOfDistance) {
        return distanceTo(pos) * percentOfDistance;
    }

    double v3distanceTo(double x1, double y1, double z1) {
        return sqrt(pow(x1, 2) + pow(y1, 2) + pow(z1, 2));
    }

    double v3percentDistance(double x, double y, double z, double percentOfDistance) {
        return v3distanceTo(x, y, z) * percentOfDistance;
    }

}