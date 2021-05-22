#!/usr/bin/env python2.7

from geometry_msgs.msg import Twist
from system_msgs.msg import events_message

import rospy
from random import random as rd

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
            
            elif 'pioneer3at' in robot:
                dest = MoveBaseGoal()
                dest.target_pose.header.frame_id = "earth"
                dest.target_pose.pose.position.x = robot_state.pose.position.x + 2*DIST*rd() - DIST        # Desired x position
                dest.target_pose.pose.position.y = robot_state.pose.position.y + 2*DIST*rd() - DIST        # Desired y position

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
        
        end_publishers[robot].publish(msg2pub)


if __name__=="__main__":

    robots = rospy.get_param("robots_names", default = [])
    rospy.init_node("fake_joy", anonymous=False)           # Initialize keyboard node

    models_service.wait_for_service()

    for r in robots:
        #Get trajectory clients
        if 'UAV' in r:
            trajectory_clients[r] = SimpleActionClient("/{}/approach_server".format(r), ExecuteDroneApproachAction)
        elif 'pioneer3at' in r:
            trajectory_clients[r] = SimpleActionClient("/{}/move_base".format(r), MoveBaseAction)                   # Server name = robot_name/move_base
        trajectory_clients[r].wait_for_server()

        #Get tele END publishers
        end_publishers[r] = rospy.Publisher("/{}/maneuvers/in".format(r), events_message, queue_size=10)
        st_sub[r] = rospy.Subscriber("/{}/maneuvers/in".format(r), events_message, maneuver_event, r) 

    rospy.spin()