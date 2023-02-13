@echo off
set /p cppFile=<..\FABgen\lib\cMakeBuild\cppFile.txt
set /p hFile=<..\FABgen\lib\cMakeBuild\hFile.txt
echo %cppFile%
echo %hFile%
echo set(PROJECT %cppFile%) > lib/cMakeBuild/var_store.cmake
echo 3
echo set(SOURCE %cppFile%.cpp) >> lib/cMakeBuild/var_store.cmake
echo 4
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

ren ..\..\..\output\CMakeFiles\%OUTPUTPATH%\build\Debug\%OUTPUTPATH%.dll ..\..\..\output\CMakeFiles\%OUTPUTPATH%\%OUTPUTPATH%.dll
rmdir /s /q ..\..\..\output\CMakeFiles\%OUTPUTPATH%\build

cd ..\..\..\..\..\vector\fSharpCode
dotnet run
pause