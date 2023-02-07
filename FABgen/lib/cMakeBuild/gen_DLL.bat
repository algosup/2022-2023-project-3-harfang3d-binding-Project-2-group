@rem This script is used to generate the .dll file for the FABGen library

@echo off
echo Enter the name of your .cpp file:
set /p filename= Type any input
echo Your .cpp file name is: %filename%

set "FILENAME=%filename%"

set /A OUTPUTPATH= lib_%FILENAME%

cd /d %~dp0

@REM Build in the cMakeBuild folder
cd ../../output/CMakeFiles/
mkdir %OUTPUTPATH%
cd %OUTPUTPATH%
mkdir build
cd build


cmake ../../../../lib/cMakeBuild
cmake --build .



@REM Run the code
@REM cd ../../fSharpCode
@REM dotnet run
