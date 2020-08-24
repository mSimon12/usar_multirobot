#!/usr/bin/env python2.7

from threading import Thread

import roslib
from math import sin, cos, pi
roslib.load_manifest('pioneer3at_controllers')
import rospy
from actionlib import SimpleActionClient, GoalStatus

from tf.transformations import quaternion_from_euler
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

from pioneer3at_controllers.msg import events_message

# Exploration
from geometry_msgs.msg import PolygonStamped, Point32, Pose2D
from exploration_msgs.msg import ExploreGoal, ExploreAction

# For teleoperation
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

########################################################################
class Manouver(object):
    
    def __init__(self,name):
        self.robot_name = name
        self.state = 'IDLE'                                                                                 # Manouver current state
        self._move_client = SimpleActionClient("/{}/move_base".format(self.robot_name), MoveBaseAction)     # Server name = robot_name/move_base
        self._move_client.wait_for_server()

        self.pub = rospy.Publisher("/{}/manouvers/out".format(name), events_message, queue_size=10)         # Publisher object
        self.msg = events_message()                                                                         # Message object
        
    def move_to(self,x,y,theta):
        '''
            Move to the desired position
        '''
        dest = MoveBaseGoal()
        dest.target_pose.header.frame_id = "earth"
        dest.target_pose.pose.position.x = x                    # Desired x position
        dest.target_pose.pose.position.y = y                    # Desired y position

        # Convert desired angle
        q = quaternion_from_euler(0,0,theta,'ryxz')
        dest.target_pose.pose.orientation.x = q[0]
        dest.target_pose.pose.orientation.y = q[1]
        dest.target_pose.pose.orientation.z = q[2]
        dest.target_pose.pose.orientation.w = q[3]
        
        self._move_client.send_goal(dest)                       # Send the goal
        self._move_client.wait_for_result()                     # Wait for the result
        state = self._move_client.get_state()                   # Get the state of the action

        if state == GoalStatus.SUCCEEDED:
            return "end"                                        # Motion successfully executed
        elif state == GoalStatus.PREEMPTED:
            return "susp"                                       # Client cancel the motion
        else:
            return "error"                                      # The server aborted the motion

################################################################################################################################################
class approach(Manouver):
    '''
        Manouver responsible for sending the robot to a specific position.
        It requires the goal position on start and if suspended it saves the 
        position for future execution if resumed.

        If the system is reseted or aborted, the goal position is missed.
    '''
    def __init__(self, name):
        super(approach, self).__init__(name)                                  # Initialize object
        self.__last_goal = None                                               # The last goal position

    def execute(self, pose):
        '''
            Require de robot to move to a specific point (x,y,theta)
        '''
        rospy.loginfo("Starting Approach!")

        if self.state == 'IDLE':
            # Save the assigned goal
            self.__last_goal = pose    

        self.state = 'EXE'                                                    # Set EXE state
        result = self.move_to(pose.x, pose.y, pose.theta)                     # Start the motion and wait for result

        # Verify the reason why the robot stopped moving
        if self.state == 'SUS':                                             # Approach have been suspended
            return
        elif result == 'end':                                               # Robot arrive to the desired position
            self.state = 'IDLE'                                             # Set IDLE state
            self.__last_goal = None                                         # Clear the last goal
            self.msg.event = 'end_approach'
            self.pub.publish(self.msg)                                      # Send the message signaling that the approach is complete
        else:                                                               # An error occured during the manouver
            self.state = 'ERROR'                                            # Set ERROR state
            self.msg.event = 'approach_error'
            self.pub.publish(self.msg)                                      # Send message signaling the error
   
    def suspend(self):
        rospy.loginfo("Suspending Approach!")
        self.state = 'SUS'                                                  # Set SUS state
        self._move_client.cancel_goal()                                     # Cancel the motion of the robot

    def resume(self):
        rospy.loginfo("Resuming Approach!")
        # Try to move to the last assigned position
        if self.__last_goal:
            self.execute(self.__last_goal)
        else:
            self.state = 'ERROR'                                            # Set ERROR state
            self.msg.event = 'approach_error'
            self.pub.publish(self.msg)                                      # Send message signaling the error

    def reset(self):
        rospy.loginfo("Reseting Approach!")
        self.__last_goal = None                                            # Clear the last goal
        self.state = 'IDLE'                                                # Set IDLE state

    def abort(self):
        rospy.loginfo("Aborting Approach!")
        self.__last_goal = None                                           # Clear the last goal
        self.state = 'IDLE'                                               # Set IDLE state

########################################################################
class exploration(object):
    '''
        Manouver responsible for sending a region to the exploration server and starting exploration.
        It requires the goal region with at least 3 point, and a start position. 
        After suspended the robot can reestart the exploration with the resume command.

        If the system is reseted or aborted, the goal region is missed.
    '''
    def __init__(self, name):
        self.robot_name = name
        self.state = 'IDLE'                             # Set IDLE state
        self.region = []                                # Region to be explored

        # Exploration service                                                                              
        self._frontier_client = SimpleActionClient("/{}/exploration_server_node".format(self.robot_name), ExploreAction)            # Create a client to the exploration node
        self._frontier_client.wait_for_server()                                                                                     # Wait server to be ready
        
        self._goal = ExploreGoal()                                                                                                  # Message to send the goal region
        self._goal.strategy_plugin = rospy.get_param("plugin_name", default="exploration_server::ExamplePlugin")                    # Select the exploration plugin
        self._goal.boundary.header.frame_id = "earth"                                                                               # Set frame wich the points are related to
        self._goal.start_point.header.frame_id = "earth"

        # Manouvers out
        self.pub = rospy.Publisher("/{}/manouvers/out".format(name), events_message, queue_size=10)                                 # Publisher object
        self.msg = events_message()                                                                                                 # Message object
        
    def execute(self, region_to_explore = None):
        rospy.loginfo("Starting Exploration!")
        
        if self.state == 'IDLE':
            # Save some variables
            self.region = region_to_explore                              # Save region being explored

        # Define boundaries
        for i in range(0, len(self.region)-1):
            p = Point32()
            p.x = self.region[i].x
            p.y = self.region[i].y
            self._goal.boundary.polygon.points.append(p)

        # Start position
        self._goal.start_point.point.x = self.region[i+1].x
        self._goal.start_point.point.y = self.region[i+1].y

        self.state = 'EXE'                                              # Set EXE state

        # Start the execution and wait response
        self._frontier_client.send_goal(self._goal)                     # Send the goal
        self._frontier_client.wait_for_result()                         # Wait for the result
        state = self._frontier_client.get_state()                       # Get the state of the action
        print(state)

        if state == GoalStatus.SUCCEEDED:
            result = "end"                                              # Exploration successfully executed
        elif state == GoalStatus.PREEMPTED:
            result = "susp"                                             # Client cancel the motion
        else:
            result = "error"                                            # The server aborted the motion

        # Verify the reason why the robot stopped moving
        if self.state == 'SUS':                                             # Exploration have been suspended
            return
        elif result == 'end':                                               # Robot explored the desired region
            self.state = 'IDLE'                                             # Set IDLE state
            self.region = []                                                # Clear the region variable
            self.msg.event = 'end_exploration'
            self.pub.publish(self.msg)                                      # Send the message signaling that the exploration is complete
        else:                                                               # An error occured during the manouver
            self.state = 'ERROR'                                            # Set ERROR state
            self.msg.event = 'exploration_error'
            self.pub.publish(self.msg)                                      # Send message signaling the error   

    def suspend(self):
        rospy.loginfo("Suspending Exploration!")
        self.state = 'SUS'                                                   # Set SUS state
        self._frontier_client.cancel_goal()                                  # Cancel the motion of the robot

    def resume(self):
        rospy.loginfo("Resuming Exploration!")
        # Try to get last region to be explored
        if self.region:
            self.execute()
        else:
            self.state = 'ERROR'                                            # Set ERROR state
            self.msg.event = 'exploration_error'
            self.pub.publish(self.msg)                                      # Send message signaling the error

    def reset(self):
        rospy.loginfo("Reseting Exploration!")
        self.region = []                                                    # Clear the last region
        self.state = 'IDLE'                                                 # Set IDLE state

    def abort(self):
        rospy.loginfo("Aborting Exploration!")
        self.region = []                                                    # Clear the last region
        self.state = 'IDLE'                                                 # Set IDLE state

########################################################################
class surroundings_verification(Manouver):
    '''
        Manouver responsibl for sending the robot to points around the victim to evalute
        possible gas sources and surroundings conditions.
    '''
    def __init__(self, name, safe_dist, n_points):
        super(surroundings_verification, self).__init__(name)
        self.safe_dist = safe_dist                                                                   # Distance from the victim
        self.n_points = n_points                                                                     # Quantity of points to visit
        self.points = []                                                                             # Points to visit arround the victim
        self.victim = {}                                                                             # Victim info
        
    def execute(self, victim_id = 'victim', victim_pose = None):
        rospy.loginfo("Starting Surroundings Verification!")
        
        if self.state == 'IDLE':
            self.victim['id'] = victim_id
            self.victim['x'] = victim_pose.x                                                          # Get victim pose
            self.victim['y'] = victim_pose.y

            # Define points around the victim
            theta_step = 2*pi/self.n_points                                                           # Theta dist between points
            self.points.append([victim_pose.x, victim_pose.y - self.safe_dist, 1.57])                 # First point to visit
            
            for i in range(1,self.n_points):                                                         
                self.points.append([victim_pose.x + self.safe_dist*sin(i*theta_step), 
                    victim_pose.y - self.safe_dist*cos(i*theta_step), 1.57 + i*theta_step])

        self.state = 'EXE'                                                                            # Set EXE state

        # Start the execution and wait response
        while self.points:   
            # Try to move to the next pose
            result = self.move_to(self.points[0][0], self.points[0][1], self.points[0][2])

            # Verify the reason why the robot stopped moving
            if self.state == 'SUS':
                return
            elif result == 'end':
                self.points.pop(0)                                 # Remove visited point
            else:
                self.state = 'ERROR'
                self.msg.event = 'verification_error'
                self.pub.publish(self.msg)                         # Send message signaling the error
                return

        # Finalize the execution
        self.state = 'IDLE'
        self.msg.event = 'end_verification'
        self.pub.publish(self.msg)                                  ## Send message signaling the manouver accomplished

    def suspend(self):
        rospy.loginfo("Suspending Surroundings Verification!")
        self.state = 'SUS'
        self._move_client.cancel_goal()                             # Stop current motion

    def resume(self):
        rospy.loginfo("Resuming Surroundings Verification!")
        # Try to move to the last assigned position
        if self.points:
            self.execute()
        else:
            self.state = 'ERROR'                                    # Set ERROR state
            self.msg.event = 'verification_error'                   # No points listed to go
            self.pub.publish(self.msg)                              # Send message signaling the error

    def reset(self):
        rospy.loginfo("Reseting Surroundings Verification!")
        self.points = []                                            # Clear points
        self.state = 'IDLE'                                         # Set IDLE state

    def abort(self):
        rospy.loginfo("Aborting Surroundings Verification!")
        self.points = []                                            # Clear points
        self.state = 'IDLE'                                         # Set IDLE state

########################################################################
class return_to_base(Manouver):
    '''
        Move the robot till the base position.
        *The base position is defined on the system start.
    '''

    def __init__(self, name, base_x, base_y):
        self.base_pos = {'x': base_x, 'y': base_y}                               # Position of the base
        super(return_to_base, self).__init__(name)

    def execute(self):
        rospy.loginfo("Starting Return to Base!")
        self.state = 'EXE'

        result = self.move_to(self.base_pos['x'], self.base_pos['y'], 0)            # Start the motion and wait for result

        # Verify the reason why the robot stopped moving
        if self.state == 'SUS':
            return
        elif result == 'end':
            self.state = 'IDLE'
            self.msg.event = 'end_return'
            self.pub.publish(self.msg)
        else:
            self.state = 'ERROR'
            self.msg.event = 'return_error'
            self.pub.publish(self.msg)

    def suspend(self):
        rospy.loginfo("Suspending Return to Base!")
        self.state = 'SUS'
        self._move_client.cancel_goal()

    def resume(self):
        rospy.loginfo("Resuming Return to Base!")
        # Try to move to the base
        if self.base_pos:
            self.execute()
        else:
            self.state = 'ERROR'                                    # Miss the base position
            self.msg.event = 'return_error'
            self.pub.publish(self.msg)

    def reset(self):
        rospy.loginfo("Reseting Return to Base!")
        self.state = 'IDLE'

    def abort(self):
        rospy.loginfo("Aborting Return to Base!")
        self.state = 'IDLE'

