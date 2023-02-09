#!/bin/bash
# This script is used to generate the .dylib file for the FABgen library

# Get the name of the .cpp file
read -p "Enter the name of your .cpp file: " filename
echo "Your .cpp file name is: $filename"
echo

#write $filename in var_store.cmake
echo "set(PROJECT $filename)" > lib/cMakeBuild/var_store.cmake

OUTPUTPATH="lib_$filename"

cd ../FABgen/output/CMakeFiles

mkdir $OUTPUTPATH
cd $OUTPUTPATH

mkdir build
cd build

cmake ../../../../lib/cMakeBuild
cmake --build .

rm -rf ../../../../output/CMakeFiles/$OUTPUTPATH/build
# rename the .dylib file
mv ../../../../output/CMakeFiles/$OUTPUTPATH/lib$OUTPUTPATH.dylib ../../../../output/CMakeFiles/$OUTPUTPATH/$OUTPUTPATH.dylib

#Run the code
# cd ../../fSharpCode
# dotnet run
# read