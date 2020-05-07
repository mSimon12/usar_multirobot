# Install script for directory: /media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/controllers/srv" TYPE FILE FILES "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/srv/motion.srv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/controllers/action" TYPE FILE FILES "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/action/motion.action")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/controllers/msg" TYPE FILE FILES
    "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionAction.msg"
    "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg"
    "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg"
    "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg"
    "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg"
    "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg"
    "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/controllers/cmake" TYPE FILE FILES "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build/controllers/catkin_generated/installspace/controllers-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/include/controllers")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/roseus/ros/controllers")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/common-lisp/ros/controllers")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/gennodejs/ros/controllers")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/lib/python2.7/dist-packages/controllers")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/lib/python2.7/dist-packages/controllers")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build/controllers/catkin_generated/installspace/controllers.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/controllers/cmake" TYPE FILE FILES "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build/controllers/catkin_generated/installspace/controllers-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/controllers/cmake" TYPE FILE FILES
    "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build/controllers/catkin_generated/installspace/controllersConfig.cmake"
    "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build/controllers/catkin_generated/installspace/controllersConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/controllers" TYPE FILE FILES "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/package.xml")
endif()

