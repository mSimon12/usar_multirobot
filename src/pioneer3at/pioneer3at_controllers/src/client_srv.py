#!/usr/bin/env python

import sys
import rospy
from geometry_msgs.msg import Twist
from pioneer3at_controllers.srv import motion

def client(name, dest):
    rospy.init_node('client',anonymous=True)
    rospy.wait_for_service("/{}/move".format(name))     #Service name = robot_name/move 

    service_call = rospy.ServiceProxy("/{}/move".format(name),motion)       # Send a Twist position
    try:
        res = service_call(dest)
        rospy.loginfo("Result = {}".format(res))
    except rospy.ROSInterruptException:
        pass

if __name__=="__main__":
    if len(sys.argv)==5:
        name = sys.argv[1]

        dest = Twist()
        dest.linear.x = float(sys.argv[2]) 
        dest.linear.y = float(sys.argv[3])
        dest.angular.z = float(sys.argv[4])
        client(name, dest)
    else:
        print("Wrong statement.")
