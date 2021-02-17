#!/usr/bin/env python

from threading import Thread, Condition
import rospy

from lib.ProductSystem import g_var
from system_msgs.msg import abstractions


class EventsFilter(object):
    '''
		Class that filters the events to a higher abstraction level required by the Allocation System
	'''
    def __init__(self):
        last_event_monitor = Thread(target=self.event_monitor)
        status_monitor = Thread(target=self.status_monitor)
        
        self.pub = rospy.Publisher('events_abstractions', abstractions, queue_size=10)
        self.msg = abstractions()
        
        last_event_monitor.start()
        status_monitor.start()
        
    def event_monitor(self):
        '''
            Monitor occurred events that may affect the allocation system
        '''
        while not rospy.is_shutdown():
            #  Monitors last event
            g_var.trace_update_flag.acquire()
            g_var.trace_update_flag.wait()
            
            self.current_status = g_var.events_trace.tail(1)            # Get the last update
            self.__last_id = self.current_status.index[0]               # Get id of the last occured event
            
            g_var.trace_update_flag.release()
            
            last_event = self.current_status['event'].array[0]
            # states = self.current_status['states'].values[0]
            # param = self.current_status['event_params'].values[0]

            # Verify failures on sensors
            self.msg.event = None
            if last_event in ['uav_er_vs', 'er_vs']:
                self.msg.event = 'vs_unallowed'
            elif last_event in ['uav_er_gs', 'er_gs']:
                self.msg.event = 'gs_unallowed'
            elif last_event in ['uav_rst_vs', 'rst_vs']:
                self.msg.event = 'vs_allowed'
            elif last_event in ['uav_rst_gs', 'rst_gs']:
                self.msg.event = 'gs_allowed'

            if self.msg.event:
                self.pub.publish(self.msg)
                
    def status_monitor(self):
        '''
            Monitor changes on the robot and mission status through g_var.manager_info
            status = ['lazy', 'busy', 'unable']
            tasks contain a dictionary with the status of all received task_ids
            task_status = ['executing', 'suspended', 'finished', 'aborted']
		'''
        g_var.manager_info_flag.acquire()
        last_status = g_var.manager_info['status']                             # Get initial status
        last_task_info = {'id': None , 'status': None}      # Get initial task status
        g_var.manager_info_flag.release()
        
        while not rospy.is_shutdown():
            # Monitors the tasks status and robot capabilities
            g_var.manager_info_flag.acquire()
            g_var.manager_info_flag.wait()
            
            if g_var.manager_info['status'] != last_status:
				# Send new robot status
                self.msg.event = 'robot_' + g_var.manager_info['status'] 
                self.pub.publish(self.msg)

				# Update last status
                last_status = g_var.manager_info['status'] 

			# Verify if there is a change of task being executed
            if g_var.manager_info['current_task'] != None:
                if g_var.manager_info['current_task'] != last_task_info['id']:
                    # Send last status of last task
                    if last_task_info['id'] != None:
                        self.msg.event = 'last_task_' + g_var.manager_info['tasks'][last_task_info['id']]
                        self.pub.publish(self.msg)
                    
                    # Send status of current task
                    self.msg.event = 'current_task_' + g_var.manager_info['tasks'][g_var.manager_info['current_task']]
                    self.pub.publish(self.msg)

                    # Update info of last changes
                    last_task_info['id'] = g_var.manager_info['current_task']
                    last_task_info['status'] = g_var.manager_info['tasks'][g_var.manager_info['current_task']]

                # Verifies if the current tasks has a status change
                elif g_var.manager_info['tasks'][g_var.manager_info['current_task']] != last_task_info['status']:
                    # Send status of current task
                    self.msg.event = 'current_task_' + g_var.manager_info['tasks'][g_var.manager_info['current_task']]
                    self.pub.publish(self.msg)

                    # Update info of last changes
                    last_task_info['status'] = g_var.manager_info['tasks'][g_var.manager_info['current_task']]
                
            g_var.manager_info_flag.release()