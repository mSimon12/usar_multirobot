#!/usr/bin/env python3

import time
import os
from threading import Condition
import pandas as pd
import rospy

from Mission import Mission
from DFS import DFS

from rosgraph_msgs.msg import Clock
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from system_msgs.msg import abstractions, events_message, mission, task_message, missions_feedback, m_status
from nav_msgs.msg import Odometry

# Global Variables

robots_info_me = Condition()
robots_info = pd.DataFrame(columns=['bat', 'pose', 'vs', 'gs', 'status', 'last_task_id', 'current_task_id'])

missions = pd.DataFrame(columns = ['priority', 'tasks', 'current_task', 'progress'])

trace_me = Condition()
trace = pd.DataFrame(columns = ['time', 'robot', 'robot_status', 'task', 'task_status'])
trace_filename = None

replan_flag = Condition()           #Signal the requirement of a replanning
global_time = 0
global_time_me = Condition()

class AllocationSystem(object):

    def __init__(self):
        self.uavs_names = rospy.get_param("uavs_names", default = [])
        self.ugvs_names = rospy.get_param("ugvs_names", default = [])


        ### Continue here - Create a variable that maintains all missions from beginning and monitors their progress -> missions?
        self.m_pub = rospy.Publisher("/missions_feedback",missions_feedback, queue_size=10)

        pd.set_option("max_columns", None)

        for uav in self.uavs_names:
            # Initialize UAV monitor
            robots_info_me.acquire()
            robots_info.loc[uav] = [100, {'x': None, 'y': None, 'z': None}, 'ok', 'nok', 'idle', None, None]
            robots_info_me.release()

            uav_SM = RobotStateMachine(uav)
            
            rospy.Subscriber("/{}/events_abstractions".format(uav), abstractions, uav_SM.events_callback)
            rospy.Subscriber("/{}/ground_truth/state".format(uav), Odometry, uav_SM.pose_callback)
            rospy.Subscriber("/{}/battery_monitor/out".format(uav), events_message, uav_SM.bat_callback)

        for ugv in self.ugvs_names:
            # Initialize UGV monitor
            robots_info_me.acquire()
            robots_info.loc[ugv] = [100, {'x': None, 'y': None, 'z': None}, 'ok', 'ok', 'idle', None, None]
            robots_info_me.release()

            ugv_SM = RobotStateMachine(ugv)
            
            rospy.Subscriber("/{}/events_abstractions".format(ugv), abstractions, ugv_SM.events_callback)
            rospy.Subscriber("/{}/odom".format(ugv), Odometry, ugv_SM.pose_callback)
            rospy.Subscriber("/{}/battery_monitor/out".format(ugv), events_message, ugv_SM.bat_callback)
    
        # Subscribe to topic to receive missions
        rospy.Subscriber("/missions", mission, self.mission_callback)
        rospy.Subscriber("/clock", Clock, self.time_update)

    def time_update(self, msg):
        global global_time
        global_time_me.acquire()
        global_time = msg.clock.secs
        global_time_me.release()

    def mission_callback(self,msg):
        '''
            Callback for new received missions
        '''
        m = Mission()
        if msg.priority >= 0:
            m.load(msg.filename)

            # Add the new mission to the dataframe
            missions.loc[m.id] = [float(m.priority), m.tasks, 0, 0]
        
        else:
            missions.drop(msg.id, inplace=True)         # Remove the mission

        # Signal the need of replanning due to the new mission received
        replan_flag.acquire()
        replan_flag.notify()
        replan_flag.release()

    def execute(self):
        '''
            Loop where the allocation is executed
        '''
        while not rospy.is_shutdown():
            replan_flag.acquire()
            replan_flag.wait()
            
            # print("\n\n\nREPLAN: ")
            # print(robots_info)

            # print("\n\nMISSION TASKS:")
            # print("{}\n\n".format(missions))

            ################### Select the next tasks of the sequence of each mission #####################
            current_tasks = Mission().tasks
            for i in missions.index:
                # Get current task description of the mission i
                if missions.loc[i,'current_task'] < len(missions.loc[i,'tasks'].index):
                    task_name = i + "_{}".format(missions.loc[i,'current_task'])
                    current_tasks.loc[task_name] = missions.loc[i,'tasks'].loc[missions.loc[i,'current_task']]  
                    current_tasks.loc[task_name,'priority'] = missions.loc[i,'priority']
            ###############################################################################################

            #Select robots that can execute the tasks
            robots_info_me.acquire()
            robots = robots_info.loc[robots_info['status'] != 'unable']           # Get only robots enabled (idle or busy)
            robots_info_me.release()

            # Require replanning and send tasks to robots
            if (not current_tasks.empty) and (not robots.empty):
                assign_tasks = self.allocate(robots, current_tasks)

            ## Update Commander
            mission_fbk = missions_feedback()
            for i in missions.index:
                m = m_status()
                m.id = i
                m.progress = missions.loc[i,'progress'] 

                # Get current task
                if missions.loc[i,'current_task'] >= len(missions.loc[i,'tasks'].index):
                    m.status = 'finished'
                else:
                    m.status = i + "_{}".format(missions.loc[i,'current_task'])

                m.robot = ''
                if assign_tasks:
                    for t in assign_tasks.getValue():
                        if t[0] == m.status:
                            m.robot = t[1]

                mission_fbk.missions.append(m)
            self.m_pub.publish(mission_fbk)

            replan_flag.release()


    def allocate(self, robots, tasks):
        '''
            Allocate tasks to robots
        '''
        rospy.loginfo("Searching for best robots allocation!")
        # print("\nROBOTS\n{}\n".format(robots))
        # print("\nTASKS:\n{}\n\n\n".format(tasks))

        # Sort tasks by priority
        tasks.sort_values(by=['priority'], ascending=True, inplace=True)

        # Build the Tree with all possible options
        search = DFS(robots,tasks)

        # Receive a node containing allocated tasks
        tasks_node = search.run()

        robots_info_me.acquire()

        ###### Send TASKS to ROBOTS ############################################################
        if tasks_node:
            rospy.loginfo("\n\nSelected tasks: {}\n".format(tasks_node.getValue()))
            for t in tasks_node.getValue():
                task_pub = rospy.Publisher("/{}/task".format(t[1]),task_message, queue_size=10)
                
                if t[0] != robots_info.loc[t[1],'current_task_id']:
                    # Build the message for task requisition
                    task_msg = task_message()
                    task_msg.id = t[0]

                    if tasks.loc[t[0],'maneuver'] == 'search':
                        if 'pioneer3at' in t[1]:
                            task_msg.task = 'exploration'
                        elif 'UAV' in t[1]:
                            task_msg.task = 'victim_search'
                    else:
                        task_msg.task = tasks.loc[t[0],'maneuver']
                    task_msg.gas_sensor = tasks.loc[t[0],'gs']
                    task_msg.victim_sensor = tasks.loc[t[0],'vs']

                    # Define task position or region
                    if tasks.loc[t[0],'maneuver'] == 'approach':
                        pos = Twist()
                        pos.linear.x = tasks.loc[t[0],'position']['x']
                        pos.linear.y = tasks.loc[t[0],'position']['y']
                        pos.linear.z = tasks.loc[t[0],'position']['z']
                        pos.angular.z = tasks.loc[t[0],'position']['theta']
                        task_msg.position.append(pos)
                    elif tasks.loc[t[0],'maneuver'] in ['assessment', 'search']:
                        pos = Twist()
                        pos.linear.x = tasks.loc[t[0],'region']['x0']
                        pos.linear.y = tasks.loc[t[0],'region']['y0']
                        # pos.linear.z = tasks.loc[t[0],'region']['z0']
                        task_msg.position.append(pos)
                        
                        pos = Twist()
                        pos.linear.x = tasks.loc[t[0],'region']['x1']
                        pos.linear.y = tasks.loc[t[0],'region']['y1']
                        # pos.linear.z = tasks.loc[t[0],'region']['z1']
                        task_msg.position.append(pos)

                    # Wait till it recognizes the subscribers
                    r = rospy.Rate(20)
                    while(task_pub.get_num_connections()<1):
                        r.sleep()

                    # Publish the task
                    task_pub.publish(task_msg)
                    # task_pub.unregister()

                    #Update robot info
                    robots_info.loc[t[1],'last_task_id'] = robots_info.loc[t[1],'current_task_id']
                    robots_info.loc[t[1],'current_task_id'] = t[0]

        ########################################################################################

        ## Abort tasks of unallocated robots
        for r in robots_info.index:
            if (not tasks_node) or (not [t for t in tasks_node.getValue() if t[1] == r]) and (robots_info.loc[r,'current_task_id']):
                # Send empty message
                if robots_info.loc[r,'status'] != 'unable':
                    task_pub = rospy.Publisher("/{}/task".format(r),task_message, queue_size=10)
                    task_msg = task_message()
                    task_pub.publish(task_msg)

                #Update robot info
                robots_info.loc[r,'last_task_id'] = robots_info.loc[r,'current_task_id']
                robots_info.loc[r,'current_task_id'] = None

        robots_info_me.release() 
        return tasks_node


