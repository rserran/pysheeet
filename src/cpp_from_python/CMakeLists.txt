cmake_minimum_required(VERSION 3.15)
project(cpp_from_python)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Download and configure Google Test
include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG release-1.12.1
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()

# Single executable with tests
add_executable(cpp_from_py cpp_from_py.cpp)
target_link_libraries(cpp_from_py gtest gtest_main)

# Add test
add_test(NAME CppFromPythonTests COMMAND cpp_from_py)
