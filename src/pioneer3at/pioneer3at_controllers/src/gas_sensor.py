#!/usr/bin/env python

import time
import rospy

from gazebo_msgs.srv import GetModelState
from pioneer3at_controllers.msg import events_message

def find_gas(robot_name, gas_models, sensor_range = 1):
    '''
        Function to verify if a gas_leak from the list is into the range of the sensor
        robot_name: name of the robot model on Gazebo
        gas_models: list of gas models on Gazebo
        sensor_range: range in which the robot recognize a gas_leak
    '''
    models_service = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)        # Get model service from Gazebo
    # Get position of the gas source related to the robot position
    g_status = {}                                                                        # Dictionary with the status of each gas_leak and xyz position
    for g in gas_models:
        try:
            g_status[g] = {}
            answer = models_service(g, robot_name)                                       # Call the service to receive the gas_leak position
            g_status[g]['x_pos'] = answer.pose.position.x
            g_status[g]['y_pos'] = answer.pose.position.y
            g_status[g]['z_pos'] = answer.pose.position.z
        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {}".format(e))

        # Find the distance between robot and victim
        hip = (g_status[g]['x_pos']**2 + g_status[g]['y_pos']**2)**(1/2)
        dist = (hip**2 + g_status[g]['z_pos']**2)**(1/2)

        # Mark the victim as found if it is into the range
        if dist < sensor_range:
            g_status[g]['status'] = True
        else:
            g_status[g]['status'] = False

    return g_status         #Return the status of all victims


def event_receiver(msg):
    global running

    if msg.event == 'start' and (running == False):
        running = True
        vs_on()                               #Start the sensor
    elif msg.event == 'stop':
        running = False                       #Stop the sensor
    elif msg.event == 'erro':
        running = False                       #Stop the sensor to simulate that it is not working
    elif msg.event == 'reset':
        running = False                       #Reset the sensor


# Function for victim recognition
def vs_on():
    global robot, gas_models, sensor_range,  sensor_update_period, running

    pub = rospy.Publisher("/{}/gas_sensor/out".format(robot), events_message, queue_size=10)

    while (not rospy.is_shutdown()) and running: 
        sensor = find_gas(robot, gas_models, sensor_range)
        for g in sensor:
            if sensor[g]['status'] == True:
                # rospy.loginfo("Find {} at pose [{},{},{}".format(g, sensor[g]['x_pos'],sensor[g]['y_pos'],sensor[g]['z_pos']))
                
                # Send the signal that a victim have been found and her location 
                models_service = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)       # Get model service from Gazebo
                pos = models_service(g, '')                                                         # Call the service to receive the global victim position
                
                msg = events_message()
                msg.event = 'gas_leak'
                msg.param = [pos.pose.position.x, pos.pose.position.y, pos.pose.position.z]
                pub.publish(msg)          # Publish the found gas location 

                gas_models.remove(g)       # Remove the found gas from the list

        time.sleep(sensor_update_period)

if __name__ == '__main__':
    try:
        global robot, gas_models, sensor_range,  sensor_update_period, running
        running = False

        # Get parameters
        robot = rospy.get_param('robot_name', default='robot')
        gas_models = rospy.get_param('gas_models', default=[])
        sensor_range = rospy.get_param('sensor_range', default=1.0)
        sensor_update_period =  rospy.get_param('sensor_update_period', default=1.0)

        rospy.init_node('gas_sensor', anonymous=False)                                                # Initialize the node of the sensor

        rospy.wait_for_service('/gazebo/get_model_state')
        rospy.Subscriber("/{}/gas_sensor/in".format(robot), events_message, event_receiver)        # Topic to receive occured events

        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass

