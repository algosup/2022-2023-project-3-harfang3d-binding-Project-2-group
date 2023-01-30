#include "Vector3.h"
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <math.h>

extern "C"
{
    Vector3::Vector3(double inx, double iny, double inz) : x(inx), y(iny), z(inz) {}
    double distanceTo(Vector3 pos) {
        return sqrt((pos.y - y) * (pos.y - y) + (pos.x - x) * (pos.x - x) + (pos.z - z) * (pos.z - z));
    }
    void vectorMovement(double plusx, double plusy, double plusz) {
        x += plusx;
        y += plusy;
        z += plusz;
        return;
    }
    Vector3 midpoint(Vector3 pos) {
        double mx = (x + pos.x) / 2;
        double my = (y + pos.y) / 2;
        double mz = (z + pos.z) / 2;
        Vector3 mid(mx, my, mz);
        return mid;
    }
    double percentDistance(Vector3 pos, double percentOfDistance = 100) {
        return distanceTo(pos) / (100 / percentOfDistance);
    }
}