class RobotStateMachine(object):

    def __init__(self, name):
        self.name = name

        self.task_status = None

    def events_callback(self,msg):
        '''
            Callback for events abstractions received from the robot. 
            Possible types of events:
            * Sensors status: 
                1 - Sensor allowed to use;
                2 - Sensor not allowed to use.
            * Robot working status:
                1 - Robot idle: capable of executing tasks but currently doing nothing;
                2 - Robot busy: robot executing some maneuver;
                3 - Robot unable: robot not capable of accepting tasks. 
            * Tasks updates:
                1 - Last task status;
                2 - Current tasks status.
                ** task_status = ['executing', 'suspended', 'finished', 'aborted']
        '''
        global trace, trace_filename

        trace_me.acquire()
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
        elif msg.event == 'robot_idle':
            if robots_info.loc[self.name,'status'] == 'unable':
                # Signal the need of replanning due to the new robot available
                replan_flag.acquire()
                replan_flag.notify()
                replan_flag.release()

            robots_info.loc[self.name,'status'] = 'idle'
        elif msg.event == 'robot_busy':
            robots_info.loc[self.name,'status'] = 'busy'
        elif msg.event == 'robot_unable':
            robots_info.loc[self.name,'status'] = 'unable'
            # Update trace & save it
            # trace = trace.append({'time':time.strftime("%H:%M:%S"), 'robot': self.name, 'robot_status': robots_info.loc[self.name,'status'], 'task': '-', 'task_status': '-'}, ignore_index = True)
            trace = trace.append({'time':global_time, 'robot': self.name, 'robot_status': robots_info.loc[self.name,'status'], 'task': '-', 'task_status': '-'}, ignore_index = True)
            trace.to_csv(trace_filename)

        # Updates tasks status
        elif "task_executing" in msg.event:
            print("\n{} EXECUTING {}.".format(self.name,msg.task_id))
            
            if robots_info.loc[self.name,'current_task_id'] == msg.task_id:
                # Update trace & save it
                # trace = trace.append({'time':time.strftime("%H:%M:%S"), 'robot': self.name, 'robot_status': robots_info.loc[self.name,'status'], 'task': msg.task_id, 'task_status': 'executing'}, ignore_index = True)
                trace = trace.append({'time':global_time, 'robot': self.name, 'robot_status': robots_info.loc[self.name,'status'], 'task': msg.task_id, 'task_status': 'executing'}, ignore_index = True)
                trace.to_csv(trace_filename)

        elif "task_suspended" in msg.event:
            print("\n{} SUSPENDED {}.".format(self.name,msg.task_id))
            
            if robots_info.loc[self.name,'current_task_id'] == msg.task_id:
                # Update trace & save it
                # trace = trace.append({'time':time.strftime("%H:%M:%S"), 'robot': self.name, 'robot_status': robots_info.loc[self.name,'status'], 'task': msg.task_id, 'task_status': 'suspended'}, ignore_index = True)
                trace = trace.append({'time':global_time, 'robot': self.name, 'robot_status': robots_info.loc[self.name,'status'], 'task': msg.task_id, 'task_status': 'suspended'}, ignore_index = True)
                trace.to_csv(trace_filename)

        elif "task_finished" in msg.event:
            print("\n{} FINISHED {}.".format(self.name,msg.task_id))
            
            # Signal the need of replanning due to the new mission received
            if robots_info.loc[self.name,'current_task_id'] == msg.task_id:
                # Get mission name
                try:
                    msg_mission = [m for m in missions.index if m in msg.task_id][0]
                except:
                    pass

                # Update mission progress
                missions.loc[msg_mission,'progress'] = int(((missions.loc[msg_mission,'current_task'] + 1) / len(missions.loc[msg_mission,'tasks'])) * 100)           

                # Move to next task
                missions.loc[msg_mission,'current_task'] += 1      

                #Update robot info
                robots_info.loc[self.name,'last_task_id'] = robots_info.loc[self.name,'current_task_id']
                robots_info.loc[self.name,'current_task_id'] = None

                replan_flag.acquire()
                replan_flag.notify()
                replan_flag.release()

            # Update trace & save it
            # trace = trace.append({'time':time.strftime("%H:%M:%S"), 'robot': self.name, 'robot_status': robots_info.loc[self.name,'status'], 'task': msg.task_id, 'task_status': 'finished'}, ignore_index = True)
            trace = trace.append({'time':global_time, 'robot': self.name, 'robot_status': robots_info.loc[self.name,'status'], 'task': msg.task_id, 'task_status': 'finished'}, ignore_index = True)
            trace.to_csv(trace_filename)

        elif "task_aborted" in msg.event:
            print("\n{} ABORTED {}.".format(self.name,msg.task_id))

            if robots_info.loc[self.name,'current_task_id'] == msg.task_id:

                #Update robot info
                robots_info.loc[self.name,'last_task_id'] = robots_info.loc[self.name,'current_task_id']
                robots_info.loc[self.name,'current_task_id'] = None

                # Signal the need of replanning due to the new mission received
                replan_flag.acquire()
                replan_flag.notify()
                replan_flag.release()

            # Update trace & save it
            # trace = trace.append({'time':time.strftime("%H:%M:%S"), 'robot': self.name, 'robot_status': robots_info.loc[self.name,'status'], 'task': msg.task_id, 'task_status': 'aborted'}, ignore_index = True)
            trace = trace.append({'time':global_time, 'robot': self.name, 'robot_status': robots_info.loc[self.name,'status'], 'task': msg.task_id, 'task_status': 'aborted'}, ignore_index = True)
            trace.to_csv(trace_filename)
        trace_me.release()
        # rospy.logwarn("\n\n{}".format(trace))


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
        robots_info.loc[self.name,'bat'] = msg.param[0]
        robots_info_me.release()


if __name__ == '__main__':
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        trace_filename = path + '/missions_sequences/{}.csv'.format(time.strftime("%b-%d-%Y  %H:%M:%S"))

        trace.index.name = "id"    

        rospy.init_node('task_allocation_system', anonymous=False)      # Initialize the node of the sensor
        tasks = AllocationSystem()                                      # Initialize Allocation System

        tasks.execute()                                                 # Start main loop
        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass
