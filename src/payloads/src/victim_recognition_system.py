#!/usr/bin/env python

import rospy
from threading import Thread

# ROS
from geometry_msgs.msg import Twist
from gazebo_msgs.srv import GetModelState
from system_msgs.msg import events_message

class VictimSensor(object):

    def __init__(self):
        self.__state = 'IDLE'

        # Get parameters
        self.__robot_name = rospy.get_param('robot_name', default='robot')
        self.__victims = rospy.get_param('victims_models', default=[])
        self.__sensor_range = rospy.get_param('sensor_range', default=1.0)
        self.__sensor_update_rate = rospy.get_param('sensor_update_rate', default=1.0)

        self.__models_service = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)                         # Get model service from Gazebo
        self.__models_service.wait_for_service()

        self.__pub = rospy.Publisher("victim_sensor/out", events_message, queue_size=10)
        rospy.Subscriber("victim_sensor/in", events_message, self.event_receiver)                                    # Topic to receive occured events
    

    def event_receiver(self, msg):
        '''
            Callback for received messages. Responsible for changing the sensor state
        '''
        if (msg.event == 'start') and (self.__state == 'IDLE'):
            self.__state = 'RUNNING'
            thread = Thread(target = self.vs_on)
            thread.start()                                              # Start the sensor
        elif (msg.event == 'stop') and (self.__state == 'RUNNING'):
            self.__state = 'IDLE'                                       # Stop the sensor
        elif (msg.event == 'erro') and (self.__state == 'RUNNING'):
            self.__state = 'ERROR'                                      # Stop the sensor to simulate that it is not working
            self.__pub.publish(msg)                                     # Re-send the msg to the output 
        elif (msg.event == 'reset') and (self.__state == 'ERROR'):
            self.__state = 'IDLE'                                       # Reset the sensor
        else:
            rospy.logwarn("VICTIM_SENSOR command not allowed!")

    def vs_on(self):
        '''
            Function for victim recognition
        '''
        rate = rospy.Rate(self.__sensor_update_rate)
        while (not rospy.is_shutdown()) and (self.__state == 'RUNNING'): 
            sensor = self.__find_victim()
            for v in sensor:
                if sensor[v]['status'] == True:
                    # Send the signal that a victim have been found and her location 
                    pos = self.__models_service(v, '')                                              # Call the service to receive the global victim position
    
                    # Create pose as pose2D
                    p = Twist()
                    p.linear.x = pos.pose.position.x
                    p.linear.y = pos.pose.position.y
                    p.linear.z = pos.pose.position.z

                    # Create message
                    msg = events_message()
                    msg.event = 'victim_recognized'
                    msg.position.append(p)
                    self.__pub.publish(msg)                                                         # Publish the found victim location 

                    self.__victims.remove(v)                                                        # Remove the found victim from the list

            rate.sleep()

    def __find_victim(self):
        '''
            Function to verify if a victim from the list is into the range of the sensor
            robot_name: name of the robot model on Gazebo
            victims: list of victims models on Gazebo
            sensor_range: range in which the robot recognize a victim
        '''
        # Get position of the victims related to the robot position
        v_status = {}                                                                # Dictionary with the status of each victim and xyz position
        for v in self.__victims:
            try:
                v_status[v] = {}
                answer = self.__models_service(v, self.__robot_name)                        # Call the service to receive the victim position
                v_status[v]['x_pos'] = answer.pose.position.x
                v_status[v]['y_pos'] = answer.pose.position.y
                v_status[v]['z_pos'] = answer.pose.position.z
            except rospy.ServiceException as e:
                rospy.loginfo("Get Model State service call failed:  {}".format(e))

            # Find the distance between robot and victim
            hip = (v_status[v]['x_pos']**2 + v_status[v]['y_pos']**2)**(1/2)
            dist = (hip**2 + v_status[v]['z_pos']**2)**(1/2)

            # Mark the victim as found if it is into the range
            if dist < self.__sensor_range:
                v_status[v]['status'] = True
            else:
                v_status[v]['status'] = False

        return v_status                                                               # Return the status of all victims


if __name__ == '__main__':
    try:
        rospy.init_node('victim_recognition_system', anonymous=False)   # Initialize the node of the sensor
        vs = VictimSensor()                                             # Initialize Victim Sensor
        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass
