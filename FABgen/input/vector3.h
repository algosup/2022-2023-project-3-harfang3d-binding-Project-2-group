struct Vector3
{
    double x;
    double y;
    double z;
    Vector3(double inx = 0, double iny = 0, double inz = 0);
    double distanceTo(Vector3 pos);
    void vectorMovement(double plusx, double plusy, double plusz);
    Vector3 midpoint(Vector3 pos);
    double percentDistance(Vector3 pos, double percentOfDistance = 100);
};