########################################################################
class teleoperation(object):
    '''
        Allows a human to teleoperate the robot through a joystick.
    '''
    def __init__(self, name):
        self.robot_name = name
        self.state = 'IDLE' 

        #Variables to control the speed 
        self.max_vel = rospy.get_param("move_base/DWAPlannerROS/max_vel_x")
        self.max_ang_vel = rospy.get_param("move_base/DWAPlannerROS/max_rot_vel")
        self.current_x_speed = self.max_vel/2
        self.current_ang_speed = self.max_ang_vel/2

        self.__pub = rospy.Publisher("cmd_vel",Twist, queue_size=10)

        self.pub = rospy.Publisher("/{}/manouvers/out".format(name), events_message, queue_size=10)         # Publisher object
        self.msg = events_message()                                                                         # Message object

    def execute(self):
        rospy.loginfo("Starting Teleoperation!")
        self.state = 'EXE'

        # Start teleoperation
        self.__sub = rospy.Subscriber('joy', Joy, self.Joy_callback)                       # Start receiving messages from joystick

    def reset(self):
        rospy.loginfo("Reseting Teleoperation!")
        self.state = 'IDLE'
    
    def end(self):
        self.__sub.unregister()                                         # Stop receiving messages from joystick
        self.msg.event = 'end_teleoperation'
        self.pub.publish(self.msg)                                      # Send message signaling the error
        self.state = 'IDLE'

    def error(self):
        self.__sub.unregister()                                         # Stop receiving messages from joystick
        self.msg.event = 'teleoperation_error'
        self.pub.publish(self.msg)                                      # Send message signaling the error
        self.state = 'ERROR'

    def Joy_callback(self,msg):
        speed = msg.axes[1]             # Get speed
        rot = msg.axes[2]               # Ger angular speed
        if speed < 0:
            rot = -rot

        #twist message for moving
        twist_msg = Twist()
        twist_msg.linear.x = speed*self.current_x_speed 
        twist_msg.angular.z = rot*self.current_ang_speed

        self.__pub.publish(twist_msg)          # Publish to cmd_vel

        # Change linear speed
        if msg.buttons[4]:
            self.current_x_speed += self.max_vel*0.1
            if self.current_x_speed > self.max_vel:
                self.current_x_speed = self.max_vel
        elif msg.buttons[6]:
            self.current_x_speed -= self.max_vel*0.1
            if self.current_x_speed < 0.2:
                self.current_x_speed = 0.2

        # Change angular speed
        if msg.buttons[5]:
            self.current_ang_speed += self.max_ang_vel*0.1
            if self.current_ang_speed > self.max_ang_vel:
                self.current_ang_speed = self.max_ang_vel 
        elif msg.buttons[7]:
            self.current_ang_speed -= self.max_ang_vel *0.1
            if self.current_ang_speed < 0.4:
                self.current_ang_speed = 0.4

        if msg.buttons[9]:
            # Teleoperation ended
            self.end()
        elif all(msg.buttons[4:8]):
            # Teleoperation error
            self.error()


