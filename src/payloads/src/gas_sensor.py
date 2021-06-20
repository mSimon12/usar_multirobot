#!/usr/bin/env python

import rospy
from threading import Thread
from copy import deepcopy

# ROS
from gazebo_msgs.srv import GetModelState
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from system_msgs.msg import events_message

class GasSensor(object):

    def __init__(self):
        self.__state = 'GS_OFF'
        self.__current_pose = Twist()
        self.__points_with_gas = []                                                                     # Array with points with gas

        # Get parameters
        self.__update_radius = rospy.get_param('gas_update_radius', default=3.0)                        # Radius in wich the robot does not republish gas leak
        self.__robot_name = rospy.get_param('robot_name', default='robot')
        self.__gas_models = rospy.get_param('gas_models', default=[])
        self.__sensor_range = rospy.get_param('gs_sensor_range', default=1.0)
        self.__sensor_update_rate = rospy.get_param('gs_sensor_update_rate', default=1.0)

        self.__models_service = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)             # Get model service from Gazebo
        self.__models_service.wait_for_service()

        self.__pub = rospy.Publisher("gas_sensor/out", events_message, queue_size=10)
        rospy.Subscriber("odom", Odometry, self.robot_pose)                                              # Topic to monitor robot position
        rospy.Subscriber("gas_sensor/in", events_message, self.event_receiver)                           # Topic to receive occured events


    def robot_pose(self, msg):
        '''
            Periodically update robot position according the Odometry
        '''
        self.__current_pose.linear.x = msg.pose.pose.position.x 
        self.__current_pose.linear.y = msg.pose.pose.position.y  

    def event_receiver(self, msg):
        '''
            Callback for received messages. Responsible for changing the sensor state
        '''
        if (msg.event == 'start') and (self.__state == 'GS_OFF'):
            self.__state = 'GS_ON'
            thread = Thread(target = self.gs_on)
            thread.start()                                                  # Start the sensor
        elif (msg.event == 'stop') and (self.__state == 'GS_ON'):
            self.__state = 'GS_OFF'                                         # Stop the sensor
        elif (msg.event == 'erro') and (self.__state == 'GS_ON'):
            self.__state = 'GS_ERROR'                                       # Stop the sensor to simulate that it is not working
            self.__pub.publish(msg)                                         # Re-send the msg to the output 
        elif (msg.event == 'reset') and (self.__state == 'GS_ERROR'):
            self.__state = 'GS_OFF'                                         # Reset the sensor
            self.__pub.publish(msg)                                         # Re-send the msg to the output
        else:
            rospy.logwarn("GAS_SENSOR command not allowed!")

    def gs_on(self):
        '''
            Function for gas recognition
        '''
        rate = rospy.Rate(self.__sensor_update_rate)
        while (not rospy.is_shutdown()) and (self.__state == 'GS_ON'): 
            sensor = self.__find_gas()
            for g in sensor:
                if sensor[g]['status'] == True:
                    # Verify if is a new point to publish
                    if self.__points_with_gas:
                        count = 0
                        for point in self.__points_with_gas:
                            dist = ((self.__current_pose.linear.x - point.linear.x)**2 + (self.__current_pose.linear.y - point.linear.y)**2)**(0.5)
                            if dist < self.__update_radius:
                                break
                            else:
                                count += 1
                        if count == len(self.__points_with_gas):
                            # Send the signal that a gas leak have been found and its location 
                            self.__points_with_gas.append(deepcopy(self.__current_pose))
                            msg = events_message()
                            msg.event = 'gas_leak'
                            msg.position.append(self.__current_pose)
                            self.__pub.publish(msg)                                                    # Publish the found gas location
                    else:
                        # Send the signal that a gas leak have been found and its location 
                        self.__points_with_gas.append(deepcopy(self.__current_pose))
                        msg = events_message()
                        msg.event = 'gas_leak'
                        msg.position.append(self.__current_pose)
                        self.__pub.publish(msg)                                                         # Publish the found gas location

            rate.sleep()

    def __find_gas(self):
        '''
            Function to verify if a gas_leak from the list is into the range of the sensor
            robot_name: name of the robot model on Gazebo
            gas_models: list of gas models on Gazebo
            sensor_range: range in which the robot recognize a gas_leak
        '''
        # Get position of the victims related to the robot position
        g_status = {}                                                                # Dictionary with the status of each victim and xyz position
        for v in self.__gas_models:
            try:
                g_status[v] = {}
                answer = self.__models_service(v, self.__robot_name)                        # Call the service to receive the victim position
                g_status[v]['x_pos'] = answer.pose.position.x
                g_status[v]['y_pos'] = answer.pose.position.y
                g_status[v]['z_pos'] = answer.pose.position.z

                # Find the distance between robot and victim
                hip = (g_status[v]['x_pos']**2 + g_status[v]['y_pos']**2)**(0.5)
                dist = (hip**2 + g_status[v]['z_pos']**2)**(0.5)

                # Mark the victim as found if it is into the range
                if dist < self.__sensor_range:
                    g_status[v]['status'] = True
                else:
                    g_status[v]['status'] = False

            except rospy.ServiceException as e:
                rospy.loginfo("Get Model State service call failed:  {}".format(e))

        return g_status                                                               # Return the status of all victims

if __name__ == '__main__':
    try:
        rospy.init_node('gas_sensor', anonymous=False)                  # Initialize the node of the sensor
        gs = GasSensor()                                                # Initialize Gas Sensor
        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass
