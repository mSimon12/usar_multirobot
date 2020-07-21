#! /usr/bin/env python

import rospy
import time

from pioneer3at_controllers.msg import events_message

def callback(msg):
    print(msg)

if __name__ == '__main__':
    try:

        rospy.init_node('teste', anonymous=False)                                 # Initialize the node of the sensor
        print("Ola")
        pub = rospy.Publisher("/pioneer3at_1/victim_sensor/out", events_message, queue_size=10)        # Topic to receive occured events
        msg = events_message()
        msg.event = 'calabresa'
        msg.param = [10.5, 5, 10]

        while not rospy.is_shutdown():
            pub.publish(msg)
            time.sleep(1)


        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass
