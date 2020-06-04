#!/usr/bin/env python

import sys
import roslib
roslib.load_manifest('pioneer2dx_controllers')
import rospy
import actionlib

from pioneer2dx_controllers.msg import motionAction, motionGoal


class pioneerSys(object):
    
    def __init__(self, name):
        self.__robot_name = name
        rospy.init_node("{}_client".format(name), anonymous=False)
        self.__client = actionlib.SimpleActionClient("/{}/pose".format(name), motionAction)     #Server name = robot_name/pose
        self.__client.wait_for_server()
        self.__dest = motionGoal()
    

    def go_to(self, x, y, theta):
        '''
            Require de robot to move to a specific point (x,y,theta)
        '''
        self.__dest.destination.linear.x = x 
        self.__dest.destination.linear.y = y
        self.__dest.destination.angular.z =theta
        # Fill in the goal here
        self.__client.send_goal(self.__dest)
        # self.__client.wait_for_result(rospy.Duration(5.0))


if __name__=="__main__":
    if len(sys.argv) == 5:
        system = pioneerSys(sys.argv[1])

        system.go_to(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
    else:
        print("Wrong statement.")
