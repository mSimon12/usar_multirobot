#!/usr/bin/env python2.7

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sin, sqrt, pi

MAX_LINEAR_SPEED = 0.7
MAX_ANG_SPEED = 0.5

#Robot actual position and orientation
x = 0.0
y = 0.0
theta = 0.0

#Callback that control the robot
def controller(msg):
    global x
    global y
    global theta
    
    x_goal = msg.linear.x
    y_goal = msg.linear.y
    theta_goal = msg.angular.z

    dist = sqrt((x_goal - x)**2 + (y_goal - y)**2)

    #speed object for controlling the robot
    speed = Twist()     

    name = "pioneer3at"
    pub = rospy.Publisher("{}/cmd_vel".format(name),Twist, queue_size=1)       #Become publisher to robot cmd_vel

    rate = rospy.Rate(10)

    while not rospy.is_shutdown() :
        #Difference from actual position to desired one
        x_error = x_goal - x
        y_error = y_goal - y
        
        angle_to_goal = atan2(y_error,x_error)  #goal to desired point in a straight line
        angle_error = angle_to_goal - theta
        
        if abs(x_goal - x) > 0.1 or abs(y_goal - y) > 0.1:
            if abs(angle_error) > 0.1:
                speed.linear.x = 0.0
                speed.angular.z = (MAX_ANG_SPEED - 0.2) * angle_error/pi + 0.2 * angle_error/abs((angle_error))     #rotate velocity proportional to difference
            else:
                speed.linear.x = (MAX_LINEAR_SPEED - 0.2) * abs(y_error/sin(theta))/dist + 0.2    #linear velocity proportional to difference
                speed.angular.z = 0.0
        elif abs(angle_error) > 0.1:
            angle_error = theta_goal - theta
            speed.linear.x = 0.0
            speed.angular.z = (MAX_ANG_SPEED - 0.2) * (theta_goal - theta)/pi + 0.2 * angle_error/abs((angle_error))    #rotate velocity proportional to difference
        else:
            speed.linear.x = 0.0
            speed.angular.z = 0.0
            pub.publish(speed)
            break
        
        rospy.loginfo("linear speed = {}".format(speed.linear.x))
        rospy.loginfo("angular speed = {}".format(speed.angular.z))
        pub.publish(speed)  #Publish desired speed
        rate.sleep()


#Callback for pose estimation
def actual_Pose(msg):
    global x
    global y
    global theta    
    
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])


def start_controller():
    rospy.init_node("pioneer3at_move", anonymous=True)
    name = rospy.get_name()
    rospy.Subscriber("{}/pose".format(name), Twist, controller)
    rospy.Subscriber("pioneer3at/odom",Odometry, actual_Pose)

    rospy.loginfo("Controller ready!")
    rospy.spin()


if __name__=='__main__':
    start_controller()
