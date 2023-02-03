#!/bin/sh
# alias proj="cd /d %~dp0"
# cd /d %~dp0
cd ..
cd vector
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
# $@REM insert the cmake build command here
cd ..
cd ..
cd fSharpCode
dotnet run

read