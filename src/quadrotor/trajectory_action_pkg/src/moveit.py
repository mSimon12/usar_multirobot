#!/usr/bin/env python2.7

import copy
import rospy
from threading import Condition, Thread

from actionlib import SimpleActionClient, GoalStatus
from std_msgs.msg import Header
from actionlib_msgs.msg import GoalID

from moveit_msgs.msg import MoveGroupAction, MoveGroupGoal, MotionPlanRequest, Constraints, JointConstraint 
from moveit_msgs.msg import PlanningScene, PlanningSceneComponents, AllowedCollisionEntry
from moveit_msgs.srv import GetPlanningScene, GetPlanningSceneRequest

from geometry_msgs.msg import Pose
from octomap_msgs.msg import Octomap
from nav_msgs.msg import Odometry


class MoveGroup(object):

    def __init__(self, frame, ns = ''):
        # self.scene_pub = PlanningScenePublisher(ns)

        self.move_group_client = SimpleActionClient("/{}/move_group".format(ns), MoveGroupAction)     
        self.move_group_client.wait_for_server()
        
        self.move_group_msg = MoveGroupGoal()

        #Create the message for the request
        self.move_group_msg.request = MotionPlanRequest()

        self.move_group_msg.request.workspace_parameters.header.frame_id = frame
        self.move_group_msg.request.workspace_parameters.min_corner.x = -50
        self.move_group_msg.request.workspace_parameters.min_corner.y = -50
        self.move_group_msg.request.workspace_parameters.min_corner.z = 0
        self.move_group_msg.request.workspace_parameters.max_corner.x = 50
        self.move_group_msg.request.workspace_parameters.max_corner.y = 50
        self.move_group_msg.request.workspace_parameters.max_corner.z = 50

        # Target definition      
        self.move_group_msg.request.goal_constraints.append(Constraints())

        self.constraints = JointConstraint()
        self.constraints.tolerance_above = 0.001
        self.constraints.tolerance_below = 0.001
        self.constraints.weight = 1.0

        for i in range(0,7):
            self.move_group_msg.request.goal_constraints[0].joint_constraints.append(copy.deepcopy(self.constraints))

        self.move_group_msg.planning_options.planning_scene_diff.is_diff = True
        self.move_group_msg.planning_options.plan_only = True

    def set_planner(self, planner_id = 'RRTConnectkConfigDefault', group = 'DroneBody', attempts = 10, allowed_time = 5):
        self.move_group_msg.request.planner_id = planner_id
        self.move_group_msg.request.group_name = group
        self.move_group_msg.request.num_planning_attempts = attempts
        self.move_group_msg.request.allowed_planning_time = allowed_time
        self.move_group_msg.request.max_velocity_scaling_factor = 1.0
        self.move_group_msg.request.max_acceleration_scaling_factor = 0.5  

    def set_start_state(self, robot_state):
        self.move_group_msg.request.start_state = robot_state

    def set_workspace(self,limits): 
        '''
            Workspace limits [XMIN,YMIN,ZMIN,XMAX,YMAX,ZMAX]
        '''
        self.move_group_msg.request.workspace_parameters.min_corner.x = limits[0]
        self.move_group_msg.request.workspace_parameters.min_corner.y = limits[1]
        self.move_group_msg.request.workspace_parameters.min_corner.z = limits[2]
        self.move_group_msg.request.workspace_parameters.max_corner.x = limits[3]
        self.move_group_msg.request.workspace_parameters.max_corner.y = limits[4]
        self.move_group_msg.request.workspace_parameters.max_corner.z = limits[5]
        
        # self.scene_pub.publishScene(robot_state)

    def set_target(self,target):
        self.move_group_msg.request.goal_constraints[0].joint_constraints[0].joint_name = "virtual_joint/trans_x"
        self.move_group_msg.request.goal_constraints[0].joint_constraints[0].position = target[0]

        self.move_group_msg.request.goal_constraints[0].joint_constraints[1].joint_name = "virtual_joint/trans_y"
        self.move_group_msg.request.goal_constraints[0].joint_constraints[1].position = target[1]

        self.move_group_msg.request.goal_constraints[0].joint_constraints[2].joint_name = "virtual_joint/trans_z"
        self.move_group_msg.request.goal_constraints[0].joint_constraints[2].position = target[2]

        self.move_group_msg.request.goal_constraints[0].joint_constraints[3].joint_name = "virtual_joint/rot_x"
        self.move_group_msg.request.goal_constraints[0].joint_constraints[3].position = target[3]

        self.move_group_msg.request.goal_constraints[0].joint_constraints[4].joint_name = "virtual_joint/rot_y"
        self.move_group_msg.request.goal_constraints[0].joint_constraints[4].position = target[4]

        self.move_group_msg.request.goal_constraints[0].joint_constraints[5].joint_name = "virtual_joint/rot_z"
        self.move_group_msg.request.goal_constraints[0].joint_constraints[5].position = target[5]

        self.move_group_msg.request.goal_constraints[0].joint_constraints[6].joint_name = "virtual_joint/rot_w"
        self.move_group_msg.request.goal_constraints[0].joint_constraints[6].position = target[6]
    
    def plan(self):

        # print("\nMOVE_GROUP_MSG:")
        # print(self.move_group_msg)

        self.move_group_client.send_goal(self.move_group_msg)
        self.move_group_client.wait_for_result()
        result = self.move_group_client.get_result()

        return result

    
