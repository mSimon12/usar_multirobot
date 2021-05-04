cmake_minimum_required(VERSION 2.8.3)
project(quadrotor_control_system)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  moveit_core 
  moveit_commander
  hector_moveit_actions
  trajectory_action_pkg
  joy
  hector_moveit_config
  std_msgs
  sensor_msgs
  geometry_msgs
  actionlib_msgs
  hector_uav_msgs
  actionlib
  genmsg 
  system_msgs
)

find_package(octomap REQUIRED)

## System dependencies are found with CMake's conventions
# find_package(Boost REQUIRED COMPONENTS system)

## Generate actions in the 'action' folder
add_action_files(
   FILES
   ExecuteSearch.action
   ExecuteLand.action
 )

## Generate added messages and services with any dependencies listed here
generate_messages(
   DEPENDENCIES
   #std_msgs
   geometry_msgs
   actionlib_msgs
 )


###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if your package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES mypack_pkg
  CATKIN_DEPENDS roscpp rospy hector_moveit_config std_msgs geometry_msgs hector_uav_msgs moveit_core moveit_ros_planning_interface hector_moveit_actions trajectory_action_pkg
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
  include
  ${OCTOMAP_INCLUDE_DIRS}
  ${catkin_INCLUDE_DIRS}
)

## Add cmake target dependencies of the executable
## same as for the library above
## add_dependencies(${PROJECT_NAME} ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

## Specify libraries to link a library or executable target against
# target_link_libraries(${PROJECT_NAME}_node
#   ${catkin_LIBRARIES}
# )

