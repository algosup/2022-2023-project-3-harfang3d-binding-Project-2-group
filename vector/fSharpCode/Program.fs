open System.Runtime.InteropServices

[<DllImport("VectorsSharedLibraries.dll")>]
extern double distanceTo(double x1, double y1, double x2, double y2);

let x1: float = 5.0
let y1: float = 1.0
let x2: float = 2.0
let y2: float = 2.0

let distance: double = distanceTo(x1, y1, x2, y2)

printfn "Distance between (%f, %f) and (%f, %f) is %f" x1 y1 x2 y2 distance