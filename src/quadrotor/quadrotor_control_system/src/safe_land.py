#!/usr/bin/env python2.7

import copy
from threading import Condition
from math import sqrt, atan

import rospy
import roslib
roslib.load_manifest('quadrotor_control_system')

from tf.transformations import quaternion_from_euler

from sensor_msgs.msg import Range
from nav_msgs.msg import Odometry
# from geometry_msgs.msg import Pose

from actionlib import SimpleActionServer, SimpleActionClient, GoalStatus
from quadrotor_control_system.msg import ExecuteLandAction, ExecuteLandFeedback, ExecuteLandResult
from trajectory_action_pkg.msg import ExecuteDroneApproachAction, ExecuteDroneApproachGoal

from hector_uav_msgs.srv import EnableMotors, EnableMotorsRequest

from system_msgs.msg import events_message


class SafeLand(object):

    def __init__(self, height, safe_dist):
        self.quadrotor_height = height             # Height of the motion to the ground
        self.safe_dist = safe_dist                 # Distance the drone must maintain from a victim

        # Create safe_land server
        self.land_server = SimpleActionServer('safe_land_server', ExecuteLandAction, self.land_Callback, False)
        self.server_feedback = ExecuteLandFeedback()
        self.server_result = ExecuteLandResult()

        # Get client from trajectory server
        self.trajectory_client = SimpleActionClient("approach_server", ExecuteDroneApproachAction)
        self.trajectory_client.wait_for_server()

        self.point_to_go = ExecuteDroneApproachGoal()               # Message to define next position to look for victims

        # quadrotor motion service
        self.motors = rospy.ServiceProxy('enable_motors', EnableMotors)
        self.motors.wait_for_service()

        ## variables
        self.sonar_me = Condition()
        self.odometry_me = Condition()

        # Start trajectory server
        self.land_server.start()

    def land_Callback(self,msg):
        '''
            Execute a the landing of the drone by avoiding to land above victims
        '''
        self.current_height = None
        self.odometry = None

        # Subscribe to sonar_height
        sonar_sub = rospy.Subscriber("sonar_height", Range, self.sonar_callback, queue_size=10)

        # Subscribe to ground_truth to monitor the current pose of the robot
        odom_sub = rospy.Subscriber("ground_truth/state", Odometry, self.poseCallback)

        # Subscribe to victim sensor
        sensor_sub = rospy.Subscriber("victim_sensor/out",events_message, self.v_sensor_callback, queue_size=10)

        self.sonar_me.acquire()
        if not self.current_height:
            self.sonar_me.wait()

        self.odometry_me.acquire()
        if not self.odometry:
            self.odometry_me.wait()
        self.point_to_go.goal.position.x = self.odometry.position.x
        self.point_to_go.goal.position.y = self.odometry.position.y
        self.point_to_go.goal.position.z = self.odometry.position.z - self.current_height + self.quadrotor_height

        self.point_to_go.goal.orientation.x = self.odometry.orientation.x
        self.point_to_go.goal.orientation.y = self.odometry.orientation.y
        self.point_to_go.goal.orientation.z = self.odometry.orientation.z
        self.point_to_go.goal.orientation.w = self.odometry.orientation.w

        self.odometry_me.release()   
        self.sonar_me.release()

        state = None
        while not (state in [GoalStatus.SUCCEEDED, GoalStatus.ABORTED]): 
            # print(self.point_to_go)

            if self.land_server.is_preempt_requested():
                self.land_server.set_preempted(self.server_result)
                return

            self.trajectory_client.send_goal(self.point_to_go)
            self.trajectory_client.wait_for_result()                                                # Wait for the result
            state = self.trajectory_client.get_state()                                              # Get the state of the action

            if state == GoalStatus.SUCCEEDED:
                trials = 0

                self.sonar_me.acquire()
                self.odometry_me.acquire()
                if self.current_height > (self.quadrotor_height*1.20):

                    if not self.current_height:
                        self.sonar_me.wait()

                    if not self.odometry:
                        self.odometry_me.wait()

                    # quadrotor is too high from ground
                    self.point_to_go.goal.position.z = self.odometry.position.z - self.current_height + self.quadrotor_height
                    state = None
                else:
                    #Safe Land soccesfully executed
                    motors_msg = EnableMotorsRequest()
                    motors_msg.enable = False                   # Disable motors to make the drone land
                    self.motors.call(motors_msg)

                    # Send landed pose as result
                    self.odometry_me.wait()
                    self.server_result.land_pose = self.odometry
                    self.land_server.set_succeeded(self.server_result)
                self.odometry_me.release()
                self.sonar_me.release()

            elif result == GoalStatus.ABORTED:
                trials += 1
                if trials == 5:
                    self.exploration_server.set_aborted(self.server_result)
                    return  
            elif state == GoalStatus.ABORTED:
                self.land_server.set_aborted()

        sonar_sub.unregister()
        odom_sub.unregister()
        sensor_sub.unregister()
        # rospy.logwarn("ENDING safe land!")

        return

    def sonar_callback(self,msg):
        '''
            Function to update drone height
        '''
        self.sonar_me.acquire()
        self.current_height = msg.range

        if self.current_height < self.quadrotor_height*0.8:
            self.odometry_me.acquire()
            if not self.odometry:
                self.odometry_me.wait()
            self.point_to_go.goal.position.z = self.odometry.position.z - self.current_height + self.quadrotor_height
            self.odometry_me.release()
            self.trajectory_client.cancel_goal()
        self.sonar_me.notify()
        self.sonar_me.release()

    def poseCallback(self,odometry):
        '''
            Monitor the current position of the robot
        '''
        self.odometry_me.acquire()
        self.odometry = odometry.pose.pose
        self.odometry_me.notify_all()
        self.odometry_me.release()

    def v_sensor_callback(self,msg):
        '''
            Receive position of a detected victim
        '''
        self.sonar_me.acquire()
        actual_x = self.odometry.position.x
        actual_y = self.odometry.position.y
        self.sonar_me.release()

        victim_x = msg.position[0].linear.x
        victim_y = msg.position[0].linear.y

        dist = sqrt((actual_x - victim_x)**2 + (actual_y - victim_y)**2)
        if dist < self.safe_dist:
            self.point_to_go.goal.position.x = victim_x + (self.safe_dist/dist)*(actual_x - victim_x)
            self.point_to_go.goal.position.y = victim_y + (self.safe_dist/dist)*(actual_y - victim_y)
            rospy.logwarn("Replannig safe land!!!!")
            self.trajectory_client.cancel_all_goals()
            

if __name__=="__main__":
    NAME = rospy.get_param("robot_name", default = "")
    height = rospy.get_param("quad_h", default = "0.5")
    safe_dist = rospy.get_param("safe_dist", default = "3.0")

    rospy.init_node("safe_land_server", anonymous=False)           # Initialize explore node
    safe_land = SafeLand(height,safe_dist)

    rospy.spin()
