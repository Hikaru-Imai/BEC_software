cmake_minimum_required(VERSION 3.1)
project (Detection)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ../)
find_package(OpenCV REQUIRED)
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable(RUN Detection.C)
target_link_libraries(RUN ${OpenCV_LIBS})
