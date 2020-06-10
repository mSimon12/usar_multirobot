# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "pioneer2dx_controllers: 7 messages, 1 services")

set(MSG_I_FLAGS "-Ipioneer2dx_controllers:/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg;-Igeometry_msgs:/opt/ros/melodic/share/geometry_msgs/cmake/../msg;-Iactionlib_msgs:/opt/ros/melodic/share/actionlib_msgs/cmake/../msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(pioneer2dx_controllers_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg" NAME_WE)
add_custom_target(_pioneer2dx_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pioneer2dx_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg" "actionlib_msgs/GoalID:pioneer2dx_controllers/motionFeedback:actionlib_msgs/GoalStatus:geometry_msgs/Twist:geometry_msgs/Vector3:std_msgs/Header"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg" NAME_WE)
add_custom_target(_pioneer2dx_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pioneer2dx_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg" "pioneer2dx_controllers/motionResult:actionlib_msgs/GoalID:actionlib_msgs/GoalStatus:std_msgs/Header"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer2dx/pioneer2dx_controllers/srv/motion.srv" NAME_WE)
add_custom_target(_pioneer2dx_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pioneer2dx_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer2dx/pioneer2dx_controllers/srv/motion.srv" "geometry_msgs/Twist:geometry_msgs/Vector3"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg" NAME_WE)
add_custom_target(_pioneer2dx_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pioneer2dx_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg" "geometry_msgs/Twist:geometry_msgs/Vector3"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg" NAME_WE)
add_custom_target(_pioneer2dx_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pioneer2dx_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg" "geometry_msgs/Twist:geometry_msgs/Vector3"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg" NAME_WE)
add_custom_target(_pioneer2dx_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pioneer2dx_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg" "geometry_msgs/Vector3:actionlib_msgs/GoalID:pioneer2dx_controllers/motionGoal:geometry_msgs/Twist:std_msgs/Header"
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg" NAME_WE)
add_custom_target(_pioneer2dx_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pioneer2dx_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg" ""
)

get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionAction.msg" NAME_WE)
add_custom_target(_pioneer2dx_controllers_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pioneer2dx_controllers" "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionAction.msg" "actionlib_msgs/GoalID:pioneer2dx_controllers/motionGoal:pioneer2dx_controllers/motionActionGoal:geometry_msgs/Twist:geometry_msgs/Vector3:pioneer2dx_controllers/motionResult:pioneer2dx_controllers/motionFeedback:std_msgs/Header:pioneer2dx_controllers/motionActionResult:actionlib_msgs/GoalStatus:pioneer2dx_controllers/motionActionFeedback"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_cpp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_cpp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_cpp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_cpp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_cpp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_cpp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pioneer2dx_controllers
)

### Generating Services
_generate_srv_cpp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer2dx/pioneer2dx_controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pioneer2dx_controllers
)

### Generating Module File
_generate_module_cpp(pioneer2dx_controllers
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pioneer2dx_controllers
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(pioneer2dx_controllers_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(pioneer2dx_controllers_generate_messages pioneer2dx_controllers_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_cpp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_cpp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer2dx/pioneer2dx_controllers/srv/motion.srv" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_cpp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_cpp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_cpp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_cpp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_cpp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_cpp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pioneer2dx_controllers_gencpp)
add_dependencies(pioneer2dx_controllers_gencpp pioneer2dx_controllers_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pioneer2dx_controllers_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_eus(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_eus(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_eus(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_eus(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_eus(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_eus(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pioneer2dx_controllers
)

### Generating Services
_generate_srv_eus(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer2dx/pioneer2dx_controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pioneer2dx_controllers
)

### Generating Module File
_generate_module_eus(pioneer2dx_controllers
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pioneer2dx_controllers
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(pioneer2dx_controllers_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(pioneer2dx_controllers_generate_messages pioneer2dx_controllers_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_eus _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_eus _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer2dx/pioneer2dx_controllers/srv/motion.srv" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_eus _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_eus _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_eus _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_eus _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_eus _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_eus _pioneer2dx_controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pioneer2dx_controllers_geneus)
add_dependencies(pioneer2dx_controllers_geneus pioneer2dx_controllers_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pioneer2dx_controllers_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_lisp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_lisp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_lisp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_lisp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_lisp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_lisp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pioneer2dx_controllers
)

### Generating Services
_generate_srv_lisp(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer2dx/pioneer2dx_controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pioneer2dx_controllers
)

### Generating Module File
_generate_module_lisp(pioneer2dx_controllers
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pioneer2dx_controllers
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(pioneer2dx_controllers_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(pioneer2dx_controllers_generate_messages pioneer2dx_controllers_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_lisp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_lisp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer2dx/pioneer2dx_controllers/srv/motion.srv" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_lisp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_lisp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_lisp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_lisp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_lisp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_lisp _pioneer2dx_controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pioneer2dx_controllers_genlisp)
add_dependencies(pioneer2dx_controllers_genlisp pioneer2dx_controllers_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pioneer2dx_controllers_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_nodejs(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_nodejs(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_nodejs(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_nodejs(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_nodejs(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_nodejs(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pioneer2dx_controllers
)

### Generating Services
_generate_srv_nodejs(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer2dx/pioneer2dx_controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pioneer2dx_controllers
)

### Generating Module File
_generate_module_nodejs(pioneer2dx_controllers
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pioneer2dx_controllers
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(pioneer2dx_controllers_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(pioneer2dx_controllers_generate_messages pioneer2dx_controllers_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_nodejs _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_nodejs _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer2dx/pioneer2dx_controllers/srv/motion.srv" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_nodejs _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_nodejs _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_nodejs _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_nodejs _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_nodejs _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_nodejs _pioneer2dx_controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pioneer2dx_controllers_gennodejs)
add_dependencies(pioneer2dx_controllers_gennodejs pioneer2dx_controllers_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pioneer2dx_controllers_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_py(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg"
  "${MSG_I_FLAGS}"
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_py(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_py(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_py(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_py(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pioneer2dx_controllers
)
_generate_msg_py(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pioneer2dx_controllers
)

### Generating Services
_generate_srv_py(pioneer2dx_controllers
  "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer2dx/pioneer2dx_controllers/srv/motion.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pioneer2dx_controllers
)

### Generating Module File
_generate_module_py(pioneer2dx_controllers
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pioneer2dx_controllers
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(pioneer2dx_controllers_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(pioneer2dx_controllers_generate_messages pioneer2dx_controllers_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionFeedback.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_py _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionResult.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_py _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer2dx/pioneer2dx_controllers/srv/motion.srv" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_py _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionFeedback.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_py _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionGoal.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_py _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionActionGoal.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_py _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionResult.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_py _pioneer2dx_controllers_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/devel/share/pioneer2dx_controllers/msg/motionAction.msg" NAME_WE)
add_dependencies(pioneer2dx_controllers_generate_messages_py _pioneer2dx_controllers_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pioneer2dx_controllers_genpy)
add_dependencies(pioneer2dx_controllers_genpy pioneer2dx_controllers_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pioneer2dx_controllers_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pioneer2dx_controllers)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pioneer2dx_controllers
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(pioneer2dx_controllers_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET actionlib_msgs_generate_messages_cpp)
  add_dependencies(pioneer2dx_controllers_generate_messages_cpp actionlib_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pioneer2dx_controllers)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pioneer2dx_controllers
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(pioneer2dx_controllers_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET actionlib_msgs_generate_messages_eus)
  add_dependencies(pioneer2dx_controllers_generate_messages_eus actionlib_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pioneer2dx_controllers)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pioneer2dx_controllers
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(pioneer2dx_controllers_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET actionlib_msgs_generate_messages_lisp)
  add_dependencies(pioneer2dx_controllers_generate_messages_lisp actionlib_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pioneer2dx_controllers)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pioneer2dx_controllers
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(pioneer2dx_controllers_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET actionlib_msgs_generate_messages_nodejs)
  add_dependencies(pioneer2dx_controllers_generate_messages_nodejs actionlib_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pioneer2dx_controllers)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pioneer2dx_controllers\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pioneer2dx_controllers
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(pioneer2dx_controllers_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET actionlib_msgs_generate_messages_py)
  add_dependencies(pioneer2dx_controllers_generate_messages_py actionlib_msgs_generate_messages_py)
endif()
