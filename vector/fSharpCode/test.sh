
# alias proj="cd /d %~dp0"
# cd /d %~dp0
cd ..
cd cMakeBuild
cd build

cmake ..
# $@REM insert the cmake build command here
cd ..
cd ..
cd fSharpCode
dotnet run

read