class PlanningScenePublisher(object):

    def __init__(self, name, robot_state):
        self.drone_name = name
        self.current_state = robot_state

        self.scene_publisher = rospy.Publisher('/{}/planning_scene'.format(name), PlanningScene, queue_size=10)
        self.scene_msg = PlanningScene()
        self.scene_msg.name = "Drone_scene"

        self.scene_msg.world.octomap.header.frame_id = '{}/map'.format(name)
        self.scene_msg.world.octomap.origin = Pose()

        self.scene_msg.allowed_collision_matrix.entry_names = ["base_link", "camera_link", "sonar_link"]

        self.scene_msg.allowed_collision_matrix.entry_values.append(AllowedCollisionEntry())
        self.scene_msg.allowed_collision_matrix.entry_values[0].enabled = [False,False,True]

        self.scene_msg.allowed_collision_matrix.entry_values.append(AllowedCollisionEntry())
        self.scene_msg.allowed_collision_matrix.entry_values[1].enabled = [False,False,False]

        self.scene_msg.allowed_collision_matrix.entry_values.append(AllowedCollisionEntry())
        self.scene_msg.allowed_collision_matrix.entry_values[2].enabled = [True,False,False]

        self.odometry_me = Condition()
        self.octomap_me = Condition()

        # Subscribe to octomap topic
        self.octomap = None
        self.octo_sub = rospy.Subscriber("/{}/octomap_binary".format(self.drone_name),Octomap,self.octomap_callback, queue_size=10)

        # Subscribe to ground_truth to monitor the current pose of the robot
        self.odometry = None
        rospy.Subscriber("/{}/ground_truth/state".format(self.drone_name), Odometry, self.poseCallback)

        # x = Thread(target=self.publishScene)
        # rospy.loginfo("Starting Planning Scene Publisher")
        # x.start()


    def publishScene(self):

        # r = rospy.Rate(0.1)      # 1hz 
        # while not rospy.is_shutdown():
        self.odometry_me.acquire()
        while(not self.odometry):
            self.odometry_me.wait()

        # Update robot pose
        self.current_state.multi_dof_joint_state.transforms[0].translation.x = self.odometry.position.x
        self.current_state.multi_dof_joint_state.transforms[0].translation.y = self.odometry.position.y
        self.current_state.multi_dof_joint_state.transforms[0].translation.z = self.odometry.position.z
        self.current_state.multi_dof_joint_state.transforms[0].rotation.x = self.odometry.orientation.x
        self.current_state.multi_dof_joint_state.transforms[0].rotation.x = self.odometry.orientation.y
        self.current_state.multi_dof_joint_state.transforms[0].rotation.x = self.odometry.orientation.z
        self.current_state.multi_dof_joint_state.transforms[0].rotation.x = self.odometry.orientation.w

        # Set current scene
        self.scene_msg.robot_state = self.current_state
        self.odometry_me.release()

        self.octomap_me.acquire()
        
        # Wait updates on robot pose and octomap
        while(not self.octomap):
            self.octomap_me.wait()

        self.scene_msg.world.octomap.octomap = self.octomap
        self.octomap_me.release()

        # Publish the scene
        # rospy.loginfo("Publishing new scene!")
        self.scene_publisher.publish(self.scene_msg)
            
            # Wait time to ensure the rate of the publications
            # r.sleep()


    def octomap_callback(self, msg):
        '''
            Monitor the current octomap
        '''
        self.octomap_me.acquire()
        self.octomap = msg
        self.octomap.id="OcTree"
        self.octomap_me.notifyAll()
        self.octomap_me.release()


    def poseCallback(self,odometry):
        '''
            Monitor the current position of the robot
        '''
        self.odometry_me.acquire()
        self.odometry = odometry.pose.pose
        # print(self.odometry)
        self.odometry_me.notifyAll()
        self.odometry_me.release()
