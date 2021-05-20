#!/usr/bin/env python

import copy
import numpy
from numpy import arange
from math import sqrt, atan2
from threading import Condition

import rospy
import roslib
roslib.load_manifest('quadrotor_control_system')

from actionlib import SimpleActionServer, SimpleActionClient, GoalStatus
from trajectory_action_pkg.msg import ExecuteDroneApproachAction, ExecuteDroneApproachGoal

from moveit_msgs.srv import GetPlanningScene, GetPlanningSceneRequest
from moveit_msgs.msg import PlanningSceneComponents

from sensor_msgs.msg import Range
from nav_msgs.msg import Odometry

from quadrotor_control_system.msg import ExecuteAssesstAction, ExecuteAssesstFeedback, ExecuteAssesstResult

from frontiers.srv import Frontiers, FrontiersRequest
from geometry_msgs.msg import Pose

from octomap import OcTree

class Explore(object):

    def __init__(self, height):

        self.motion_height = height             # Height of the motion to the ground

        # Create trajectory server
        self.exploration_server = SimpleActionServer('assessment_server', ExecuteAssesstAction, self.exploreCallback, False)
        self.server_feedback = ExecuteAssesstFeedback()
        self.server_result = ExecuteAssesstResult()

        # Get client from trajectory server
        self.trajectory_client = SimpleActionClient("approach_server", ExecuteDroneApproachAction)
        self.trajectory_client.wait_for_server()

        self.next_point = ExecuteDroneApproachGoal()               # Message to define next position to look for victims

        #Planning scene client
        self.frontiers_client = rospy.ServiceProxy('frontiers_server/find', Frontiers)
        self.frontiers_client.wait_for_service()

        self.frontiers_req = FrontiersRequest()          #Frontiers request message

        # Variables
        self.sonar_me = Condition()
        self.odometry_me = Condition()

        self.current_height = None
        self.odometry = None

        # Subscribe to sonar_height
        rospy.Subscriber("sonar_height", Range, self.sonar_callback, queue_size=10)

        # Subscribe to ground_truth to monitor the current pose of the robot
        rospy.Subscriber("ground_truth/state", Odometry, self.poseCallback)

        self.scene_req = GetPlanningSceneRequest()

        # Start trajectory server
        self.exploration_server.start()


    def sonar_callback(self,msg):
        '''
            Function to update drone height
        '''
        self.sonar_me.acquire()
        self.current_height = msg.range
        self.sonar_me.release()


    def poseCallback(self,odometry):
        '''
            Monitor the current position of the robot
        '''
        self.odometry_me.acquire()
        self.odometry = odometry.pose.pose
        self.odometry_me.notify()
        self.odometry_me.release()


    def trajectory_feed(self,msg):
        '''
            Verifies preemption requisitions
        '''
        print("\n\n\nASSESSMENT FEEDBACK")
        if self.exploration_server.is_preempt_requested():
            self.trajectory_client.cancel_goal()

    def exploreCallback(self,pose):
        '''
            Execute a loop looking for frontiers and moving to points unvisited into the defined area
        '''
        # Wait till the robot pose is received
        self.odometry_me.acquire()
        while self.odometry == None:
            self.odometry_me.wait()

        self.next_point.goal = self.odometry
        self.odometry_me.release()

        self.frontiers_req.x_min = 0.0
        self.frontiers_req.x_max = 50.0
        self.frontiers_req.y_min = 0.0
        self.frontiers_req.y_max = 50.0

        trials = 0                                              # v_search trials

        while not rospy.is_shutdown():

            self.odometry_me.acquire()
            self.server_result.last_pose = self.odometry
            self.server_feedback.current_pose = self.odometry
            self.odometry_me.release()
            
            if self.exploration_server.is_preempt_requested():
                self.exploration_server.set_preempted(self.server_result)
                return

            self.exploration_server.publish_feedback(self.server_feedback)

            self.sonar_me.acquire()
            # print("Current height from ground:\n\n{}".format(self.current_height))                        # Current distance from ground
            h_error = self.motion_height - self.current_height
            self.sonar_me.release()

            self.odometry_me.acquire()
            self.next_point.goal.position.z = self.odometry.position.z + h_error        # Desired z position
            self.odometry_me.release()

            self.trajectory_client.send_goal(self.next_point, feedback_cb = self.trajectory_feed)
            self.trajectory_client.wait_for_result()                                                # Wait for the result
            result = self.trajectory_client.get_state()                                             # Get the state of the action
            # print(result)

            if result == GoalStatus.SUCCEEDED:
                p = Pose()
                self.odometry_me.acquire()
                p = self.odometry
                self.frontiers_req.explored.append(p)
                self.odometry_me.release()

                # Verify if all the area have been explored and find next frontier point if needed
                # if 'all area explored':
                #     self.odometry_me.acquire()
                #     self.server_result.last_pose = self.odometry
                #     self.odometry_me.release()

                #     self.exploration_server.set_succeeded(self.server_result)
                
                status = self.findFrontiers()
                if not status:
                    self.exploration_server.set_succeeded(self.server_result)
                    return

                self.odometry_me.acquire()
                self.server_result.last_pose = self.odometry
                self.odometry_me.release()


                

                # self.next_point.goal.position.y =
                # self.next_point.goal.position.x =
                # theta =

                # Convert desired angle
                # q = quaternion_from_euler(0,0,theta,'ryxz')
                # self.next_point.goal.orientation.x = q[0]
                # self.next_point.goal.orientation.y = q[1]
                # self.next_point.goal.orientation.z = q[2]
                # self.next_point.goal.orientation.w = q[3]
            
            elif result == GoalStatus.ABORTED:
                trials += 1
                if trials == 2:
                    self.exploration_server.set_aborted(self.server_result)
                    return


    def findFrontiers(self):
        ''' 
            Return points not visited into the specified frontier
        '''
        rospy.loginfo("Looking for frontiers!")

        frontiers = self.frontiers_client.call(self.frontiers_req)

        if frontiers.frontiers: 
            self.next_point.goal.position.x = frontiers.frontiers[0].x
            self.next_point.goal.position.y = frontiers.frontiers[0].y
            self.next_point.goal.position.x = self.motion_height
            return True
        else:
            return False


if __name__=="__main__":
    # NAME = rospy.get_param("robot_name", default = "")
    height = float(rospy.get_param("height", default = "3.0"))

    rospy.init_node("explore_server", anonymous=False)           # Initialize explore node
    exp = Explore(height)

    rospy.spin()
