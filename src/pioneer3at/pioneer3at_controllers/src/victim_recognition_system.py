#!/usr/bin/env python

import time
import rospy

from gazebo_msgs.srv import GetModelState
from pioneer3at_controllers.msg import events_message

def find_victim(robot_name, victims, sensor_range = 1):
    '''
        Function to verify if a victim from the list is into the range of the sensor
        robot_name: name of the robot model on Gazebo
        victims: list of victims models on Gazebo
        sensor_range: range in which the robot recognize a victim
    '''
    models_service = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)        # Get model service from Gazebo

    # Get position of the victims related to the robot position
    v_status = {}                                                                        # Dictionary with the status of each victim and xyz position
    for v in victims:
        try:
            v_status[v] = {}
            answer = models_service(v, robot_name)                                       # Call the service to receive the victim position
            v_status[v]['x_pos'] = answer.pose.position.x
            v_status[v]['y_pos'] = answer.pose.position.y
            v_status[v]['z_pos'] = answer.pose.position.z
        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {}".format(e))

        # Find the distance between robot and victim
        hip = (v_status[v]['x_pos']**2 + v_status[v]['y_pos']**2)**(1/2)
        dist = (hip**2 + v_status[v]['z_pos']**2)**(1/2)

        # Mark the victim as found if it is into the range
        if dist < sensor_range:
            v_status[v]['status'] = True
        else:
            v_status[v]['status'] = False

    return v_status         #Return the status of all victims


def event_receiver(msg):
    global status

    if (msg.event == 'start') and (status == 'idle'):
        status = 'running'
        vs_on()                                             #Start the sensor
    elif (msg.event == 'stop') and (status == 'running'):
        status = 'idle'                                     #Stop the sensor
    elif msg.event == 'erro':
        status = 'error'                                    #Stop the sensor to simulate that it is not working
    elif msg.event == 'reset':
        status = 'idle'                                     #Reset the sensor


# Function for victim recognition
def vs_on():
    global robot, victims, sensor_range,  sensor_update_period, status

    pub = rospy.Publisher("/{}/victim_sensor/out".format(robot), events_message, queue_size=10)

    while (not rospy.is_shutdown()) and (status == 'running'): 
        sensor = find_victim(robot, victims, sensor_range)
        for v in sensor:
            if sensor[v]['status'] == True:
                # rospy.loginfo("Find {} at pose [{},{},{}".format(v, sensor[v]['x_pos'],sensor[v]['y_pos'],sensor[v]['z_pos']))
                
                # Send the signal that a victim have been found and her location 
                models_service = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)       # Get model service from Gazebo
                pos = models_service(v, '')                                                         # Call the service to receive the global victim position
                
                msg = events_message()
                msg.event = 'victim_recognized'
                msg.param = [pos.pose.position.x, pos.pose.position.y, pos.pose.position.z]
                pub.publish(msg)        # Publish the found victim location 

                victims.remove(v)       # Remove the found victim from the list

        time.sleep(sensor_update_period)

if __name__ == '__main__':
    try:
        global robot, victims, sensor_range,  sensor_update_period, status
        status = 'idle'

        # Get parameters
        robot = rospy.get_param('robot_name', default='robot')
        victims = rospy.get_param('victims_models', default=[])
        sensor_range = rospy.get_param('sensor_range', default=1.0)
        sensor_update_period =  rospy.get_param('sensor_update_period', default=1.0)

        rospy.init_node('victim_recognition_system', anonymous=False)                                 # Initialize the node of the sensor

        rospy.wait_for_service('/gazebo/get_model_state')
        rospy.Subscriber("/{}/victim_sensor/in".format(robot), events_message, event_receiver)        # Topic to receive occured events

        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass

