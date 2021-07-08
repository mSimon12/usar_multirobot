cmake_minimum_required(VERSION 2.8.3)
project(system_msgs)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  roscpp
  rospy
  std_msgs
  geometry_msgs 
  sensor_msgs
  actionlib_msgs
)


## Generate messages in the 'msg' folder
 add_message_files(
   FILES
   events_message.msg
   task_message.msg
   abstractions.msg
   mission.msg
   m_status.msg
   missions_feedback.msg
   required_events.msg
 )

## Generate added messages and services with any dependencies listed here
generate_messages(
   DEPENDENCIES
   #std_msgs
   geometry_msgs
   actionlib_msgs
   std_msgs
 )

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES mypack_pkg
  CATKIN_DEPENDS message_runtime roscpp rospy std_msgs geometry_msgs sensor_msgs
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


