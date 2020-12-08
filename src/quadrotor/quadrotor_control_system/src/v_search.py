#!/usr/bin/env python2.7

import copy
from numpy import arange
from math import sqrt, atan2, pi, ceil, sin, cos
from threading import Condition

import rospy
import roslib
roslib.load_manifest('quadrotor_control_system')

from tf.transformations import quaternion_from_euler

from sensor_msgs.msg import Range
from nav_msgs.msg import Odometry
# from geometry_msgs.msg import Pose

from actionlib import SimpleActionServer, SimpleActionClient, GoalStatus
from quadrotor_control_system.msg import ExecuteSearchAction, ExecuteSearchFeedback, ExecuteSearchResult
from trajectory_action_pkg.msg import ExecuteDroneApproachAction, ExecuteDroneApproachGoal


class V_search(object):

    def __init__(self, height, res):

        self.resolution = res                   # Resolution of the motion
        self.motion_height = height             # Height of the motion to the ground

        # Create search server
        self.search_server = SimpleActionServer('search_server', ExecuteSearchAction, self.searchCallback, False)
        self.server_feedback = ExecuteSearchFeedback()
        self.server_result = ExecuteSearchResult()

        # Get client from trajectory server
        self.trajectory_client = SimpleActionClient("approach_server", ExecuteDroneApproachAction)
        self.trajectory_client.wait_for_server()

        self.next_point = ExecuteDroneApproachGoal()               # Message to define next position to look for victims

        ## variables
        self.sonar_me = Condition()
        self.odometry_me = Condition()

        self.current_height = None
        self.odometry = None

        # Subscribe to sonar_height
        rospy.Subscriber("sonar_height", Range, self.sonar_callback, queue_size=10)

        # Subscribe to ground_truth to monitor the current pose of the robot
        rospy.Subscriber("ground_truth/state", Odometry, self.poseCallback)

        # Start trajectory server
        self.search_server.start()


    def searchCallback(self, search_area):
        '''
            Execute a search for vitims into the defined area
        '''
        x = search_area.x                                                                   # x size of the area to explore
        y = search_area.y                                                                   # y size of the area to explore
        start = search_area.origin                                                          # Point to start the search
        
        self.next_point.goal.position.x = start.x                                           # Desired x position
        self.next_point.goal.position.y = start.y                                           # Desired y position
        theta = 0

        # Convert desired angle
        q = quaternion_from_euler(0,0,theta,'ryxz')
        self.next_point.goal.orientation.x = q[0]
        self.next_point.goal.orientation.y = q[1]
        self.next_point.goal.orientation.z = q[2]
        self.next_point.goal.orientation.w = q[3]

        x_positions = ceil(x/self.resolution)
        y_positions = ceil(y/self.resolution)

        x_count = 0                                             # Counter of steps (in meters traveled)
        direction = 1                                           # Direction of the motion (right, left or up)
        trials = 0                                              # v_search trials

        while not rospy.is_shutdown():

            self.server_result.last_pose = self.odometry

            if self.search_server.is_preempt_requested():
                self.search_server.set_preempted(self.server_result)
                return

            self.server_feedback.current_pose = self.odometry
            self.search_server.publish_feedback(self.server_feedback)

            self.sonar_me.acquire()
            # print("Current height from ground:\n\n{}".format(self.current_height))                        # Current distance from ground
            h_error = self.motion_height - self.current_height
            self.sonar_me.release()

            self.odometry_me.acquire()
            self.next_point.goal.position.z = self.odometry.position.z + h_error        # Desired z position
            self.odometry_me.release()

            self.trajectory_client.send_goal(self.next_point)
            self.trajectory_client.wait_for_result()                                                # Wait for the result
            result = self.trajectory_client.get_state()                                             # Get the state of the action
            # print(result)


            if result == GoalStatus.SUCCEEDED:
                # Verifies if all the area have been searched
                if (self.next_point.goal.position.x == (start.x + x)) and ((self.next_point.goal.position.y == (start.y + y))):
                    self.search_server.set_succeeded(self.server_result)
                    return

                last_direction = direction
                direction = self.square_function(x_count, 2*x)                  # Get the direction of the next step

                if last_direction != direction:
                    # drone moves on y axis
                    theta = pi/2
                    self.next_point.goal.position.y += y/y_positions
                elif direction == 1:
                    # drone moves to the right
                    theta = 0
                    self.next_point.goal.position.x += x/x_positions
                    x_count += x/x_positions
                elif direction == -1:
                    # drone moves to the left
                    theta = pi
                    self.next_point.goal.position.x -= x/x_positions
                    x_count += x/x_positions

                # Convert desired angle
                q = quaternion_from_euler(0,0,theta,'ryxz')
                self.next_point.goal.orientation.x = q[0]
                self.next_point.goal.orientation.y = q[1]
                self.next_point.goal.orientation.z = q[2]
                self.next_point.goal.orientation.w = q[3]
            
            elif result == GoalStatus.ABORTED:
                trials += 1
                if trials == 2:
                    self.search_server.set_aborted(self.server_result)
                    return


    def square_function(self, x, max_x):
        '''
            Function to simulate a square wave function
        '''
        if round(sin(2*pi*x/max_x), 2) > 0:
            return 1
        elif round(sin(2*pi*x/max_x), 2)< 0:
            return -1
        else:
            if round(cos(2*pi*x/max_x), 2) > 0:
                return 1
            else:
                return -1

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
        self.odometry_me.release()


if __name__=="__main__":
    NAME = rospy.get_param("robot_name", default = "")
    resolution = float(rospy.get_param("resolution", default = "3.0"))
    height = float(rospy.get_param("height", default = "3.0"))

    rospy.init_node("search_server", anonymous=False)           # Initialize explore node
    search = V_search(height, resolution)

    rospy.spin()
