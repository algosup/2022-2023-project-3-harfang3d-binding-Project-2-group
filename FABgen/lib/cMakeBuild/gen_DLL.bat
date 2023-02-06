cd /d %~dp0
cd ..
cd cMakeBuild
mkdir build
cd build
cmake ..
cmake --build .
cd ..
cd ..
cd cMakeBuild2
mkdir build
cd build
cmake ..
cmake --build .
@REM insert the cmake build command here
cd ..
cd ..
cd fSharpCode
dotnet run
