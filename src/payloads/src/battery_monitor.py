#!/usr/bin/env python
import time
import rospy
from threading import Thread

from actionlib_msgs.msg import GoalStatusArray
from actionlib import GoalStatus
from system_msgs.msg import events_message
from geometry_msgs.msg import Twist

class BatteryMonitor(Thread):

    def __init__(self):
        Thread.__init__(self)

        motion_topic = rospy.get_param("move_topic",default="move_base/status")         # Get name of topic to know that the robot is moving
        motion_w = rospy.get_param("move_consuption_weight",default="0.0035")        # Get the weight of motion on battery consuption
        victim_w = rospy.get_param("v_sensor_consuption_weight",default="0.0009")       # Get the weight of victim sensor on battery consuption
        gas_w = rospy.get_param("g_sensor_consuption_weight",default="0.0005")       # Get the weight of gas sensor on battery consuption

        # Get parameters
        self.upd_rate = 10.0                                                             # Rate in which the battery level is updated
        self.pub_rate = rospy.get_param('publish_rate', default = 1.0)                   # Rate in which the battery level is published

        #Variables for battery consumption simulation
        self.battery_level = 100                                                        # Battery level percent
        # Weights for move and sensors on battery consumption
        self.__weights = {'move': motion_w,
                          'victim_sensor': victim_w, 
                          'gas_sensor': gas_w}                                                 
        self.__sensors_status = {'move_base': False, 'victim_sensor': False, 'gas_sensor': False, 'cmd': False}       # Variable to know sensor status

        # Message object
        self.msg = events_message()                                                                              
        self.msg.event = 'battery_level'
        self.msg.param.append(self.battery_level)

        # Publisher object for periodically sending battery level
        self.pub = rospy.Publisher("battery_monitor/out", events_message, queue_size=10)       

        rospy.Subscriber("battery_monitor/in", events_message, self.event_receiver)            # Topic to receive occured events
        rospy.Subscriber("victim_sensor/in", events_message, self.victim_sensor_status)        # Topic to monitor victim sensor status
        rospy.Subscriber("gas_sensor/in", events_message, self.gas_sensor_status)              # Topic to monitor gas sensor status

        ##Topics to monitor motion
        rospy.Subscriber(motion_topic, GoalStatusArray, self.move_base_status)                 # Topic to monitor move_base status
        rospy.Subscriber("cmd_vel", Twist, self.cmd)                 # Topic to monitor move_base status

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

            if self.__sensors_status['move_base'] or self.__sensors_status['cmd']: 
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
            status = [(x.status == GoalStatus.ACTIVE) for x in msg.status_list]
            if status and any(status):
                self.__sensors_status['move_base'] = True
            else:
                self.__sensors_status['move_base'] = False
        except:
            self.__sensors_status['move_base'] = False

    def cmd(self, msg):

        if msg.linear.x:
            self.__sensors_status['cmd'] = True
        elif msg.linear.y:
            self.__sensors_status['cmd'] = True
        elif msg.linear.z:
            self.__sensors_status['cmd'] = True
        elif msg.angular.x:
            self.__sensors_status['cmd'] = True
        elif msg.angular.y:
            self.__sensors_status['cmd'] = True
        elif msg.angular.z:
            self.__sensors_status['cmd'] = True
        else:
            self.__sensors_status['cmd'] = False

    def event_receiver(self, msg):
        #Receive battery level
        if msg.event == 'battery_level':
            if msg.param:
                self.battery_level = msg.param[0]


if __name__ == '__main__':
    try:  
        rospy.init_node('battery_monitor', anonymous=False)                 # Initialize the node of the battery monitor

        bat_monitor = BatteryMonitor()
        bat_monitor.start()                                                 # Start battery monitor thread

        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass