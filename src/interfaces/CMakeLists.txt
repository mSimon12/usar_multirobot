cmake_minimum_required(VERSION 2.8.3)
project(interfaces)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  roscpp
  rospy
  std_msgs
  nav_msgs
  geometry_msgs 
)

## Generate messages in the 'msg' folder
 add_message_files(
   FILES
   trace_events.msg
 )

## Generate added messages and services with any dependencies listed here
generate_messages(
#   DEPENDENCIES
#   geometry_msgs
)


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES interfaces
  CATKIN_DEPENDS message_runtime rospy std_msgs nav_msgs geometry_msgs
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

