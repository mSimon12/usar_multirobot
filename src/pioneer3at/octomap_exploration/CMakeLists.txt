cmake_minimum_required(VERSION 2.8.3)
project(octomap_exploration)

set(CMAKE_CXX_FLAGS "-std=c++11")

find_package(catkin REQUIRED COMPONENTS 
    roscpp 
    std_msgs 
    geometry_msgs
    message_generation
    actionlib_msgs
    move_base_msgs
    actionlib
    octomap_msgs
)

find_package(octomap REQUIRED)
find_package(OpenMP REQUIRED)

## Generate actions in the 'action' folder
 add_action_files(
   DIRECTORY action
   FILES ExecuteExploration.action
 )

## Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   actionlib_msgs std_msgs geometry_msgs
 )

catkin_package(CATKIN_DEPENDS actionlib roscpp std_msgs message_generation message_runtime)

if(OPENMP_FOUND)
  message(STATUS "OPENMP FOUND")
  set(OpenMP_FLAGS ${OpenMP_CXX_FLAGS})
  set(OpenMP_LIBS gomp)
endif()

include_directories(include ${OCTOMAP_INCLUDE_DIRS} ${catkin_INCLUDE_DIRS})

add_executable(octomap_explorer src/Explorer.cpp src/explorer_node.cpp)
target_compile_options(octomap_explorer PRIVATE ${OpenMP_FLAGS} ${CMAKE_CXX_FLAGS})
target_link_libraries(octomap_explorer ${OCTOMAP_LIBRARIES} ${catkin_LIBRARIES} ${Boost_LIBRARIES} ${OpenMP_LIBS})
add_dependencies(octomap_explorer move_base_msgs_generate_messages)
