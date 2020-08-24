#!/usr/bin/env python
import time
import rospy
from threading import Thread

from actionlib_msgs.msg import GoalStatusArray
from actionlib import GoalStatus
from quadrotor_controllers.msg import drone_events_message

class BatteryMonitor(Thread):

    def __init__(self):
        Thread.__init__(self)
        # Get parameters
        self.upd_rate = 10.0                                                             # Rate in which the battery level is updated
        self.pub_rate = rospy.get_param('publish_rate', default = 1.0)                   # Rate in which the battery level is published

        #Variables for battery consumption simulation
        self.battery_level = 100                                                    # Battery level percent
        # Weights for move and sensors on battery consumption
        self.__weights = {'move': 0.0035,
                          'victim_sensor': 0.0009, 
                          'gas_sensor': 0.0005}                                                 
        self.__sensors_status = {'move_base': False, 'victim_sensor': False, 'gas_sensor': False}       # Variable to know sensor status

        # Message object
        self.msg = drone_events_message()                                                                              
        self.msg.event = 'battery_level'
        self.msg.param.append(self.battery_level)

        # Publisher object for periodically sending battery level
        self.pub = rospy.Publisher("battery_monitor/out", drone_events_message, queue_size=10)       

        rospy.Subscriber("battery_monitor/in", drone_events_message, self.event_receiver)            # Topic to receive occured events
        rospy.Subscriber("victim_sensor/in", drone_events_message, self.victim_sensor_status)        # Topic to monitor victim sensor status
        rospy.Subscriber("gas_sensor/in", drone_events_message, self.gas_sensor_status)              # Topic to monitor gas sensor status
        rospy.Subscriber("move_base/status", GoalStatusArray, self.move_base_status)           # Topic to monitor move_base status

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

            if self.__sensors_status['move_base']: 
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

    def victim_sensor_status(self, msg):
        if msg.event == 'start':
            self.__sensors_status['victim_sensor'] = True
        elif (msg.event == 'stop') or (msg.event == 'reset'):
            self.__sensors_status['victim_sensor'] = False

    def gas_sensor_status(self, msg):
        if msg.event == 'start':
            self.__sensors_status['gas_sensor'] = True
        elif (msg.event == 'stop') or (msg.event == 'reset'):
            self.__sensors_status['gas_sensor'] = False

    def move_base_status(self, msg):
        try:
            if msg.status_list[0].status == GoalStatus.ACTIVE:
                self.__sensors_status['move_base'] = True
            else:
                self.__sensors_status['move_base'] = False
        except:
            self.__sensors_status['move_base'] = False

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