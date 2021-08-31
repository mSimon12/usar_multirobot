#!/usr/bin/env python2.7

from threading import Thread, Condition
import copy

import roslib
from math import sin, cos, pi, sqrt, atan2
roslib.load_manifest('quadrotor_control_system')
import rospy
from actionlib import SimpleActionClient, GoalStatus

from tf.transformations import quaternion_from_euler, euler_from_quaternion

from hector_uav_msgs.srv import EnableMotors

from trajectory_action_pkg.msg import ExecuteDroneApproachAction, ExecuteDroneApproachGoal
from geometry_msgs.msg import Pose, Point, PoseStamped, Twist

# from sensor_msgs.msg import Range
from system_msgs.msg import events_message

# Victim search
from quadrotor_control_system.msg import ExecuteSearchAction, ExecuteSearchGoal

# Safe Land
from quadrotor_control_system.msg import ExecuteLandAction,  ExecuteLandGoal

# Exploration
from hector_moveit_exploration.msg import ExecuteDroneExplorationAction, ExecuteDroneExplorationGoal
# from quadrotor_control_system.msg import ExecuteAssesstAction,  ExecuteAssesstGoal

# Return to base
from hector_uav_msgs.srv import EnableMotors, EnableMotorsRequest

# For teleoperation
from sensor_msgs.msg import Joy, Range
from nav_msgs.msg import Odometry


########################################################################
class Maneuver(object):
    
    def __init__(self,name):
        self.state = 'IDLE'           
        self.suspending = False   
        self.trajectory_client = SimpleActionClient("approach_server", ExecuteDroneApproachAction)
        self.trajectory_client.wait_for_server()

        # Subscribe to sonar_height
        rospy.Subscriber("sonar_height", Range, self.sonar_callback, queue_size=10)
        rospy.Subscriber("ground_truth/state", Odometry, self.poseCallback)
        self.sonar_me = Condition()
        self.current_height = None

        self.odometry_me = Condition()
        self.odometry = None

        self.pub = rospy.Publisher("/{}/maneuvers/out".format(name), events_message, queue_size=10)         # Publisher object
        self.msg = events_message()                                                                         # Message object
        
    def move_to(self,x,y,z,theta):
        '''
            Move to the desired position
        '''
        dest = ExecuteDroneApproachGoal()
        dest.goal.position.x = x                    # Desired x position
        dest.goal.position.y = y                    # Desired y position

        trials = 0      # approach trials

        while trials < 10:

            self.sonar_me.acquire()
            h_error = z - self.current_height
            self.sonar_me.release()

            self.odometry_me.acquire()
            self.odometry_me.wait()
            dest.goal.position.z = self.odometry.position.z + h_error        # Desired z position
            self.odometry_me.release()

            # Convert desired angle
            q = quaternion_from_euler(0,0,theta,'ryxz')
            dest.goal.orientation.x = q[0]
            dest.goal.orientation.y = q[1]
            dest.goal.orientation.z = q[2]
            dest.goal.orientation.w = q[3]

            self.trajectory_client.send_goal(dest)                      # Send the goal
            self.trajectory_client.wait_for_result()                    # Wait for the result
            state = self.trajectory_client.get_state()                  # Get the state of the action
            
            if state == GoalStatus.SUCCEEDED:
                return "end"                                        # Motion successfully executed
            elif state == GoalStatus.PREEMPTED:
                return "susp"                                       # Client cancel the motion
            
            trials += 1
        return "error"                                      # The server aborted the motion

    def sonar_callback(self,msg):
        '''
            Function to update drone height
        '''
        self.sonar_me.acquire()
        self.current_height = msg.range
        self.sonar_me.release()

    def poseCallback(self,odometry):
        '''
            Monitor the current position of the robot
        '''
        self.odometry_me.acquire()
        self.odometry = odometry.pose.pose
        self.odometry_me.notify()
        self.odometry_me.release()

################################################################################################################################################
class approach(Maneuver):
    '''
        Maneuver responsible for sending the robot to a specific position.
        It requires the goal position on start and if suspended it saves the 
        position for future execution if resumed.

        If the system is reseted or aborted, the goal position is missed.
    '''
    def __init__(self, name):
        super(approach, self).__init__(name)                                  # Initialize object
        self.__last_goal = None                                               # The last goal position

    def execute(self, pose, received_msg = None):
        '''
            Require de robot to move to a specific point (x,y,theta)
        '''

        if self.state == 'IDLE':
            self.msg = copy.deepcopy(received_msg)

            rospy.loginfo("Starting Approach!")
            # Save the assigned goal
            self.__last_goal = pose    

        self.state = 'EXE'                                                    # Set EXE state
        result = self.move_to(pose.linear.x, pose.linear.y, pose.linear.z, pose.angular.z)         # Start the motion and wait for result

        # Verify the reason why the robot stopped moving
        if self.suspending:                                                 # Approach have been suspended
            self.suspending = False   
            return
        elif result == 'end':                                               # Robot arrive to the desired position
            self.state = 'IDLE'                                             # Set IDLE state
            self.__last_goal = None                                         # Clear the last goal
            self.msg.event = 'end_approach'
            self.pub.publish(self.msg)                                      # Send the message signaling that the approach is complete
        else:                                                               # An error occured during the maneuver
            self.state = 'ERROR'                                            # Set ERROR state
            self.msg.event = 'approach_error'
            self.pub.publish(self.msg)                                      # Send message signaling the error
   
    def suspend(self):
        rospy.loginfo("Suspending Approach!")
        self.suspending = True
        self.state = 'SUS'                                                  # Set SUS state
        self.trajectory_client.cancel_goal()                                # Cancel the motion of the robot

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

    def erro(self):
        rospy.loginfo("Approach Erro!")
        self.state = 'ERROR'                                                # Set ERROR state
        self.trajectory_client.cancel_goal()                                # Cancel the motion of the robot

########################################################################
class assessment(object):
    '''
        Maneuver responsible for sending a region to the exploration server and starting assessment.
        It requires the goal region with at least 3 point, and a start position. 
        After suspended the robot can reestart the assessment with the resume command.

        If the system is reseted or aborted, the goal region is missed.
    '''
    def __init__(self, name):
        self.robot_name = name
        self.suspending = False 
        self.state = 'IDLE'                             # Set IDLE state
        self.region = []                                # Region to be explored

        # Exploration service                                                                            
        self._assess_client = SimpleActionClient("assessment_server", ExecuteDroneExplorationAction)                # Create a client to the v_search server
        self._assess_client.wait_for_server()                                                                       # Wait server to be ready                                                        

        # Maneuvers out
        self.pub = rospy.Publisher("/{}/maneuvers/out".format(name), events_message, queue_size=10)                                 # Publisher object
        self.msg = events_message()                                                                                                 # Message object
        
    def execute(self, region_to_explore = None, received_msg = None):
        rospy.loginfo("Starting assessment!")
        self.suspending = False
        
        if self.state == 'IDLE':
            self.msg = copy.deepcopy(received_msg)

            # Save some variables
            self.region = region_to_explore                             # Save region being explored

        self._assess_goal = ExecuteDroneExplorationGoal()               # Message to send the goal region 
        
        # Define boundaries
        self._assess_goal.x_min = self.region[0].linear.x
        self._assess_goal.x_max = self.region[0].linear.x + self.region[1].linear.x
        self._assess_goal.y_min = self.region[0].linear.y
        self._assess_goal.y_max = self.region[0].linear.y + self.region[1].linear.y

        self.state = 'EXE'                                              # Set EXE state

        # Start the execution and wait response
        self._assess_client.send_goal(self._assess_goal)
        self._assess_client.wait_for_result()
        state = self._assess_client.get_state()                         # Get the state of the action
        # print(state)

        if state == GoalStatus.SUCCEEDED:
            result = "end"                                              # Assessment successfully executed
        elif state == GoalStatus.PREEMPTED:
            result = "susp"                                             # Client cancel the motion
        else:
            result = "error"                                            # The server aborted the motion

        # Verify the reason why the robot stopped moving
        if self.suspending:                                             # Assessment have been suspended
            # self.suspending = False
            return
        elif result == 'end':                                               # Robot explored the desired region
            self.state = 'IDLE'                                             # Set IDLE state
            self.region = []                                                # Clear the region variable
            self.msg.event = 'end_assessment'
            self.pub.publish(self.msg)                                      # Send the message signaling that the assessment is complete
        else:                                                               # An error occured during the maneuver
            self.state = 'ERROR'                                            # Set ERROR state
            self.msg.event = 'assessment_error'
            self.pub.publish(self.msg)                                      # Send message signaling the error   

    def suspend(self):
        rospy.loginfo("Suspending Assessment!")
        self.suspending = True
        self.state = 'SUS'                                                   # Set SUS state
        self._assess_client.cancel_goal()                                  # Cancel the motion of the robot

    def resume(self):
        rospy.loginfo("Resuming Assessment!")
        # Try to get last region to be explored
        if self.region:
            self.execute()
        else:
            self.state = 'ERROR'                                            # Set ERROR state
            self.msg.event = 'assessment_error'
            self.pub.publish(self.msg)                                      # Send message signaling the error

    def reset(self):
        rospy.loginfo("Reseting Assessment!")
        self.region = []                                                    # Clear the last region
        self.state = 'IDLE'                                                 # Set IDLE state

    def abort(self):
        rospy.loginfo("Aborting Assessment!")
        self.region = []                                                    # Clear the last region
        self.state = 'IDLE'                                                 # Set IDLE state

    def erro(self):
        rospy.loginfo("Assessment Erro!")
        self.state = 'ERROR'                                                # Set ERROR state
        self._assess_client.cancel_goal()                                  # Cancel the motion of the robot

########################################################################
class v_search(object):
    '''
        Maneuver responsible for sending a region to the exploration server and starting v_search.
        It requires the goal region with at least 3 point, and a start position. 
        After suspended the robot can restart the v_search with the resume command.

        If the system is reseted or aborted, the goal region is missed.
    '''
    def __init__(self, name):
        self.robot_name = name
        self.suspending = False 
        self.state = 'IDLE'                             # Set IDLE state
        self.region = []                                # Region to be explored

        # Exploration service                                                                              
        self._search_client = SimpleActionClient("search_server", ExecuteSearchAction)                # Create a client to the v_search server
        self._search_client.wait_for_server()                                                         # Wait server to be ready
        
        self._area = ExecuteSearchGoal()                                                              # Message to send the goal region

        # Maneuvers out
        self.pub = rospy.Publisher("/{}/maneuvers/out".format(name), events_message, queue_size=10)                  # Publisher object
        self.msg = events_message()                                                                                  # Message object
        
    def execute(self, region_to_search = None, received_msg = None):
        
        if self.state == 'IDLE':
            self.msg = copy.deepcopy(received_msg)

            rospy.loginfo("Starting v_search!")
            # Save some variables
            self.region = region_to_search                              # Save region being explored

        # Define start position to explore
        p = Point()
        p.x = self.region[0].linear.x
        p.y = self.region[0].linear.y
        self._area.origin = p

        self._area.x = self.region[1].linear.x
        self._area.y = self.region[1].linear.y

        self.state = 'EXE'                                              # Set EXE state

        # Start the execution and wait response
        self._search_client.send_goal(self._area)                     # Send the goal
        self._search_client.wait_for_result()                         # Wait for the result

        # Get result
        result = self._search_client.get_result()
        self.region[1].linear.y = (self.region[0].linear.y + self.region[1].linear.y) - result.last_pose.position.y
        self.region[0].linear.y = result.last_pose.position.y

        state = self._search_client.get_state()                       # Get the state of the action

        if state == GoalStatus.SUCCEEDED:
            result = "end"                                              # v_search successfully executed
        elif state == GoalStatus.PREEMPTED:
            result = "susp"                                             # Client cancel the motion
        else:
            result = "error"                                            # The server aborted the motion

        # Verify the reason why the robot stopped moving
        if self.suspending:                                                 # v_search have been suspended
            self.suspending = False
            return
        elif result == 'end':                                               # Robot explored the desired region
            self.state = 'IDLE'                                             # Set IDLE state
            self.region = []                                                # Clear the region variable
            self.msg.event = 'end_v_search'
            self.pub.publish(self.msg)                                      # Send the message signaling that the v_search is complete
        else:                                                               # An error occured during the maneuver
            self.state = 'ERROR'                                            # Set ERROR state
            self.msg.event = 'v_search_error'
            self.pub.publish(self.msg)                                      # Send message signaling the error   

    def suspend(self):
        rospy.loginfo("Suspending V_Search!")
        self.suspending = True
        self.state = 'SUS'                                                   # Set SUS state
        self._search_client.cancel_goal()                                  # Cancel the motion of the robot

    def resume(self):
        rospy.loginfo("Resuming V_Search!")
        # Try to get last region to be explored
        if self.region:
            self.execute()
        else:
            self.state = 'ERROR'                                            # Set ERROR state
            self.msg.event = 'v_search_error'
            self.pub.publish(self.msg)                                      # Send message signaling the error

    def reset(self):
        rospy.loginfo("Reseting V_Search!")
        self.region = []                                                    # Clear the last region
        self.state = 'IDLE'                                                 # Set IDLE state

    def abort(self):
        rospy.loginfo("Aborting V_Search!")
        self.region = []                                                    # Clear the last region
        self.state = 'IDLE'                                                 # Set IDLE state

    def erro(self):
        rospy.loginfo("V_Search Erro!")
        self._search_client.cancel_goal()                                  # Cancel the motion of the robot

# ########################################################################
class surroundings_verification(Maneuver):
    '''
        Maneuver responsible for sending the robot to points around the victim to evalute
        possible gas sources and surroundings conditions.
    '''
    def __init__(self, name, min_dist, max_dist, rounds, points, height):
        super(surroundings_verification, self).__init__(name)
        self.min_dist = min_dist                                                                     # Min Distance from the victim
        self.max_dist = max_dist                                                                     # Max Distance from the victim
        self.rounds = rounds                                                                         # Rounds the robot must do
        self.n_points = points                                                                       # Quantity of points to visit per round
        self.height = height                                                                         # Height to move around the victim
        
        # Variables needed for maneuver execution
        self.points = []                                                                             # Points to visit arround the victim
        self.victim = {}                                                                             # Victim info                                                                        
        
    def execute(self, victim_id = 'victim', victim_pose = None, received_msg = None):
        
        delta = (self.max_dist - self.min_dist)/(self.rounds*self.n_points)
        
        if self.state == 'IDLE':
            self.msg = copy.deepcopy(received_msg)
            
            rospy.loginfo("Starting Surroundings Verification!")
            self.victim['id'] = victim_id
            self.victim['x'] = victim_pose.linear.x                                                         # Get victim pose
            self.victim['y'] = victim_pose.linear.y
            self.victim['z'] = victim_pose.linear.z

            self.odometry_me.acquire()
            r_v_dist = sqrt((self.odometry.position.x - self.victim['x'])**2 + (self.odometry.position.y - self.victim['y'])**2)
            initial_x = (self.odometry.position.x - self.victim['x'])*self.min_dist/r_v_dist
            initial_y = (self.odometry.position.y - self.victim['y'])*self.min_dist/r_v_dist
            initial_theta = atan2(initial_y, initial_x)
            self.odometry_me.release()

            # Define points around the victim
            theta_step = 2*pi/self.n_points                                                           # Theta dist between points
            
            count = 0
            for i in range(0,self.rounds):
                for j in range(0,self.n_points):                                                         
                    self.points.append([self.victim['x'] + (self.min_dist + count*delta)*cos(initial_theta + j*theta_step), 
                        self.victim['y'] + (self.min_dist + count*delta)*sin(initial_theta + j*theta_step), self.height, initial_theta + j*theta_step + pi])
                    count += 1

        self.state = 'EXE'                                                                            # Set EXE state

        # Start the execution and wait response
        while self.points:   
            # Try to move to the next pose
            result = self.move_to(self.points[0][0], self.points[0][1], self.points[0][2], self.points[0][3])
            # Verify the reason why the robot stopped moving
            if self.suspending:
                self.suspending = False
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
        self.pub.publish(self.msg)                                  ## Send message signaling the maneuver accomplished

    def suspend(self):
        rospy.loginfo("Suspending Surroundings Verification!")
        self.suspending = True
        self.state = 'SUS'
        self.trajectory_client.cancel_goal()                             # Stop current motion

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

    def erro(self):
        rospy.loginfo("Surroundings Verification Erro!")
        self.trajectory_client.cancel_goal()                                # Cancel the motion of the robot

# ########################################################################
class return_to_base(Maneuver):
    '''
        Move the robot till the base position.
        *The base position is defined on the system start.
    '''

    def __init__(self, name, base_x, base_y, base_z):
        self.base_pos = {'x': base_x, 'y': base_y, 'z': base_z}                               # Position of the base
        super(return_to_base, self).__init__(name)

        # quadrotor motion service
        self.motors = rospy.ServiceProxy('enable_motors', EnableMotors)
        self.motors.wait_for_service()

    def execute(self):
        if self.state == 'IDLE':
            rospy.loginfo("Starting Return to Base!")
            self.state = 'EXE'

        result = self.move_to(self.base_pos['x'], self.base_pos['y'], self.base_pos['z'] + 1.0, 0)            # Start the motion and wait for result

        if result == 'end':
            result = self.move_to(self.base_pos['x'], self.base_pos['y'], self.base_pos['z'] + 0.2, 0)            # Start the motion and wait for result
            
            motors_msg = EnableMotorsRequest()
            motors_msg.enable = False                   # Disable motors to make the drone land
            self.motors.call(motors_msg)

        # Verify the reason why the robot stopped moving
        if self.suspending:
            self.suspending = False
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
        self.suspending = True
        self.state = 'SUS'
        self.trajectory_client.cancel_goal()

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

    def erro(self):
        rospy.loginfo("Return to Base Erro!")
        self.state = 'ERROR'                                                # Set ERROR state
        self.trajectory_client.cancel_goal()                                # Cancel the motion of the robot

# ########################################################################
class teleoperation(Maneuver):
    '''
        Allows a human to teleoperate the robot through a joystick.
    '''
    def __init__(self, name):
        super(teleoperation, self).__init__(name)

        # self.robot_name = name
        # self.state = 'IDLE' 

        #Variables to control the speed 
        self.max_vel = 0.8                              #rospy.get_param()
        self.max_ang_vel = 1.0                          #rospy.get_param()
        self.current_speed = self.max_vel/2
        self.current_ang_speed = self.max_ang_vel/2

        #Publish msg to execute the motion
        self.__tele_pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        self.__tele_msg = Twist()

        # self.__last_time = rospy.get_time()

        # self.pub = rospy.Publisher("/{}/maneuvers/out".format(name), events_message, queue_size=10)         # Publisher object
        # self.msg = events_message()                                                                         # Message object

         # Subscribe to joy msgs
        self.__sub = rospy.Subscriber('/joy', Joy, self.Joy_callback)                       # Start receiving messages from joystick

    def execute(self):
        rospy.loginfo("Starting Teleoperation!")
        self.state = 'EXE'

    def reset(self):
        rospy.loginfo("Reseting Teleoperation!")
        self.state = 'IDLE'
    
    def end(self):
        self.stop()
        self.state = 'IDLE'
        self.msg.event = 'end_teleoperation'
        self.pub.publish(self.msg)                                      # Send message signaling the error

    def abort(self):
        rospy.loginfo("Aborting Teleoperation!")
        self.stop()
        self.state = 'IDLE'

    def error(self):
        self.stop()
        self.state = 'ERROR'
        self.msg.event = 'teleoperation_error'
        self.pub.publish(self.msg)                                      # Send message signaling the error

    def stop(self):
        self.move_to(self.odometry.position.x,self.odometry.position.y, self.current_height,0.0)

    def Joy_callback(self,msg):
        if self.state == 'EXE':
            z_speed = msg.axes[1]             # Get vertical speed
            x_speed = msg.axes[3]             # Get horizontal speed
            rot = msg.axes[2]                # Get angular speed

            self.__tele_msg.linear.x = x_speed*self.current_speed
            self.__tele_msg.linear.z = z_speed*self.current_speed
            self.__tele_msg.angular.z = rot*self.current_ang_speed

            #Send the desired position
            self.__tele_pub.publish(self.__tele_msg)

            # Change linear speed
            if msg.buttons[4]:
                self.current_speed += self.max_vel*0.1
                if self.current_speed > self.max_vel:
                    self.current_speed = self.max_vel
            elif msg.buttons[6]:
                self.current_speed -= self.max_vel*0.1
                if self.current_speed < 0.05:
                    self.current_speed = 0.05

            # Change angular speed
            if msg.buttons[5]:
                self.current_ang_speed += self.max_ang_vel*0.1
                if self.current_ang_speed > self.max_ang_vel:
                    self.current_ang_speed = self.max_ang_vel 
            elif msg.buttons[7]:
                self.current_ang_speed -= self.max_ang_vel *0.1
                if self.current_ang_speed < 0.2:
                    self.current_ang_speed = 0.2
    
            if any(msg.buttons[4:8]):
                print("\n\nSPEED: {}".format(self.current_speed))
                print("ANGULAR SPEED: {}".format(self.current_ang_speed))

            if msg.buttons[9]:
                # Teleoperation ended
                self.end()
            elif all(msg.buttons[4:8]):
                # Teleoperation error
                self.error()

# ########################################################################
class safe_land(object):
    '''
        Allows a human to teleoperate the robot through a joystick.
    '''
    def __init__(self, name):
        self.robot_name = name
        self.state = 'IDLE' 

        # Landing service                                                                              
        self._land_client = SimpleActionClient("safe_land_server", ExecuteLandAction)                # Create a client to the v_search server
        self._land_client.wait_for_server()                                                          # Wait server to be ready
        
        self._land_goal = ExecuteLandGoal()                                                               # Message to send the goal region

        self.pub = rospy.Publisher("/{}/maneuvers/out".format(name), events_message, queue_size=10)    # Publisher object
        self.msg = events_message()                                                                    # Message object

    def execute(self, victims = None):
        rospy.loginfo("Starting Safe Land!")
        self.state = 'EXE'

        self._land_goal.victims_pose = victims

        # Start safe_land
        self._land_client.send_goal(self._land_goal)
        self._land_client.wait_for_result()
        state = self._land_client.get_state()                       # Get the state of the action
        print(state)

        if state == GoalStatus.SUCCEEDED:
            # safe_land successfully executed
            self.state = 'IDLE'                                             # Set IDLE state
            self.msg.event = 'end_safe_land'
            self.pub.publish(self.msg)                                      # Send the message signaling that the safe_land is complete
        else:
            # The server aborted the motion
            self.state = 'ERROR'                                            # Set ERROR state
            self.msg.event = 'safe_land_error'
            self.pub.publish(self.msg)                                      # Send message signaling the error   

    def reset(self):
        rospy.loginfo("Reseting Safe Land!")
        self.state = 'IDLE'

    def erro(self):
        rospy.loginfo("Safe Land Erro!")
        self.state = 'ERROR'                                                # Set ERROR state
        self._land_client.cancel_goal()                                # Cancel the motion of the robot


########################################################################
##### Maneuvers events callback ########################################
def maneuver_event(msg):
    global app, assess, search, rb, vsv, tele, land

    # Verify the received message
    if "approach" in msg.event:
        # Commands for approach maneuver
        if (msg.event == "start_approach") and (app.state == 'IDLE'):
            # Verify paramenters
            if msg.position:
                thread = Thread(target=app.execute,args=[msg.position[0], msg])
                thread.start()                                                              # Start approach
            else:
                rospy.logwarn("Wrong approach parameters! Must be [x,y,z,theta]")             # Missing parameters
        
        elif (msg.event == "suspend_approach") and (app.state == 'EXE'):
            app.suspend()
        elif (msg.event == "resume_approach") and (app.state == 'SUS'):
            thread = Thread(target=app.resume)
            thread.start()
        elif (msg.event == "reset_approach") and (app.state =='ERROR'):
            app.reset()
        elif (msg.event == "abort_approach") and (app.state == 'SUS'):
            app.abort()
        elif (msg.event == "approach_error") and (app.state in ['SUS','EXE']):
            app.erro()
        else:
            rospy.logwarn("Command not allowed!")

    elif "assessment" in msg.event:
        # Commands for assessment maneuver
        if (msg.event == "start_assessment") and (assess.state == 'IDLE'):
            # Verify paramenters
            if len(msg.position) > 1:                                                           # Need at least three points to create a polygon
                thread = Thread(target=assess.execute, args=[msg.position, msg])
                thread.start()                                                                  # Start assessment
            else:
                rospy.logwarn("Wrong assessment parameters! Must have a initial vertice and size of square.")             # Missing parameters
        
        elif (msg.event == "suspend_assessment") and (assess.state == 'EXE'):
            assess.suspend()
        elif (msg.event == "resume_assessment") and (assess.state == 'SUS'):
            thread = Thread(target=assess.resume)
            thread.start()
        elif (msg.event == "reset_assessment") and (assess.state =='ERROR'):
            assess.reset()
        elif (msg.event == "abort_assessment") and (assess.state == 'SUS'):
            assess.abort()
        elif (msg.event == "assessment_error") and (assess.state in ['SUS','EXE']):
            assess.erro()
        else:
            rospy.logwarn("Command not allowed!")

    elif "v_search" in msg.event:
        # Commands for v_search maneuver
        if (msg.event == "start_v_search") and (search.state == 'IDLE'):
            # Verify paramenters
            if len(msg.position) == 2:                                                           # Need at least three points to create a polygon
                thread = Thread(target=search.execute, args=[msg.position, msg])
                thread.start()                                                                   # Start v_search
            else:
                rospy.logwarn("Wrong v_search parameters! Must have a initial vertice and size of square.")             # Missing parameters
        
        elif (msg.event == "suspend_v_search") and (search.state == 'EXE'):
            search.suspend()
        elif (msg.event == "resume_v_search") and (search.state == 'SUS'):
            thread = Thread(target=search.resume)
            thread.start()
        elif (msg.event == "reset_v_search") and (search.state =='ERROR'):
            search.reset()
        elif (msg.event == "abort_v_search") and (search.state == 'SUS'):
            search.abort()
        elif (msg.event == "v_search_error") and (search.state in ['SUS','EXE']):
            search.erro()
        else:
            rospy.logwarn("Command not allowed!")

    elif "verification" in msg.event:
        # Commands for victim surroundings verification maneuver
        if (msg.event == "start_verification") and (vsv.state == 'IDLE'):
            if msg.position:
                thread = Thread(target=vsv.execute, args=[msg.info, msg.position[0], msg])
                thread.start()                                                                  # Start victim surroundings verification
            else:
                rospy.logerr("Null victim pose!!!")
        elif (msg.event == "suspend_verification") and (vsv.state == 'EXE'):
            vsv.suspend()
        elif (msg.event == "resume_verification") and (vsv.state == 'SUS'):
            thread = Thread(target=vsv.resume)
            thread.start()
        elif (msg.event == "reset_verification") and (vsv.state =='ERROR'):
            vsv.reset()
        elif (msg.event == "abort_verification") and (vsv.state == 'SUS'):
            vsv.abort()
        elif (msg.event == "verification_error") and (vsv.state in ['SUS','EXE']):
            vsv.erro()
        else:
            rospy.logwarn("Command not allowed!")

    elif "return" in msg.event:
        # Commands for returtn to base maneuver
        if (msg.event == "start_return") and (rb.state == 'IDLE'):
            thread = Thread(target=rb.execute)
            thread.start()                                                                        # Start return to base
        elif (msg.event == "suspend_return") and (rb.state == 'EXE'):
            rb.suspend()
        elif (msg.event == "resume_return") and (rb.state == 'SUS'):
            thread = Thread(target=rb.resume)
            thread.start()
        elif (msg.event == "reset_return") and (rb.state =='ERROR'):
            rb.reset()
        elif (msg.event == "abort_return") and (rb.state == 'SUS'):
            rb.abort()
        elif (msg.event == "return_error") and (rb.state in ['SUS','EXE']):
            rb.erro()
        else:
            rospy.logwarn("Command not allowed!")

    elif "teleoperation" in msg.event:
        # Commands for teleoperation maneuver
        if (msg.event == "start_teleoperation") and (tele.state =='IDLE'):
            thread = Thread(target=tele.execute)
            thread.start()                                                                      # Start teleoperation
        elif (msg.event == "reset_teleoperation") and (tele.state == 'ERROR'):
            tele.reset()
        elif (msg.event == "end_teleoperation") and (tele.state == 'EXE'):
            # Teleoperation ended
            tele.end()
        elif (msg.event == "abort_teleoperation") and (tele.state == 'EXE'):
            tele.abort()
        elif (msg.event == "teleoperation_error") and (tele.state == 'EXE'):
            # Teleoperation ended
            tele.error()
        else:
            rospy.logwarn("Command not allowed!")

    elif "safe_land" in msg.event:
        # Commands for safe_land maneuver
        if (msg.event == "start_safe_land") and (land.state =='IDLE'):
            thread = Thread(target=land.execute, args=[msg.position])
            thread.start()                                                                  # Start safe_land
        elif (msg.event == "reset_safe_land") and (land.state == 'ERROR'):
            land.reset()
        elif (msg.event == "safe_land_error") and (land.state == 'EXE'):
            # Teleoperation ended
            land.error()    
        else:
            rospy.logwarn("Command not allowed!")



