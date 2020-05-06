#!/usr/bin/env python

import sys
import rospy
from gazebo_msgs.srv import DeleteModel

def client(name):
    rospy.init_node('rescue_node',anonymous=True)
    rospy.wait_for_service("/gazebo/delete_model")     #Service to delete models

    # victim_del = DeleteModel()  
    # victim_del = name

    service_call = rospy.ServiceProxy("/gazebo/delete_model", DeleteModel)       # Send the victim to be deleted from gazebo
    try:
        res = service_call(name)
        if(res):
            rospy.loginfo("{} rescued!".format(name))
        else:
            rospy.loginfo("Not possible to rescue {}.".format(name))
    except rospy.ROSInterruptException:
        pass

if __name__=="__main__":
    if len(sys.argv)==2:
        victim = sys.argv[1]
        client(victim)
    else:
        print("Wrong statement.")