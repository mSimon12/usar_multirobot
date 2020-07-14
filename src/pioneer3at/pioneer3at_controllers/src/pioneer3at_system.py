#!/usr/bin/env python2.7

import roslib
roslib.load_manifest('pioneer3at_controllers')
import rospy
import actionlib

from tf.transformations import quaternion_from_euler
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pioneer3at_controllers.msg import events_message

class pioneerSys(object):
    
    def __init__(self, name):
        self.__robot_name = name

    def approach(self, x, y, theta):
        '''
            Require de robot to move to a specific point (x,y,theta)
        '''
        client = actionlib.SimpleActionClient("/{}/move_base".format(self.__robot_name), MoveBaseAction)     #Server name = robot_name/move_base
        client.wait_for_server()
        dest = MoveBaseGoal()

        dest.target_pose.header.frame_id = "earth"
        q = quaternion_from_euler(0,0,theta,'ryxz')
        dest.target_pose.pose.position.x = x
        dest.target_pose.pose.position.y = y
        dest.target_pose.pose.orientation.x = q[0]
        dest.target_pose.pose.orientation.y = q[1]
        dest.target_pose.pose.orientation.z = q[2]
        dest.target_pose.pose.orientation.w = q[3]
        
        client.send_goal(dest)        #Send the goal
        # client.wait_for_result(rospy.Duration(5.0))

def event_receiver(msg):
    global sys
    rospy.loginfo(msg)

    if msg.event == "approach":
        x = msg.param[0]
        y = msg.param[1]
        theta = msg.param[2]
        sys.approach(x, y, theta)

if __name__=="__main__":
    global sys
    NAME = rospy.get_param("robot_name", default="")
    sys = pioneerSys(NAME)
    
    rospy.init_node("{}_system".format(NAME), anonymous=False)
    rospy.Subscriber("/{}/events".format(NAME), events_message, event_receiver)         # Topic to receive desired position

    rospy.spin()

