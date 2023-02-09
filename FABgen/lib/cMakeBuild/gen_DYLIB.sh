# This script is used to generate the .dylib file for the FABgen library
#!/bin/bash

# Get the name of the .cpp file
read -p "Enter the name of your .cpp file: " filename
echo "Your .cpp file name is: $filename"
echo

# Write the filename in var_store.cmake
echo "set(PROJECT $filename)" > lib/cMakeBuild/var_store.cmake

# Create the folder with the filename
OUTPUTPATH="lib_$filename"

cd ../FABgen/output/CMakeFiles

# Create the output folder
mkdir $OUTPUTPATH
cd $OUTPUTPATH

# Create the build folder
mkdir build
cd build

# Run CMake
cmake ../../../../lib/cMakeBuild
cmake --build .


#Run the code
# cd ../../fSharpCode
# dotnet run
# read