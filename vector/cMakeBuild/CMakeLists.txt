cmake_minimum_required(VERSION 3.0)
project(VectorsSharedLibraries)
set(CMAKE_CXX_STANDARD 11)

# Add header files to the project
include_directories(..)

# Add the source files to the project
set(SOURCES ../vector2.cpp ../vector3.cpp)
set(HEADERS ../vector2.h ../vector3.h)

# Create the library
add_library(VectorsSharedLibraries SHARED ${SOURCES} ${HEADERS})

target_include_directories(VectorsSharedLibraries PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/..>
    $<INSTALL_INTERFACE:include>
    PRIVATE src
)

set_target_properties(${lib_name} PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
)

if (APPLE)
    set_target_properties(${lib_name} PROPERTIES
        MACOSX_RPATH ON
    )
endif()