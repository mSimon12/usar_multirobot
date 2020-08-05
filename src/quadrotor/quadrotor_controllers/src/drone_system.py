#!/usr/bin/env python2.7

import sys
import roslib
roslib.load_manifest('quadrotor_controllers')
import rospy
import actionlib
from tf.transformations import quaternion_from_euler

from hector_uav_msgs.msg import PoseAction, PoseGoal

class droneSys(object):
    
    def __init__(self, name):
        self.__drone_name = name
        rospy.init_node("{}_client".format(name), anonymous=False)
        self.__client = actionlib.SimpleActionClient("/{}/action/pose".format(name), PoseAction)     #Server name = robot_name/pose
        self.__client.wait_for_server()
        self.__dest = PoseGoal()
        self.__dest.target_pose.header.frame_id = "earth"

    

    def go_to(self, x, y, z, theta):
        '''
            Require de drone to move to a specific point (x,y,z,theta)
        '''
        self.__dest.target_pose.pose.position.x = x
        self.__dest.target_pose.pose.position.y = y
        self.__dest.target_pose.pose.position.z = z

        (rot_x, rot_y, rot_z, rot_w) = quaternion_from_euler(0, 0, theta, axes='sxyz')    # convert to quaternion

        self.__dest.target_pose.pose.orientation.x = rot_x
        self.__dest.target_pose.pose.orientation.y = rot_y
        self.__dest.target_pose.pose.orientation.z = rot_z
        self.__dest.target_pose.pose.orientation.w = rot_w

        # Fill in the goal here
        self.__client.send_goal(self.__dest)
        # self.__client.wait_for_result(rospy.Duration(5.0))


if __name__=="__main__":
    if len(sys.argv) == 6:
        system = droneSys(sys.argv[1])

        system.go_to(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))
    else:
        print("Wrong statement.")
