#!/usr/bin/env python
import rospy

from actionlib_msgs.msg import GoalStatusArray
from actionlib import GoalStatus
from system_msgs.msg import events_message

class FailuresMonitor(object):

    def __init__(self):
        self.state = 'NO_FAIL'                                                                  # Initial state
        
        # Publisher object for sending failures messages
        self.pub = rospy.Publisher("failures_monitor/out", events_message, queue_size=10)       
        rospy.Subscriber("failures_monitor/in", events_message, self.event_receiver)            # Topic to receive occured events

    def event_receiver(self, msg):
        # Reset failure monitor system
        if (msg.event == 'reset') and (self.state != 'NO_FAIL'):
            self.state = 'NO_FAIL'
            self.pub.publish(msg)                                                # Republish the message to the output
            return
        elif (msg.event == 'reset'):
            rospy.logwarn("Command not allowed!")
            return

        # Change Failure system state
        if (self.state == 'NO_FAIL'):
            if (msg.event == 'position_failure'):
                self.state = 'POS_F'
            elif (msg.event == 'slight_failure'):
                self.state = 'SIMP_F'
            elif (msg.event == 'critic_failure'):
                self.state = 'CRITIC_F'
            else:
                rospy.logwarn("Command not allowed!")
                return

        elif (self.state == 'SIMP_F'):
            if (msg.event == 'position_failure'):
                self.state = 'POS_F'
            elif (msg.event == 'critic_failure'):
                self.state = 'CRITIC_F'
            else:
                rospy.logwarn("Command not allowed!")
                return       

        elif (self.state == 'POS_F'):
            if (msg.event == 'critic_failure'):
                self.state = 'CRITIC_F'
            else:
                rospy.logwarn("Command not allowed!")
                return

        elif (self.state == 'CRITIC_F'):
            rospy.logwarn("Command not allowed!")
            return
        
        self.pub.publish(msg)                                                # Republish the message to the output


if __name__ == '__main__':
    try:   
        rospy.init_node('failures_monitor', anonymous=False)                 # Initialize the node of the sensor

        fail_monitor = FailuresMonitor()                                      # Failures monitor initialization
        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass