cmake_minimum_required(VERSION 2.8.3)
project(uav)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages

find_package(catkin REQUIRED COMPONENTS
  usar_gazebo
)

catkin_package()

install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
install(DIRECTORY rviz_cfg DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

