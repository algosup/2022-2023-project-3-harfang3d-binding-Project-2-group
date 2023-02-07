struct Vector2
{
    double x;
    double y;
    Vector2(double x, double y);
    double distanceTo(Vector2 pos);
    void vectorMovement(double plusx, double plusy);
    Vector2 midpoint(Vector2 pos);
    double percentDistance(Vector2 pos, double percentOfDistance);
};