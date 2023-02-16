include(var_store.cmake)

cmake_minimum_required(VERSION 3.0)
set(CMAKE_CXX_STANDARD 11)

project(${SOURCE})

set(PROJECT_NAME lib_${PROJECT})
set(SOURCES ../../input/${SOURCE})
set(HEADERS ../../input/${HEADER})

project(${PROJECT_NAME})

include_directories(..)

# Create the library
add_library(${PROJECT_NAME} SHARED ${SOURCES} ${HEADERS})

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

set(TARGET_PATH ../../${PROJECT_NAME})

# Set the output directory
set_target_properties(${PROJECT_NAME} PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${TARGET_PATH}
)