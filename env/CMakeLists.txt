cmake_minimum_required(VERSION 3.14)

project(env)


set(CMAKE_CXX_STANDARD 14)


find_package(OpenCV REQUIRED)

add_library(c_opencv SHARED
        op_c.cpp
        agent.cpp
        detect/detect.cpp
        detect/finish_detect.cpp
        detect/running_detect.cpp
        detect/menu_detect.cpp
        detect/start_detect.cpp
        detect/button_detect.cpp
        dnn/elixir_detect.cpp
        dnn/card_detect.cpp
        dnn/hp_detect.cpp)

include_directories(./include)

include_directories(${OpenCV_INCLUDE_DIRS})

target_link_libraries(c_opencv ${OpenCV_LIBS})

add_executable(env main3.cpp)


target_link_libraries(env c_opencv)

