cmake_minimum_required(VERSION 3.6)
project("X-ray Spectrum Analyzer")

# The project version number.
set(VERSION_MAJOR   0   CACHE STRING "Project major version number.")
set(VERSION_MINOR   0   CACHE STRING "Project minor version number.")
set(VERSION_PATCH   1   CACHE STRING "Project patch version number.")
mark_as_advanced(VERSION_MAJOR VERSION_MINOR VERSION_PATCH)

enable_testing()

set(CMAKE_CXX_STANDARD 11)

add_subdirectory(doc)

find_package(Boost COMPONENTS unit_test_framework system filesystem REQUIRED)

set(SOURCE_FILES src/subshell.cpp src/XrayTransition.cpp src/XrayTransition.h src/AugerTransition.cpp src/AugerTransition.h src/AtomicTransitions.cpp src/AtomicTransitions.h)
add_library(xray_spectrum_analyzer SHARED ${SOURCE_FILES})
target_include_directories(xray_spectrum_analyzer PRIVATE src ${BOOST_INCLUDE_DIRS})
target_link_libraries(xray_spectrum_analyzer ${Boost_LIBRARIES})


set(TEST_SOURCE_FILES src/testing/tests.cpp src/testing/test_boost.cpp src/subshell.cpp src/subshell_test.cpp src/XrayTransition.cpp src/XrayTransition.h src/XrayTransition_test.cpp src/AugerTransition.cpp src/AugerTransition.h src/AugerTransition_test.cpp src/AtomicTransitions.cpp src/AtomicTransitions.h src/AtomicTransitions_test.cpp)

add_executable(testing_xray_spectrum_analyzer ${TEST_SOURCE_FILES})

# indicates the include paths
target_include_directories(testing_xray_spectrum_analyzer PRIVATE ${BOOST_INCLUDE_DIRS})

target_link_libraries(testing_xray_spectrum_analyzer ${Boost_LIBRARIES} xray_spectrum_analyzer)

# declares a test with our executable
add_test(NAME test1 COMMAND testing_xray_spectrum_analyzer)

add_custom_command(
        TARGET testing_xray_spectrum_analyzer
        POST_BUILD
        COMMAND ${CMAKE_COMMAND}
        ARGS -E copy_directory ${CMAKE_SOURCE_DIR}/../data ${CMAKE_CURRENT_BINARY_DIR}/data)