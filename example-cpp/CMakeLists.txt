cmake_minimum_required(VERSION 2.8.9)
project(benchbot-test)

# Setup dependencies
find_package(PkgConfig REQUIRED)
pkg_check_modules(BENCHBOT benchbot)

# Build program
add_executable(benchbot-test main.cpp)
target_link_libraries(benchbot-test benchbot benchbot ${BENCHBOT_LIBRARIES})

