#!/usr/bin/env python2.7

import rospy
from geometry_msgs.msg import Twist
from pioneer2dx_controllers.srv import motion
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sin, sqrt, pi, exp

# Robot actual position and orientation
x = 0.0
y = 0.0
theta = 0.0

#Callback for current pose estimation
def actual_Pose(msg):
    global x
    global y
    global theta    
    
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])      # Convertion from quartenion to euler representation


#Callback that control the robot
def controller(msg):
    global x
    global y
    global theta
    
    # Desired position and rotation angle
    x_goal = msg.destination.linear.x
    y_goal = msg.destination.linear.y
    theta_goal = msg.destination.angular.z

    # Speed object for controlling the robot
    speed = Twist()     

    pub = rospy.Publisher("/{}/cmd_vel".format(NAME),Twist, queue_size=1)       #Become publisher to robot cmd_vel

    rate = rospy.Rate(30)       #Update once 30 times per second

    flag = 0    #Status of the motion (0-Approach; 1-Orientation; 2-Correction)

    while not rospy.is_shutdown() :
        #Difference from actual position to desired one
        x_error = x_goal - x
        y_error = y_goal - y
        angle_to_goal = atan2(y_error,x_error)              # Angle to desired point in a straight line 

        dist = sqrt((x_goal - x)**2 + (y_goal - y)**2)      # Distance till the goal

        # Apply as angle_to_goal_error the direction with smaller error
        angle_to_goal_error = angle_to_goal - theta
        if angle_to_goal_error >= pi:
            angle_to_goal_error = angle_to_goal_error - 2*pi
        elif angle_to_goal_error <= -pi:
            angle_to_goal_error = angle_to_goal_error + 2*pi

        # Apply as angle_error the direction with smaller error
        angle_error = theta_goal - theta
        if angle_error >= pi:
            angle_error = angle_error - 2*pi
        elif angle_error <= -pi:
            angle_error = angle_error + 2*pi

        # MOTION DIRECTION ANALISYS (Move forward if needed angle < 90 and backward if angle > 90)
        if abs(angle_to_goal_error) <= pi/2:
            new_speed  = MAX_LINEAR_SPEED * (1 - exp(-dist))      
        else:
            new_speed  = -MAX_LINEAR_SPEED * (1 - exp(-dist))       # negative speed
            if angle_to_goal_error > 0:
                angle_to_goal_error = angle_to_goal_error - pi
            else:
                angle_to_goal_error = angle_to_goal_error + pi

        # STATUS CONTROLL (3 MOVEMENT PHASES)
        if dist > 0.3:
            # Approach phase
            flag = 0
        elif dist < 0.1 and abs(angle_error) < 0.05:
            # End the movement
            speed.linear.x = 0
            speed.angular.z = 0
            pub.publish(speed)
            return True                                     # Return True to the service caller
        elif dist < 0.05 and (flag == 0 or flag == 2):
            # Orientation correction phase
            flag = 1
        elif abs(angle_error) < 0.05 and flag == 1:
            # Position correction phase
            flag = 2
        else: 
            pass

        # MOTION CONTROLL
        if flag == 0:
            # Aproach phase
            if abs(angle_to_goal_error) > 0.2:
                speed.linear.x = 0.0
                if angle_to_goal_error > 0:
                    speed.angular.z = (MAX_ANG_SPEED - 0.2) * angle_to_goal_error/pi + 0.2      #rotate velocity proportional to difference
                else:
                    speed.angular.z = (MAX_ANG_SPEED - 0.2) * angle_to_goal_error/pi - 0.2      #rotate velocity proportional to difference
            else:
                # Linear speed limitation 
                if abs(new_speed - speed.linear.x) > 0.1:
                    if new_speed > speed.linear.x:
                        speed.linear.x = speed.linear.x + 0.1
                    else:
                        speed.linear.x = speed.linear.x - 0.1
                else:
                    speed.linear.x = new_speed 
                speed.angular.z = (MAX_ANG_SPEED/pi) * angle_to_goal_error * (1 - exp(-dist))
        elif flag == 1:
            # Orientation correction
            speed.linear.x = 0.0
            if angle_error > 0:
                speed.angular.z = (MAX_ANG_SPEED - 0.2) * angle_error/pi + 0.2      #rotate velocity proportional to difference
            else:
                speed.angular.z = (MAX_ANG_SPEED - 0.2) * angle_error/pi - 0.2      #rotate velocity proportional to difference
        elif flag == 2:
            # Correction phase
            if abs(new_speed - speed.linear.x) > 0.1:
                if new_speed > speed.linear.x:
                    speed.linear.x = speed.linear.x + 0.1
                else:
                    speed.linear.x = speed.linear.x - 0.1
            else:
                speed.linear.x = new_speed 
            speed.angular.z = (MAX_ANG_SPEED/pi) * (angle_to_goal_error + angle_error)/2

        # rospy.loginfo("distance = {}".format(dist))
        # rospy.loginfo("flag = {}".format(flag))
        # rospy.loginfo("angle_to_goal_error = {}".format(angle_to_goal_error))
        # rospy.loginfo("angle_error = {}".format(angle_error))
        
        # rospy.loginfo("linear speed = {}".format(speed.linear.x))
        # rospy.loginfo("angular speed = {}".format(speed.angular.z))
        pub.publish(speed)  #Publish desired 
        rate.sleep()

#Create the node responsible for the movement
def start_controller():
    rospy.init_node("motion_controller", anonymous=True)
    rospy.Service("/{}/move".format(NAME), motion, controller)
    # rospy.Subscriber("/{}/controller/pose".format(NAME), Twist, controller)         # Topic to receive desired position
    rospy.Subscriber("/{}/odom".format(NAME),Odometry, actual_Pose)                 # Topic to receive current position

    rospy.loginfo("Controller ready!")
    rospy.spin()

if __name__=='__main__':

    global MAX_LINEAR_SPEED
    global MAX_ANG_SPEED
    global NAME

    MAX_LINEAR_SPEED = rospy.get_param("max_speed", default=1)
    MAX_ANG_SPEED = rospy.get_param("max_ang_speed", default=0.5)
    NAME = rospy.get_param("robot_name", default="")
    start_controller()
