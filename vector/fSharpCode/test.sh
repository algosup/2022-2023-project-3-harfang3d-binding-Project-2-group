
# alias proj="cd /d %~dp0"
# cd /d %~dp0
cd ..
cd cMakeBuild
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