########################################################################
##### Manouvers events callback ########################################
def manouver_event(msg):
    global app, exp, rb, vsv, tele

    # Verify the received message
    if "approach" in msg.event:
        # Commands for approach manouver
        if (msg.event == "start_approach") and (app.state == 'IDLE'):
            # Verify paramenters
            if msg.position:
                thread = Thread(target=app.execute,args=[msg.position[0]])
                thread.start()                                                              # Start approach
            else:
                rospy.logwarn("Wrong approach parameters! Must be [x,y,theta]")             # Missing parameters
        
        elif (msg.event == "suspend_approach") and (app.state == 'EXE'):
            app.suspend()
        elif (msg.event == "resume_approach") and (app.state == 'SUS'):
            thread = Thread(target=app.resume)
            thread.start()
        elif (msg.event == "reset_approach") and (app.state =='ERROR'):
            app.reset()
        elif (msg.event == "abort_approach") and (app.state == 'SUS'):
            app.abort()
        else:
            rospy.logwarn("Command not allowed!")

    elif "exploration" in msg.event:
        # Commands for exploration manouver
        if (msg.event == "start_exploration") and (exp.state == 'IDLE'):
            # Verify paramenters
            if len(msg.position) > 3:                                                           # Need at least three points to create a polygon
                thread = Thread(target=exp.execute, args=[msg.position])
                thread.start()                                                                  # Start exploration
            else:
                rospy.logwarn("Wrong exploration parameters! Must have at least 3 vertices and 1 start position.")             # Missing parameters
        
        elif (msg.event == "suspend_exploration") and (exp.state == 'EXE'):
            exp.suspend()
        elif (msg.event == "resume_exploration") and (exp.state == 'SUS'):
            thread = Thread(target=exp.execute)
            thread.start()
        elif (msg.event == "reset_exploration") and (exp.state =='ERROR'):
            exp.reset()
        elif (msg.event == "abort_exploration") and (exp.state == 'SUS'):
            exp.abort()
        else:
            rospy.logwarn("Command not allowed!")

    elif "verification" in msg.event:
        # Commands for victim surroundings verification manouver
        if (msg.event == "start_verification") and (vsv.state == 'IDLE'):
            if msg.position:
                thread = Thread(target=vsv.execute, args=[msg.info, msg.position[0]])
                thread.start()                                                                  # Start victim surroundings verification
            else:
                rospy.logerr("Null victim pose!!!")
        elif (msg.event == "suspend_verification") and (vsv.state == 'EXE'):
            vsv.suspend()
        elif (msg.event == "resume_verification") and (vsv.state == 'SUS'):
            thread = Thread(target=vsv.execute)
            thread.start()
        elif (msg.event == "reset_verification") and (vsv.state =='ERROR'):
            vsv.reset()
        elif (msg.event == "abort_verification") and (vsv.state == 'SUS'):
            vsv.abort()
        else:
            rospy.logwarn("Command not allowed!")

    elif "return" in msg.event:
        # Commands for returtn to base manouver
        if (msg.event == "start_return") and (rb.state == 'IDLE'):
            thread = Thread(target=rb.execute)
            thread.start()                                                                        # Start return to base
        elif (msg.event == "suspend_return") and (rb.state == 'EXE'):
            rb.suspend()
        elif (msg.event == "resume_return") and (rb.state == 'SUS'):
            thread = Thread(target=rb.execute)
            thread.start()
        elif (msg.event == "reset_return") and (rb.state =='ERROR'):
            rb.reset()
        elif (msg.event == "abort_return") and (rb.state == 'SUS'):
            rb.abort()
        else:
            rospy.logwarn("Command not allowed!")

    elif "teleoperation" in msg.event:
        # Commands for teleoperation manouver
        if (msg.event == "start_teleoperation") and (tele.state =='IDLE'):
            thread = Thread(target=tele.execute)
            thread.start()                                                                      # Start teleoperation
        elif (msg.event == "reset_teleoperation") and (tele.state == 'ERROR'):
            tele.reset()
        elif (msg.event == "end_teleoperation") and (tele.state == 'EXE'):
            # Teleoperation ended
            tele.end()
        elif (msg.event == "teleoperation_error") and (tele.state == 'EXE'):
            # Teleoperation ended
            tele.error()
        else:
            rospy.logwarn("Command not allowed!")

def victim_event(msg):
    '''
        Suspend all manouvers in execution if a victim is found.
    '''
    global app, exp, rb, vsv
    if msg.event == 'victim_recognized':
        if (app.state == 'EXE'):
            app.suspend()                       # Suspend approach
        if (exp.state == 'EXE'):
            exp.suspend()                       # Suspend exploration
        if (rb.state == 'EXE'):
            rb.suspend()                        # Suspend return to base
        if (vsv.state == 'EXE'):
            vsv.suspend()                       # Suspend victim surroundings verification


if __name__=="__main__":
    global app, exp, rb, vsv, tele
    NAME = rospy.get_param("robot_name", default = "")

    # Return to base parameters
    x_coord = rospy.get_param("xcoordinate", default = 0.0)
    y_coord = rospy.get_param("ycoordinate", default = 0.0)
    
    # VSV parameters
    safe_dist = rospy.get_param("vsv_safe_dist", default = 1.0)
    n_points = rospy.get_param("vsv_n_points", default = 8)

    rospy.init_node("{}_manouvers".format(NAME), anonymous=False)           # Initialize manouvers node

    # Create object for each type of manouver
    app = approach(NAME)
    exp = exploration(NAME)
    vsv = surroundings_verification(NAME, safe_dist, n_points)
    rb = return_to_base(NAME, x_coord, y_coord)
    tele = teleoperation(NAME)
    
    rospy.Subscriber("manouvers/in", events_message, manouver_event, queue_size=10)            # Topic to receive command events
    rospy.Subscriber("victim_sensor/out", events_message, victim_event, queue_size=10)         # Topic to receive events from victim sensor

    rospy.spin()
