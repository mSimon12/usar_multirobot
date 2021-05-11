#!/usr/bin/env python3

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
import rospy

import roslib; roslib.load_manifest('teleop_twist_keyboard')
import sys, select, termios, tty

moveBindings = {
        'i':(1,0,0,0),
        'o':(1,0,0,-1),
        'j':(0,0,0,1),
        'l':(0,0,0,-1),
        'u':(1,0,0,1),
        ',':(-1,0,0,0),
        '.':(-1,0,0,1),
        'm':(-1,0,0,-1),
        'O':(1,-1,0,0),
        'I':(1,0,0,0),
        'J':(0,1,0,0),
        'L':(0,-1,0,0),
        'U':(1,1,0,0),
        '<':(-1,0,0,0),
        '>':(-1,-1,0,0),
        'M':(-1,1,0,0),
        't':(0,0,1,0),
        'b':(0,0,-1,0),
    }


def getKey(key_timeout):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node("keyboard", anonymous=False)           # Initialize keyboard node

    speed = 1.0
    key_timeout = 0.1

    joy_pub = rospy.Publisher('/joy', Joy, queue_size=10)
    joy_msg = Joy()

    try:
        while(1):
            joy_msg.axes = [0.0, 0.0, 0.0, 0.0]
            joy_msg.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            key = getKey(key_timeout)
            if key in moveBindings.keys():
                joy_msg.axes[1] = moveBindings[key][2]     # Get vertical speed
                joy_msg.axes[3] = moveBindings[key][0]     # Get horizontal speed
                joy_msg.axes[2] = moveBindings[key][3]     # Get angular speed
            else:
                #Increase linear speed
                if key == 'q':
                    joy_msg.buttons[4] = 1
                #Decrease linear speed
                elif key == 'a':
                    joy_msg.buttons[6] = 1
                #Increase angular speed
                elif key == 'w':
                    joy_msg.buttons[5] = 1
                #Decrease angular speed
                elif key == 's':
                    joy_msg.buttons[7] = 1
                #End teleoperation
                elif key == 'e':
                    joy_msg.buttons[9] = 1
                #Teleoperation error
                elif key == 'd':
                    joy_msg.buttons[4] = 1
                    joy_msg.buttons[5] = 1
                    joy_msg.buttons[6] = 1
                    joy_msg.buttons[7] = 1
                elif (key == '\x03'):
                    break

            joy_pub.publish(joy_msg)

    except Exception as e:
        print(e)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


