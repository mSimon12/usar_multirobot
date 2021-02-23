#!/usr/bin/env python

from threading import Condition
import pandas as pd
import rospy

from Mission import Mission

from system_msgs.msg import abstractions, mission
from nav_msgs.msg import Odometry

if __name__ == '__main__':
    try:
        rospy.init_node('mission_assigner', anonymous=False)      # Initialize the node of the sensor

        # Creates a mission ######################################
        m = Mission("test_mission",2)

        task = m.get_std_task()
        task['agent'] = "pioneer3at_1"
        task['position'] = {'x': 1.0, 'y': 5.0, 'z': 0.0}
        task['vs'] = 'on'
        task['maneuver'] = 'approach'

        m.add_task(task)
        m.save("mission.xml")
        ##########################################################

        pub = rospy.Publisher('/missions', mission, queue_size=10)
        mission_msg = mission()
        mission_msg.id = "test_mission"
        mission_msg.filename = 'mission.xml'
        mission_msg.priority = 2

        #Publish mission message
        pub.publish(mission_msg)

        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass
