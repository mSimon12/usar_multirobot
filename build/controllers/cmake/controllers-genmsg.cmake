# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "controllers: 7 messages, 1 services")

set(MSG_I_FLAGS "-Icontrollers:/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg;-Igeometry_msgs:/opt/ros/melodic/share/geometry_msgs/cmake/../msg;-Iactionlib_msgs:/opt/ros/melodic/share/actionlib_msgs/cmake/../msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(controllers_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg" NAME_WE)
add_custom_target(_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg" "geometry_msgs/Twist:geometry_msgs/Vector3"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionAction.msg" NAME_WE)
add_custom_target(_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionAction.msg" "actionlib_msgs/GoalID:actionlib_msgs/GoalStatus:controllers/motionFeedback:controllers/motionActionResult:geometry_msgs/Twist:controllers/motionActionGoal:controllers/motionResult:std_msgs/Header:controllers/motionGoal:geometry_msgs/Vector3:controllers/motionActionFeedback"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg" NAME_WE)
add_custom_target(_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg" ""
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg" NAME_WE)
add_custom_target(_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg" "actionlib_msgs/GoalID:actionlib_msgs/GoalStatus:controllers/motionFeedback:geometry_msgs/Twist:geometry_msgs/Vector3:std_msgs/Header"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg" NAME_WE)
add_custom_target(_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg" "actionlib_msgs/GoalID:actionlib_msgs/GoalStatus:controllers/motionResult:std_msgs/Header"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg" NAME_WE)
add_custom_target(_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg" "controllers/motionGoal:actionlib_msgs/GoalID:geometry_msgs/Vector3:geometry_msgs/Twist:std_msgs/Header"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg" NAME_WE)
add_custom_target(_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg" "geometry_msgs/Twist:geometry_msgs/Vector3"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/srv/motion.srv" NAME_WE)
add_custom_target(_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/srv/motion.srv" "geometry_msgs/Twist:geometry_msgs/Vector3"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/controllers
)
_generate_msg_cpp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/controllers
)
_generate_msg_cpp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/controllers
)
_generate_msg_cpp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/controllers
)
_generate_msg_cpp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/controllers
)
_generate_msg_cpp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/controllers
)
_generate_msg_cpp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/controllers
)

### Generating Services
_generate_srv_cpp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/controllers
)

### Generating Module File
_generate_module_cpp(controllers
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/controllers
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(controllers_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(controllers_generate_messages controllers_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(controllers_generate_messages_cpp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(controllers_generate_messages_cpp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(controllers_generate_messages_cpp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(controllers_generate_messages_cpp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(controllers_generate_messages_cpp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(controllers_generate_messages_cpp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(controllers_generate_messages_cpp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/srv/motion.srv" NAME_WE)
add_dependencies(controllers_generate_messages_cpp _controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(controllers_gencpp)
add_dependencies(controllers_gencpp controllers_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS controllers_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/controllers
)
_generate_msg_eus(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/controllers
)
_generate_msg_eus(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/controllers
)
_generate_msg_eus(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/controllers
)
_generate_msg_eus(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/controllers
)
_generate_msg_eus(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/controllers
)
_generate_msg_eus(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/controllers
)

### Generating Services
_generate_srv_eus(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/controllers
)

### Generating Module File
_generate_module_eus(controllers
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/controllers
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(controllers_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(controllers_generate_messages controllers_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(controllers_generate_messages_eus _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(controllers_generate_messages_eus _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(controllers_generate_messages_eus _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(controllers_generate_messages_eus _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(controllers_generate_messages_eus _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(controllers_generate_messages_eus _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(controllers_generate_messages_eus _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/srv/motion.srv" NAME_WE)
add_dependencies(controllers_generate_messages_eus _controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(controllers_geneus)
add_dependencies(controllers_geneus controllers_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS controllers_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/controllers
)
_generate_msg_lisp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/controllers
)
_generate_msg_lisp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/controllers
)
_generate_msg_lisp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/controllers
)
_generate_msg_lisp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/controllers
)
_generate_msg_lisp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/controllers
)
_generate_msg_lisp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/controllers
)

### Generating Services
_generate_srv_lisp(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/controllers
)

### Generating Module File
_generate_module_lisp(controllers
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/controllers
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(controllers_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(controllers_generate_messages controllers_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(controllers_generate_messages_lisp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(controllers_generate_messages_lisp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(controllers_generate_messages_lisp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(controllers_generate_messages_lisp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(controllers_generate_messages_lisp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(controllers_generate_messages_lisp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(controllers_generate_messages_lisp _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/srv/motion.srv" NAME_WE)
add_dependencies(controllers_generate_messages_lisp _controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(controllers_genlisp)
add_dependencies(controllers_genlisp controllers_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS controllers_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/controllers
)
_generate_msg_nodejs(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/controllers
)
_generate_msg_nodejs(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/controllers
)
_generate_msg_nodejs(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/controllers
)
_generate_msg_nodejs(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/controllers
)
_generate_msg_nodejs(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/controllers
)
_generate_msg_nodejs(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/controllers
)

### Generating Services
_generate_srv_nodejs(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/controllers
)

### Generating Module File
_generate_module_nodejs(controllers
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/controllers
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(controllers_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(controllers_generate_messages controllers_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(controllers_generate_messages_nodejs _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(controllers_generate_messages_nodejs _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(controllers_generate_messages_nodejs _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(controllers_generate_messages_nodejs _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(controllers_generate_messages_nodejs _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(controllers_generate_messages_nodejs _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(controllers_generate_messages_nodejs _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/srv/motion.srv" NAME_WE)
add_dependencies(controllers_generate_messages_nodejs _controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(controllers_gennodejs)
add_dependencies(controllers_gennodejs controllers_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS controllers_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/controllers
)
_generate_msg_py(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/controllers
)
_generate_msg_py(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/controllers
)
_generate_msg_py(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/controllers
)
_generate_msg_py(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/controllers
)
_generate_msg_py(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/controllers
)
_generate_msg_py(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/controllers
)

### Generating Services
_generate_srv_py(controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/controllers
)

### Generating Module File
_generate_module_py(controllers
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/controllers
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(controllers_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(controllers_generate_messages controllers_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(controllers_generate_messages_py _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(controllers_generate_messages_py _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(controllers_generate_messages_py _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(controllers_generate_messages_py _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(controllers_generate_messages_py _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(controllers_generate_messages_py _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(controllers_generate_messages_py _controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/controllers/srv/motion.srv" NAME_WE)
add_dependencies(controllers_generate_messages_py _controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(controllers_genpy)
add_dependencies(controllers_genpy controllers_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS controllers_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/controllers)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/controllers
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(controllers_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET actionlib_msgs_generate_messages_cpp)
  add_dependencies(controllers_generate_messages_cpp actionlib_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/controllers)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/controllers
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(controllers_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET actionlib_msgs_generate_messages_eus)
  add_dependencies(controllers_generate_messages_eus actionlib_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/controllers)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/controllers
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(controllers_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET actionlib_msgs_generate_messages_lisp)
  add_dependencies(controllers_generate_messages_lisp actionlib_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/controllers)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/controllers
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(controllers_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET actionlib_msgs_generate_messages_nodejs)
  add_dependencies(controllers_generate_messages_nodejs actionlib_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/controllers)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/controllers\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/controllers
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(controllers_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET actionlib_msgs_generate_messages_py)
  add_dependencies(controllers_generate_messages_py actionlib_msgs_generate_messages_py)
endif()
