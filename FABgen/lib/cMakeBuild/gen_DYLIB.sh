#!/bin/bash
# This script is used to generate the .dylib file for the FABgen library
cppFile=$(cat lib/cMakeBuild/cppFile.txt)
hFile=$(cat lib/cMakeBuild/hFile.txt)

# Write the filename in var_store.cmake
echo "set(PROJECT $cppFile)" > lib/cMakeBuild/var_store.cmake
echo "set(SOURCE $cppFile.cpp)" >> lib/cMakeBuild/var_store.cmake
echo "set(HEADER $hFile.h)" >> lib/cMakeBuild/var_store.cmake


# Create the folder with the filename
OUTPUTPATH="lib_$cppFile"

cd ../FABgen/output/CMakeFiles

# output "here is the current directory:"
echo "here is the current directory:"
pwd

# Create the output folder
mkdir $OUTPUTPATH
cd $OUTPUTPATH

# Create the build folder
mkdir build
cd build

# Run CMake
cmake ../../../../lib/cMakeBuild
cmake --build .

rm -rf ../../../../output/CMakeFiles/$OUTPUTPATH/build
# Rename the .dylib file
mv ../../../../output/CMakeFiles/$OUTPUTPATH/lib$OUTPUTPATH.dylib ../../../../output/CMakeFiles/$OUTPUTPATH/$OUTPUTPATH.dylib

#Run the code
# cd ../../fSharpCode
# dotnet run
# read