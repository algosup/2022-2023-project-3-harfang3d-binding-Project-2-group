cmake_minimum_required(VERSION 3.0)
project(VectorsSharedLibraries)
set(CMAKE_CXX_STANDARD 11)

# Add header files to the project
include_directories(..)

# Add the source files to the project
set(SOURCES ../vector2.cpp ../vector3.cpp)

# Add the header files to the project
set(HEADERS ../vector2.h ../vector3.h)

# Create the library
add_library(VectorsSharedLibraries SHARED ${SOURCES})