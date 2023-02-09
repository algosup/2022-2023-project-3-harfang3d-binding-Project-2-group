@REM This script is used to generate the .dll file for the FABgen library

@echo off

@REM Ask for the name of the .cpp file (normally "vector2")
set /p filename="Enter the name of your .cpp file: "
echo Your .cpp file name is: %filename%
echo.

@REM Write the filename in var_store.cmake
echo set(PROJECT %filename%) > lib/cMakeBuild/var_store.cmake

@REM Create the folder with the filename
set OUTPUTPATH=lib_%filename%

cd ..\FABgen\output\CMakeFiles

@REM Create the output folder
mkdir %OUTPUTPATH%
cd %OUTPUTPATH%

@REM Create the build folder
mkdir build
cd build

@REM Run CMake
cmake ..\..\..\..\lib\cMakeBuild
cmake --build .


@REM Run the code
@REM cd ../../fSharpCode
@REM dotnet run