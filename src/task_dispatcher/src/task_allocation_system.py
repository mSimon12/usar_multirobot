#!/usr/bin/env python

from threading import Condition
import pandas as pd
import rospy

from Mission import Mission
from DFS import DFS

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from system_msgs.msg import abstractions, events_message, mission, task_message
from nav_msgs.msg import Odometry

# Global Variables
robots_info_me = Condition()
robots_info = pd.DataFrame(columns=['bat', 'pose', 'vs', 'gs', 'status', 'last_task_id', 'current_task_id'])

missions = pd.DataFrame(columns = ['priority', 'tasks', 'current_task'])

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

        # Add the new mission to the dataframe
        missions.loc[m.id] = [float(m.priority), m.tasks, 0]

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

            # print("\n\n")
            # robots_info_me.acquire()
            # print(robots_info)
            # robots_info_me.release()
            # print("\n\n")

            print("\n\nMISSION TASKS:")
            print("{}\n\n".format(missions))

            ################### Select the next tasks of the sequence of each mission #####################
            current_tasks = Mission().tasks
            for i in missions.index:
                # Get current task description of the mission i
                task_name = i + "_{}".format(missions.loc[i,'current_task'])
                current_tasks.loc[task_name] = missions.loc[i,'tasks'].loc[missions.loc[i,'current_task']]  
                current_tasks.loc[task_name,'priority'] = missions.loc[i,'priority']
            ###############################################################################################

            #Select robots that can execute the tasks
            robots_info_me.acquire()
            robots = robots_info
            robots_info_me.release()

            # Require replanning
            self.allocate(robots, current_tasks)

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

        print("\n\nSelected tasks: {}\n".format(tasks_node.getValue()))

        for t in tasks_node.getValue():
            task_pub = rospy.Publisher("/{}/task".format(t[1]),task_message, queue_size=10)
            
            # Build the message for task requisition
            task_msg = task_message()
            task_msg.id = t[0]
            task_msg.task = tasks.loc[t[0],'maneuver']
            task_msg.gas_sensor = tasks.loc[t[0],'gs']
            task_msg.victim_sensor = tasks.loc[t[0],'vs']

            # Define task position or region
            if tasks.loc[t[0],'maneuver'] == 'approach':
                pos = Twist()
                pos.linear.x = tasks.loc[t[0],'position']['x']
                pos.linear.y = tasks.loc[t[0],'position']['y']
                pos.linear.z = tasks.loc[t[0],'position']['z']
                pos.angular.z = tasks.loc[t[0],'position']['z']
                task_msg.position.append(pos)
            elif tasks.loc[t[0],'maneuver'] in ['assessment', 'search']:
                pos = Twist()
                pos.linear.x = tasks.loc[t[0],'region']['x0']
                pos.linear.y = tasks.loc[t[0],'region']['y0']
                pos.linear.z = tasks.loc[t[0],'region']['z0']
                task_msg.position.append(pos)
                
                pos = Twist()
                pos.linear.x = tasks.loc[t[0],'region']['x1']
                pos.linear.y = tasks.loc[t[0],'region']['y1']
                pos.linear.z = tasks.loc[t[0],'region']['z1']
                task_msg.position.append(pos)

            r = rospy.Rate(20)
            while(task_pub.get_num_connections()<1):
                r.sleep()
                print("Connections: {}".format(task_pub.get_num_connections()))
            task_pub.publish(task_msg)
            # task_pub.unregister()

            #Update robot info
            robots_info.loc[t[1],'last_task_id'] = robots_info.loc[t[1],'current_task_id']
            robots_info.loc[t[1],'current_task_id'] = t[0]

        print(robots_info)


class RobotStateMachine(object):

    def __init__(self, name):
        self.name = name

        self.trace = {}

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
            # Signal the need of replanning due to the new mission received
            if robots_info.loc[self.name,'current_task_id'] == msg.task_id:
                # Get mission name
                try:
                    msg_mission = [m for m in missions.index if m in msg.task_id][0]
                except:
                    pass
                # Move to next task
                missions.loc[msg_mission,'current_task'] += 1

                #Update robot info
                robots_info.loc[t[1],'last_task_id'] = robots_info.loc[t[1],'current_task_id']
                robots_info.loc[t[1],'current_task_id'] = None
                
                # Remove mission from the list if all tasks have been finished
                if missions.loc[msg_mission,'current_task'] > len(missions.loc[msg_mission,'tasks'].index):
                    missions.drop(index = msg_mission, inplace = True)

            replan_flag.acquire()
            replan_flag.notify()
            replan_flag.release()
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
        robots_info.loc[self.name,'bat'] = msg.param[0]
        robots_info_me.release()


if __name__ == '__main__':
    try:
        rospy.init_node('task_allocation_system', anonymous=False)      # Initialize the node of the sensor
        tasks = AllocationSystem()                                      # Initialize Allocation System

        tasks.execute()                                                 # Start main loop
        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass
