#!/usr/bin/env python

from threading import Condition
import pandas as pd
import rospy

from Mission import Mission

from system_msgs.msg import abstractions, events_message, mission
from nav_msgs.msg import Odometry

# Global Variables
robots_info_me = Condition()
robots_info = pd.DataFrame(columns=['bat', 'pose', 'vs', 'gs', 'status', 'last_task_id', 'current_task_id'])

replan_flag = Condition()           #Signal the requirement of a replanning



class AllocationSystem(object):

    def __init__(self):
        self.uavs_names = rospy.get_param("uavs_names", default = [])
        self.ugvs_names = rospy.get_param("ugvs_names", default = [])

        pd.set_option("max_columns", None)

        for uav in self.uavs_names:
            # Initialize UAV monitor
            robots_info_me.acquire()
            robots_info.loc[uav] = [100, {'x': None, 'y': None, 'z': None}, 'ok', 'nok', 'lazy', None, None]
            robots_info_me.release()

            uav_SM = RobotStateMachine(uav)
            
            rospy.Subscriber("/{}/events_abstractions".format(uav), abstractions, uav_SM.events_callback)
            rospy.Subscriber("/{}/ground_truth/state".format(uav), Odometry, uav_SM.pose_callback)
            rospy.Subscriber("/{}/battery_monitor/out".format(uav), events_message, uav_SM.bat_callback)

        for ugv in self.ugvs_names:
            # Initialize UGV monitor
            robots_info_me.acquire()
            robots_info.loc[ugv] = [100, {'x': None, 'y': None, 'z': None}, 'ok', 'ok', 'lazy', None, None]
            robots_info_me.release()

            ugv_SM = RobotStateMachine(ugv)
            
            rospy.Subscriber("/{}/events_abstractions".format(ugv), abstractions, ugv_SM.events_callback)
            rospy.Subscriber("/{}/odom".format(ugv), Odometry, ugv_SM.pose_callback)
            rospy.Subscriber("/{}/battery_monitor/out".format(ugv), events_message, ugv_SM.bat_callback)
    
        # Subscribe to topic to receive missions
        rospy.Subscriber("/missions", mission, self.mission_callback)


    def mission_callback(self,msg):
        '''
            Callback for new received missions
        '''
        m = Mission()
        m.load(msg.filename)

        print("\nMISSION TASKS: \n{}\n\n".format(m.tasks))


    def execute(self):
        '''
            Loop where the allocation is executed
        '''
        rate = rospy.Rate(0.2)
        while not rospy.is_shutdown():
            print("\n\n")
            robots_info_me.acquire()
            print(robots_info)
            robots_info_me.release()
            print("\n\n")
            
            rate.sleep()


class RobotStateMachine(object):

    def __init__(self, name):
        self.name = name

        self.trace = {}

        # self.odometry_me = Condition()
        # self.odometry = None

    def events_callback(self,msg):
        '''
            Callback for events abstractions received from the robot. 
            Possible types of events:
            * Sensors status: 
                1 - Sensor allowed to use;
                2 - Sensor not allowed to use.
            * Robot working status:
                1 - Robot lazy: capable of executing tasks but currently doing nothing;
                2 - Robot busy: robot executing some maneuver;
                3 - Robot unable: robot not capable of accepting tasks. 
            * Tasks updates:
                1 - Last task status;
                2 - Current tasks status.
                ** task_status = ['executing', 'suspended', 'finished', 'aborted']
        '''

        # Sensors status update --- Monitor the status of the sensors: if it can be used or not
        if msg.event == 'vs_unallowed':
            robots_info.loc[self.name,'vs'] = 'nok'
        elif msg.event == 'vs_allowed':
            robots_info.loc[self.name,'vs'] = 'ok'
        elif msg.event == 'gs_unallowed':
            robots_info.loc[self.name,'gs'] = 'nok'
        elif msg.event == 'gs_allowed':
            robots_info.loc[self.name,'gs'] = 'ok'

        # Update robot working status
        elif msg.event == 'robot_lazy':
            robots_info.loc[self.name,'status'] = 'lazy'
        elif msg.event == 'robot_busy':
            robots_info.loc[self.name,'status'] = 'busy'
        elif msg.event == 'robot_unable':
            robots_info.loc[self.name,'status'] = 'unable'

        # Updates tasks status
        elif "task_executing" in msg.event:
            print("\n\nEXECUTING {}.\n\n".format(msg.task_id))
        elif "task_suspended" in msg.event:
            print("\n\nSUSPENDED {}.\n\n".format(msg.task_id))
        elif "task_finished" in msg.event:
            print("\n\nFINISHED {}.\n\n".format(msg.task_id))
        elif "task_aborted" in msg.event:
            print("\n\nABORTED {}.\n\n".format(msg.task_id))


    def pose_callback(self,msg):
        '''
            Monitor the current position of the robot
        '''
        robots_info_me.acquire()
        robots_info.loc[self.name,'pose']['x'] = msg.pose.pose.position.x
        robots_info.loc[self.name,'pose']['y'] = msg.pose.pose.position.y
        robots_info.loc[self.name,'pose']['z'] = msg.pose.pose.position.z
        robots_info_me.release()

    def bat_callback(self,msg):
        '''
            Updates the battery level of the robot
        '''
        robots_info_me.acquire()
        robots_info.loc[self.name,'bat'] = msg.param
        robots_info_me.release()


if __name__ == '__main__':
    try:
        rospy.init_node('task_allocation_system', anonymous=False)      # Initialize the node of the sensor
        tasks = AllocationSystem()                                      # Initialize Allocation System

        tasks.execute()                                                 # Start main loop
        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass
