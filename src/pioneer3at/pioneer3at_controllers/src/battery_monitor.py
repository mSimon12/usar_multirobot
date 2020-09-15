#!/usr/bin/env python
import time
import rospy
from threading import Thread

from geometry_msgs.msg import Twist
from actionlib import GoalStatus
from system_msgs.msg import events_message

class BatteryMonitor(Thread):

    def __init__(self):
        Thread.__init__(self)
        # Get parameters
        self.upd_rate = 10.0                                                             # Rate in which the battery level is updated
        self.pub_rate = rospy.get_param('publish_rate', default = 1.0)                   # Rate in which the battery level is published

        #Variables for battery consumption simulation
        self.battery_level = 100                                                         # Battery level percent
        # Weights for move and sensors on battery consumption
        self.__weights = {'move': 0.0035,
                          'victim_sensor': 0.0009, 
                          'gas_sensor': 0.0005}                                                 
        self.__sensors_status = {'victim_sensor': False, 'gas_sensor': False}       # Variable to know sensor status

        # Message object
        self.msg = events_message()                                                                              
        self.msg.event = 'battery_level'
        self.msg.param.append(self.battery_level)

        # Publisher object for periodically sending battery level
        self.pub = rospy.Publisher("battery_monitor/out", events_message, queue_size=10)       

        rospy.Subscriber("battery_monitor/in", events_message, self.event_receiver)            # Topic to receive occured events
        rospy.Subscriber("victim_sensor/in", events_message, self.victim_sensor_status)        # Topic to monitor victim sensor status
        rospy.Subscriber("gas_sensor/in", events_message, self.gas_sensor_status)              # Topic to monitor gas sensor status

        self.time = -10
        rospy.Subscriber("cmd_vel", Twist, self.move_status)                                   # Topic to monitor cmd_vel messages
        

    def run(self):
        #Monitor the battery level
        rate = rospy.Rate(self.upd_rate)                                # Rate of battery update
        count = 0
        while not rospy.is_shutdown():
            count += 1
            bat_delta = 0
            if self.__sensors_status['victim_sensor']:
                bat_delta += self.__weights['victim_sensor']

            if self.__sensors_status['gas_sensor']:
                bat_delta += self.__weights['gas_sensor']

            # If the last update of cmd_vel was less then 4 seconds it consider the robot on motion
            t = rospy.get_time()
            if (t - self.time) < 4.0: 
                bat_delta += self.__weights['move']
            
            self.battery_level -= bat_delta                             # Update battery level

            # Delimitate to positive values [0,100]
            if self.battery_level > 100:
                self.battery_level = 100
            elif self.battery_level < 0:
                self.battery_level = 0

            if count >= (self.upd_rate/self.pub_rate):
                self.msg.param[0] = self.battery_level
                self.pub.publish(self.msg)                              # Publish the battery level
                count = 0
            
            rate.sleep()                                                # Wait to ensure loop frequency

    # Callback to verify victim_sensor status
    def victim_sensor_status(self, msg):
        if msg.event == 'start':
            self.__sensors_status['victim_sensor'] = True
        elif (msg.event == 'stop') or (msg.event == 'reset'):
            self.__sensors_status['victim_sensor'] = False

    # Callback to verify gas_sensor status
    def gas_sensor_status(self, msg):
        if msg.event == 'start':
            self.__sensors_status['gas_sensor'] = True
        elif (msg.event == 'stop') or (msg.event == 'reset'):
            self.__sensors_status['gas_sensor'] = False

    # Callback to verify motion status
    def move_status(self, msg):
        self.time = rospy.get_time()

    def event_receiver(self, msg):
        #Receive battery level
        if msg.event == 'battery_level':
            if msg.param:
                self.battery_level = msg.param[0]


if __name__ == '__main__':
    try:   
        rospy.init_node('battery_monitor', anonymous=False)                 # Initialize the node of the sensor

        bat_monitor = BatteryMonitor()
        bat_monitor.start()                                                 # Start battery monitor thread

        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass