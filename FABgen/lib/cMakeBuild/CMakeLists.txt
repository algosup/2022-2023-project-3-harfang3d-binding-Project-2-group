include(var_store.cmake)

cmake_minimum_required(VERSION 3.0)
set(CMAKE_CXX_STANDARD 11)


project(${PROJECT})

set(PROJECT_NAME lib_${PROJECT})
set(SOURCES ../../input/${PROJECT}.cpp)
set(HEADERS ../../input/${PROJECT}.h)

project(${PROJECT_NAME})
message(STATUS " ========= Building ${PROJECT_NAME} Project =========")

include_directories(..)

# Add the source files to the project
set(SOURCES ${SOURCES})

# Add header files to the project
set(HEADERS ${HEADERS})

message(STATUS " ========= Setting sources at: ${SOURCES} and headers at: ${HEADERS} =========")

# Create the library
add_library(${PROJECT_NAME} SHARED ${SOURCES} ${HEADERS})
message(STATUS " ========= Created library: ${PROJECT_NAME} =========")

target_include_directories(${PROJECT_NAME} PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/..>
    $<INSTALL_INTERFACE:include>
    PRIVATE src
)

# Set output filename suffix based on platform
if(APPLE)
    set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".dylib")
elseif(WIN32)
    set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".dll")
endif()

# This is a hack to get the library to be copied to the correct location and to detect the right folder depending on the .NET version
# This is not a good solution, but there is a better solution, this solution is to put the following lines in the .fsproj file
# <ItemGroup>
#   <None Include="../cMakeBuild/lib/lib${PROJECT_NAME}.dylib">
#       <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
#   </None>
# </ItemGroup>

# execute_process(COMMAND dotnet --version OUTPUT_VARIABLE DOTNET_VERSION)
# string(REGEX REPLACE "(\r?\n)+$" "" DOTNET_VERSION "${DOTNET_VERSION}")
# message(STATUS "Detected .NET version: ${DOTNET_VERSION}")

# if (DOTNET_VERSION MATCHES "^6\\.")
#     set(TARGET_PATH ../fSharpCode/bin/Debug/net6.0)
# elseif (DOTNET_VERSION MATCHES "^7\\.")
#     set(TARGET_PATH ../fSharpCode/bin/Debug/net7.0)
# else()
#     message(FATAL_ERROR "Unsupported .NET version: ${DOTNET_VERSION}")
# endif()

# message(STATUS "Using .NET path: ${TARGET_PATH}")

set(TARGET_PATH FABgen/output/${PROJECT_NAME})

# Set the output directory
set_target_properties(${PROJECT_NAME} PROPERTIES
    # LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
    LIBRARY_OUTPUT_DIRECTORY ${TARGET_PATH}
)
