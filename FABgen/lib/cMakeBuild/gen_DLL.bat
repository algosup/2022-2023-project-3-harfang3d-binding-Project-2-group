@echo off

for /f "delims=" %%a in (lib/cMakeBuild/cppFile.txt) do set "cppFile=%%a"
for /f "delims=" %%a in (lib/cMakeBuild/hFile.txt) do set "hFile=%%a"


echo set(PROJECT %cppFile%) > lib/cMakeBuild/var_store.cmake
echo set(SOURCE %cppFile%.cpp) >> lib/cMakeBuild/var_store.cmake
echo set(HEADER %hFile%.h) >> lib/cMakeBuild/var_store.cmake

set "OUTPUTPATH=lib_%cppFile%"

cd ..\FABgen\output\CMakeFiles

echo here is the current directory:
cd

mkdir %OUTPUTPATH%
cd %OUTPUTPATH%

mkdir build
cd build

cmake ..\..\..\..\lib\cMakeBuild
cmake --build .

rmdir /s /q ..\..\..\output\CMakeFiles\%OUTPUTPATH%\build

ren ..\..\..\output\CMakeFiles\%OUTPUTPATH%\lib%OUTPUTPATH%.dylib ..\..\..\output\CMakeFiles\%OUTPUTPATH%\%OUTPUTPATH%.dylib

cd ..\..\fSharpCode
dotnet run
pause