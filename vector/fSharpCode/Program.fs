open System.Runtime.InteropServices
open System

#if WINDOWS
[<DllImport("lib_vector2.dll")>] 
#else
[<DllImport("VectorsSharedLibraries.dylib")>] 
#endif

extern double distanceTo(double x1, double y1, double x2, double y2);

let x1: float = 5.0
let y1: float = 1.0
let x2: float = 2.0
let y2: float = 2.0

let distance: double = distanceTo(x1, y1, x2, y2)

printfn "Distance between (%f, %f) and (%f, %f) is %f" x1 y1 x2 y2 distance

#if WINDOWS
[<DllImport("lib_vector2.dll")>] 
#else
[<DllImport("VectorsSharedLibraries2.dylib")>] 
#endif

extern double v3distanceTo(double x3, double y3, double z3);

let x3: float = 5.0
let y3: float = 6.0
let z3: float = 3.0

let v3distance: double = v3distanceTo(x3, y3, z3)

printfn "Distance between (%f, %f, %f) and (0, 0, 0) is %f" x3 y3 z3 v3distance