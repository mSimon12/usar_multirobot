#!/usr/bin/env python

import os
import sys
import rospy

from system_msgs.msg import mission

from Mission import Mission


def start_publisher():
    # Get path to the current directory
    path = os.path.dirname(os.path.abspath(__file__))

    pub = rospy.Publisher('/missions', mission, queue_size=10)

    # Creates a mission ######################################
    m = Mission(sys.argv[1],sys.argv[2])

    task = m.get_std_task()
    task['agent'] = sys.argv[3]
    task['position'] = {'x': float(sys.argv[4]), 'y': float(sys.argv[5]), 'z': float(sys.argv[6]), 'theta': 0.0}
    task['vs'] = True
    task['maneuver'] = 'approach'

    task2 = m.get_std_task()
    task2['agent'] = sys.argv[3]
    task2['position'] = {'x': 1.0, 'y': 5.0, 'z': 0.0, 'theta': 3.14}
    task2['vs'] = True
    task2['maneuver'] = 'approach'

    m.add_task(task)
    m.add_task(task2)
    m.save(path + "/mission.xml")

    print("\nMISSION TASKS: \n{}\n\n".format(m.tasks))
    ##########################################################

    mission_msg = mission()
    mission_msg.id = sys.argv[1]
    mission_msg.filename = path + "/mission.xml"
    mission_msg.priority = int(sys.argv[2])

    #Publish mission message
    rospy.loginfo("Publishing mission!")
    rospy.loginfo(mission_msg)

    pub.publish(mission_msg)


if __name__ == '__main__':
    try:
        rospy.init_node('mission_assigner', anonymous=True)      # Initialize the node of the sensor

        start_publisher()

    except rospy.ROSInterruptException:
        pass
         
    