if __name__=="__main__":
    global app, assess, search, rb, vsv, tele, land
    NAME = rospy.get_param("robot_name", default = "")

    # Return to base parameters
    x_coord = rospy.get_param("xcoordinate", default = 0.0)
    y_coord = rospy.get_param("ycoordinate", default = 0.0)
    z_coord = rospy.get_param("zcoordinate", default = 0.0)
    
    # VSV parameters
    min_dist = rospy.get_param("vsv_min_dist", default = 1.0)
    max_dist = rospy.get_param("vsv_max_dist", default = 5.0)
    vsv_rounds = rospy.get_param("vsv_rounds", default = 2)
    vsv_round_points = rospy.get_param("vsv_round_points", default = 8)
    height = rospy.get_param("vsv_height", default = 8)

    rospy.init_node("{}_maneuvers".format(NAME), anonymous=False)           # Initialize maneuvers node

    # Enable the quadrotor motors
    rospy.wait_for_service("enable_motors")
    enabler = rospy.ServiceProxy("enable_motors",EnableMotors)
    enabler(True)

    # Create object for each type of maneuver
    app = approach(NAME)
    assess = assessment(NAME)
    search = v_search(NAME)
    vsv = surroundings_verification(NAME, min_dist, max_dist, vsv_rounds, vsv_round_points, height)
    rb = return_to_base(NAME, x_coord, y_coord, z_coord)
    tele = teleoperation(NAME)
    land = safe_land(NAME)

    # Subscribe to maneuvers in topic
    rospy.Subscriber("maneuvers/in", events_message, maneuver_event, queue_size=10)            # Topic to receive command events

    rospy.spin()
