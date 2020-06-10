# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "quadrotor_controllers: 7 messages, 1 services")

set(MSG_I_FLAGS "-Iquadrotor_controllers:/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg;-Igeometry_msgs:/opt/ros/melodic/share/geometry_msgs/cmake/../msg;-Iactionlib_msgs:/opt/ros/melodic/share/actionlib_msgs/cmake/../msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(quadrotor_controllers_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg" NAME_WE)
add_custom_target(_quadrotor_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "quadrotor_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg" "geometry_msgs/Twist:geometry_msgs/Vector3"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg" NAME_WE)
add_custom_target(_quadrotor_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "quadrotor_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg" "quadrotor_controllers/motionResult:actionlib_msgs/GoalID:actionlib_msgs/GoalStatus:std_msgs/Header"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionAction.msg" NAME_WE)
add_custom_target(_quadrotor_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "quadrotor_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionAction.msg" "actionlib_msgs/GoalID:quadrotor_controllers/motionActionFeedback:quadrotor_controllers/motionActionResult:quadrotor_controllers/motionActionGoal:actionlib_msgs/GoalStatus:geometry_msgs/Twist:quadrotor_controllers/motionGoal:quadrotor_controllers/motionResult:std_msgs/Header:geometry_msgs/Vector3:quadrotor_controllers/motionFeedback"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/quadrotor/quadrotor_controllers/srv/motion.srv" NAME_WE)
add_custom_target(_quadrotor_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "quadrotor_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/quadrotor/quadrotor_controllers/srv/motion.srv" "geometry_msgs/Twist:geometry_msgs/Vector3"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg" NAME_WE)
add_custom_target(_quadrotor_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "quadrotor_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg" "actionlib_msgs/GoalID:quadrotor_controllers/motionFeedback:actionlib_msgs/GoalStatus:geometry_msgs/Twist:geometry_msgs/Vector3:std_msgs/Header"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg" NAME_WE)
add_custom_target(_quadrotor_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "quadrotor_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg" "geometry_msgs/Twist:geometry_msgs/Vector3"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg" NAME_WE)
add_custom_target(_quadrotor_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "quadrotor_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg" "geometry_msgs/Vector3:actionlib_msgs/GoalID:geometry_msgs/Twist:quadrotor_controllers/motionGoal:std_msgs/Header"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg" NAME_WE)
add_custom_target(_quadrotor_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "quadrotor_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_cpp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_cpp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_cpp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_cpp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_cpp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_cpp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/quadrotor_controllers
)

### Generating Services
_generate_srv_cpp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/quadrotor/quadrotor_controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/quadrotor_controllers
)

### Generating Module File
_generate_module_cpp(quadrotor_controllers
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/quadrotor_controllers
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(quadrotor_controllers_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(quadrotor_controllers_generate_messages quadrotor_controllers_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_cpp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_cpp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_cpp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/quadrotor/quadrotor_controllers/srv/motion.srv" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_cpp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_cpp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_cpp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_cpp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_cpp _quadrotor_controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(quadrotor_controllers_gencpp)
add_dependencies(quadrotor_controllers_gencpp quadrotor_controllers_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS quadrotor_controllers_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_eus(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_eus(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_eus(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_eus(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_eus(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_eus(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/quadrotor_controllers
)

### Generating Services
_generate_srv_eus(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/quadrotor/quadrotor_controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/quadrotor_controllers
)

### Generating Module File
_generate_module_eus(quadrotor_controllers
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/quadrotor_controllers
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(quadrotor_controllers_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(quadrotor_controllers_generate_messages quadrotor_controllers_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_eus _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_eus _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_eus _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/quadrotor/quadrotor_controllers/srv/motion.srv" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_eus _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_eus _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_eus _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_eus _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_eus _quadrotor_controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(quadrotor_controllers_geneus)
add_dependencies(quadrotor_controllers_geneus quadrotor_controllers_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS quadrotor_controllers_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_lisp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_lisp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_lisp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_lisp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_lisp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_lisp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/quadrotor_controllers
)

### Generating Services
_generate_srv_lisp(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/quadrotor/quadrotor_controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/quadrotor_controllers
)

### Generating Module File
_generate_module_lisp(quadrotor_controllers
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/quadrotor_controllers
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(quadrotor_controllers_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(quadrotor_controllers_generate_messages quadrotor_controllers_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_lisp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_lisp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_lisp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/quadrotor/quadrotor_controllers/srv/motion.srv" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_lisp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_lisp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_lisp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_lisp _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_lisp _quadrotor_controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(quadrotor_controllers_genlisp)
add_dependencies(quadrotor_controllers_genlisp quadrotor_controllers_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS quadrotor_controllers_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_nodejs(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_nodejs(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_nodejs(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_nodejs(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_nodejs(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_nodejs(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/quadrotor_controllers
)

### Generating Services
_generate_srv_nodejs(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/quadrotor/quadrotor_controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/quadrotor_controllers
)

### Generating Module File
_generate_module_nodejs(quadrotor_controllers
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/quadrotor_controllers
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(quadrotor_controllers_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(quadrotor_controllers_generate_messages quadrotor_controllers_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_nodejs _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_nodejs _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_nodejs _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/quadrotor/quadrotor_controllers/srv/motion.srv" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_nodejs _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_nodejs _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_nodejs _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_nodejs _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_nodejs _quadrotor_controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(quadrotor_controllers_gennodejs)
add_dependencies(quadrotor_controllers_gennodejs quadrotor_controllers_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS quadrotor_controllers_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_py(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_py(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_py(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_py(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_py(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/quadrotor_controllers
)
_generate_msg_py(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/quadrotor_controllers
)

### Generating Services
_generate_srv_py(quadrotor_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/quadrotor/quadrotor_controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/quadrotor_controllers
)

### Generating Module File
_generate_module_py(quadrotor_controllers
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/quadrotor_controllers
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(quadrotor_controllers_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(quadrotor_controllers_generate_messages quadrotor_controllers_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_py _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_py _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_py _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/quadrotor/quadrotor_controllers/srv/motion.srv" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_py _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_py _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_py _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_py _quadrotor_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/quadrotor_controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(quadrotor_controllers_generate_messages_py _quadrotor_controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(quadrotor_controllers_genpy)
add_dependencies(quadrotor_controllers_genpy quadrotor_controllers_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS quadrotor_controllers_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/quadrotor_controllers)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/quadrotor_controllers
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(quadrotor_controllers_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET actionlib_msgs_generate_messages_cpp)
  add_dependencies(quadrotor_controllers_generate_messages_cpp actionlib_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/quadrotor_controllers)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/quadrotor_controllers
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(quadrotor_controllers_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET actionlib_msgs_generate_messages_eus)
  add_dependencies(quadrotor_controllers_generate_messages_eus actionlib_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/quadrotor_controllers)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/quadrotor_controllers
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(quadrotor_controllers_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET actionlib_msgs_generate_messages_lisp)
  add_dependencies(quadrotor_controllers_generate_messages_lisp actionlib_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/quadrotor_controllers)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/quadrotor_controllers
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(quadrotor_controllers_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET actionlib_msgs_generate_messages_nodejs)
  add_dependencies(quadrotor_controllers_generate_messages_nodejs actionlib_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/quadrotor_controllers)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/quadrotor_controllers\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/quadrotor_controllers
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(quadrotor_controllers_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET actionlib_msgs_generate_messages_py)
  add_dependencies(quadrotor_controllers_generate_messages_py actionlib_msgs_generate_messages_py)
endif()
