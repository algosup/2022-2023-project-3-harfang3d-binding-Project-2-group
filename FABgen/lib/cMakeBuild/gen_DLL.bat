@echo off

set "cppFile=%systemroot%\System32\find.exe" lib/cMakeBuild/cppFile.txt
for /f "delims=" %%a in ('%cppFile%') do set "cppFile=%%a"

set "hFile=%systemroot%\System32\find.exe" lib/cMakeBuild/hFile.txt
for /f "delims=" %%a in ('%hFile%') do set "hFile=%%a"

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