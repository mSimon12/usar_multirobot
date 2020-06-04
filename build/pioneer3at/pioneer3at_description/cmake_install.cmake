# Install script for directory: /media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer3at/pioneer3at_description

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
  include("/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build/pioneer3at/pioneer3at_description/catkin_generated/safe_execute_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build/pioneer3at/pioneer3at_description/catkin_generated/installspace/pioneer3at_description.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pioneer3at_description/cmake" TYPE FILE FILES
    "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build/pioneer3at/pioneer3at_description/catkin_generated/installspace/pioneer3at_descriptionConfig.cmake"
    "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build/pioneer3at/pioneer3at_description/catkin_generated/installspace/pioneer3at_descriptionConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pioneer3at_description" TYPE FILE FILES "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer3at/pioneer3at_description/package.xml")
endif()

