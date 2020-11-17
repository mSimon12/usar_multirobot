#!/usr/bin/env python2.7

import copy
from numpy import arange
from math import sqrt, atan2
from threading import Condition

import rospy
import roslib
roslib.load_manifest('quadrotor_controllers')



# from tf.transformations import euler_from_quaternion, quaternion_from_euler

from actionlib import SimpleActionServer, SimpleActionClient, GoalStatus
from trajectory_action_pkg.msg import ExecuteDroneApproachAction, ExecuteDroneApproachGoal

# from hector_uav_msgs.msg import PoseGoal, PoseAction

# from geometry_msgs.msg import Pose, Transform
# from nav_msgs.msg import Odometry

# from moveit_commander import RobotCommander, MoveGroupCommander
# from moveit_msgs.msg import RobotState, DisplayTrajectory
# from moveit_msgs.srv import  GetStateValidityRequest, GetStateValidity



class Explore(object):

    def __init__(self):
        # Mutual exclusion odometry
        self.odometry_me = Condition()

        # Create trajectory server
        self.exploration_server = SimpleActionServer('explore_server', ExecuteDroneApproachAction, self.exploreCallback, False)
        self.server_feedback = ExecuteDroneApproachFeedback()
        self.server_result = ExecuteDroneApproachResult()

        # Get client from trajectory server
        self.trajectory_client = SimpleActionClient("approach_server", ExecuteDroneApproachAction)
        self.trajectory_client.wait_for_server()

        # Start trajectory server
        self.exploration_server.start()


    def exploreCallback(self,pose):
        '''
            Execute a loop looking for frontiers and moving to points unvisited into the defined area
        '''
        pass


    def findFrontiers(self):
        ''' 
            Return points not visited into the specified frontier
        '''
        pass


if __name__=="__main__":
    # NAME = rospy.get_param("robot_name", default = "")

    rospy.init_node("explore_server", anonymous=False)           # Initialize explore node
    exp = Explore()

    rospy.spin()
