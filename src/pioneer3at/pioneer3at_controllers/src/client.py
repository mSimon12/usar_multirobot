#!/usr/bin/env python

import sys
import roslib
roslib.load_manifest('controllers')
import rospy
import actionlib

from pioneer3at_controllers.msg import motionAction, motionGoal

def client(name, goal):
    rospy.init_node('client', anonymous=True)
    client = actionlib.SimpleActionClient("/{}/pose".format(name), motionAction)     #Server name = robot_name/pose
    client.wait_for_server()

    # Fill in the goal here
    client.send_goal(goal)
    # client.wait_for_result(rospy.Duration(5.0))

if __name__=="__main__":
    if len(sys.argv) == 5:
        name = sys.argv[1]

        dest = motionGoal()
        dest.destination.linear.x = float(sys.argv[2]) 
        dest.destination.linear.y = float(sys.argv[3])
        dest.destination.angular.z = float(sys.argv[4])
        client(name, dest)
    else:
        print("Wrong statement.")
