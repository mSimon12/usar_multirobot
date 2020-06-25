#!/usr/bin/env python2.7

import sys
import roslib
roslib.load_manifest('pioneer3at_controllers')
import rospy
import actionlib

from tf.transformations import quaternion_from_euler
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class pioneerSys(object):
    
    def __init__(self, name):
        self.__robot_name = name
        rospy.init_node("{}_client".format(name), anonymous=False)
        self.__client = actionlib.SimpleActionClient("/{}/move_base".format(name), MoveBaseAction)     #Server name = robot_name/move_base
        self.__client.wait_for_server()
        self.__dest = MoveBaseGoal()
    

    def go_to(self, x, y, theta):
        '''
            Require de robot to move to a specific point (x,y,theta)
        '''
        self.__dest.target_pose.header.frame_id = "earth"
        q = quaternion_from_euler(0,0,theta,'ryxz')
        self.__dest.target_pose.pose.position.x = x
        self.__dest.target_pose.pose.position.y = y
        self.__dest.target_pose.pose.orientation.x = q[0]
        self.__dest.target_pose.pose.orientation.y = q[1]
        self.__dest.target_pose.pose.orientation.z = q[2]
        self.__dest.target_pose.pose.orientation.w = q[3]
        
        self.__client.send_goal(self.__dest)        #Send the goal
        # self.__client.wait_for_result(rospy.Duration(5.0))


if __name__=="__main__":
    if len(sys.argv) == 5:
        system = pioneerSys(sys.argv[1])

        system.go_to(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
    else:
        print("Wrong statement.")
