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

# Set output filename suffix based on platform
if(APPLE)
    set_target_properties(VectorsSharedLibraries PROPERTIES SUFFIX ".dylib")
elseif(WIN32)
    set_target_properties(VectorsSharedLibraries PROPERTIES SUFFIX ".dll")
endif()

execute_process(COMMAND dotnet --version OUTPUT_VARIABLE DOTNET_VERSION)
string(REGEX REPLACE "(\r?\n)+$" "" DOTNET_VERSION "${DOTNET_VERSION}")
message(STATUS "Detected .NET version: ${DOTNET_VERSION}")

if (DOTNET_VERSION MATCHES "^6\\.")
    set(TARGET_PATH ../fSharpCode/bin/Debug/net6.0)
elseif (DOTNET_VERSION MATCHES "^7\\.")
    set(TARGET_PATH ../fSharpCode/bin/Debug/net7.0)
else()
    message(FATAL_ERROR "Unsupported .NET version: ${DOTNET_VERSION}")
endif()

message(STATUS "Using .NET path: ${TARGET_PATH}")


# Set the output directory
set_target_properties(VectorsSharedLibraries PROPERTIES
    # LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
    LIBRARY_OUTPUT_DIRECTORY ${TARGET_PATH}
)
