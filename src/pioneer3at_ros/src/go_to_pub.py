#!/usr/bin/env python

import rospy
from std_msgs.msg import String


def start_publisher():
    rospy.init_node('publisher', anonymous=True)
    pub = rospy.Publisher('chatter',String,queue_size=10)
    rospy.loginfo("Publisher ready")
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        msg = "{}: ding dong...".format(rospy.get_time())
        rospy.loginfo("Publishing...")
        pub.publish(msg)
        rate.sleep()



if __name__=='__main__':
    start_publisher()