#!/bin/sh
# This script is used to generate the .dylib file for the FABGen library

# Get the name of the .cpp file
echo -n "Enter the name of your .cpp file: "
read filename
echo "Your .cpp file name is: $filename"

FILENAME="$filename"

OUTPUTPATH="lib_$FILENAME"


cd ../../output/CMakeFiles/
mkdir $OUTPUTPATH
cd $OUTPUTPATH
mkdir build
cd build

cmake ../../../../lib/cMakeBuild
cmake --build .


#Run the code
# cd ../../fSharpCode
# dotnet run
# read




