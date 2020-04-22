execute_process(COMMAND "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build/pioneer2dx_ros/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build/pioneer2dx_ros/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
