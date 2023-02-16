include(var_store.cmake)

cmake_minimum_required(VERSION 3.0)
set(CMAKE_CXX_STANDARD 11)

project(${PROJECT})

set(PROJECT_NAME lib_${PROJECT})
set(SOURCES ../../input/${SOURCE})
set(HEADERS ../../input/${HEADER})

project(${PROJECT_NAME})
# message(STATUS " ========= Building ${PROJECT_NAME} Project =========")
message(STATUS " ========= var PROJECT is ${PROJECT} =========")
message(STATUS " ========= var PROJECT_NAME is ${PROJECT_NAME} =========")

include_directories(..)

# Add the source files to the project

# Add header files to the project

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

set(TARGET_PATH ../../${PROJECT_NAME})

# Set the output directory
set_target_properties(${PROJECT_NAME} PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${TARGET_PATH}
)