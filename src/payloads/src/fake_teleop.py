#!/usr/bin/env python2.7

from geometry_msgs.msg import Twist
from rospy.topics import Publisher
from system_msgs.msg import events_message

import rospy
from random import random as rd
from time import sleep

from actionlib import SimpleActionClient, GoalStatus
from trajectory_action_pkg.msg import ExecuteDroneApproachAction, ExecuteDroneApproachGoal
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

from gazebo_msgs.srv import GetModelState

DIST = 1.5

trajectory_clients = {}
end_publishers = {}
st_sub = {}
msg2pub = events_message()

models_service = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)                         # Get model service from Gazebo

def maneuver_event(msg, robot):
    
    trials = 0
    if msg.event == "start_teleoperation":
        robot_state = models_service(robot, '')
        while trials < 4:
            # Try to move
            if 'UAV' in robot:
                dest = ExecuteDroneApproachGoal()
                dest.goal.position.x = robot_state.pose.position.x + 2*DIST*rd() - DIST        # Desired x position
                dest.goal.position.y = robot_state.pose.position.y + 2*DIST*rd() - DIST        # Desired y position
                dest.goal.position.z = robot_state.pose.position.z + DIST*rd()                 # Desired z position     
                dest.goal.orientation.w = 1.0        

                trajectory_clients[robot].send_goal(dest)
                trajectory_clients[robot].wait_for_result()                     # Wait for the result
                state = trajectory_clients[robot].get_state()                   # Get the state of the action           

                if state == GoalStatus.SUCCEEDED:
                    trials = 10
                    msg2pub.event = "end_teleoperation"
                else:
                    trials += 1
                    if trials >= 4:
                        msg2pub.event = "teleoperation_error"            
            
            elif 'pioneer3at' in robot:
                pub_msg = Twist()
                pub_msg.linear.x = 0.5*rd() - 0.25
                pub_msg.angular.z = 2*rd() - 1
                trajectory_clients[robot].publish(pub_msg)
                sleep(10)
                pub_msg.linear.x = 0.0
                pub_msg.angular.z = 0.0
                trajectory_clients[robot].publish(pub_msg)

                robot_pose = models_service(robot, '')
                if ((robot_pose.pose.position.x - robot_state.pose.position.x)**2 + (robot_pose.pose.position.y - robot_state.pose.position.y)**2)**(1/2) > 0.5:
                    trials = 10
                    msg2pub.event = "end_teleoperation"
                else:
                    trials += 1
                    if trials >= 4:
                        msg2pub.event = "teleoperation_error"              
        
        end_publishers[robot].publish(msg2pub)


if __name__=="__main__":

    robots = rospy.get_param("robots_names", default = [])
    rospy.init_node("fake_joy", anonymous=False)           # Initialize keyboard node

    models_service.wait_for_service()

    for r in robots:
        #Get trajectory clients
        if 'UAV' in r:
            trajectory_clients[r] = SimpleActionClient("/{}/approach_server".format(r), ExecuteDroneApproachAction)
            trajectory_clients[r].wait_for_server()
        elif 'pioneer3at' in r:
            trajectory_clients[r] = Publisher("/{}/cmd_vel".format(r), Twist)                   # Server name = robot_name/move_base
        
        #Get tele END publishers
        end_publishers[r] = rospy.Publisher("/{}/maneuvers/in".format(r), events_message, queue_size=10)
        st_sub[r] = rospy.Subscriber("/{}/maneuvers/in".format(r), events_message, maneuver_event, r) 

    rospy.spin()