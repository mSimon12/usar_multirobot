import time
import inspect
import pandas as pd
from threading import Thread, Condition

import tasks
from lib.ProductSystem import g_var, trigger_event
from system_msgs.msg import task_message, events_message

import OP.EVENTS as events_module

# List of events that require a parameter
P_EVENTS = ['st_app','st_vsv','st_exp']        

class TaskManager(Thread):
    '''
        This class implements the Task Manager, component responsible for deciding wich 
        enabled event to be triggered in the next step.

        This is a Thread, so you can implement a loop into the 'run' method that constantly
        updates the event to be executed.
    '''

    def __init__(self):
        Thread.__init__(self)

        self.update_flag = Condition()              # Flag to signal new cycle
        self.__last_id = -1                         # Variable to control new events received

        self.main_task = None
        self.current_task = None

        self.foundB = False                         # Varible to activate a behavior when something is found
 
        #BACKUP BEHAVIORS
        self.BB = tasks.GoBackToBase()
        self.Abort = tasks.AbortM()

        # Variable to control events priorities
        self.events_priority = {}

        # Get all events call in the module
        self.events = {}
        for x in inspect.getmembers(events_module,inspect.isclass):
            self.events[x[0]] = x[1]  

        # Start the TaskManager
        self.start() 
 
        # Start thread for the tracer monitor
        trace_receiver = Thread(target=self.wait_events)              
        trace_receiver.start() 


    def taskCallback(self,task):
        '''
            Callback that subscribe to topic were tasks are received.
        '''      
        # Get position of the task
        task_position = []
        if len(task.position) > 1:
            # Create a vector of multiple points
            for p in task.position:
                task_position.append((p.linear.x, p.linear.y))
        else:
            task_position.append(task.position[0].linear.x)
            task_position.append(task.position[0].linear.y)
            task_position.append(task.position[0].angular.z)

        self.main_task_id = task.id

        if task.task == 'approach':
            self.main_task = tasks.UGV_approach(task_position, task.victim_sensor, task.gas_sensor)              #Create object of the main task
        elif task.task == 'exploration':
            self.main_task = tasks.UGV_exploration(task_position, task.victim_sensor, task.gas_sensor)           #Create object of the main task
        elif task.task == 'verification':
            self.main_task = tasks.UGV_verification(task_position, task.victim_sensor, task.gas_sensor)          #Create object of the main task
        elif task.task == 'return':
            self.main_task = tasks.UGV_return(task_position, task.victim_sensor, task.gas_sensor)                #Create object of the main task
        elif task.task == 'teleoperation':
            self.main_task = tasks.UGV_teleoperation(task_position, task.victim_sensor, task.gas_sensor)         #Create object of the main task

        # Make a historic of the tasks executed by the robot

        # Signal that a new task was received
        self.update_flag.acquire()
        self.update_flag.notify()
        self.update_flag.release()


    def wait_events(self):
        '''
            Wait till a new event is received.
        '''
        while True:
            g_var.trace_update_flag.acquire()
            g_var.trace_update_flag.wait()

            self.current_status = g_var.events_trace.tail(1)            # Get the last update
            self.__last_id = self.current_status.index[0]               # Get id of the last occured event

            g_var.trace_update_flag.release()

            # #Print the event that just occured
            last_event = self.current_status['event'].array[0]
            states = self.current_status['states'].values[0]
            param = self.current_status['event_params'].values[0]
            # print("\n[Task Manager]: Last event --> {} (param = {})".format(last_event, self.current_status['event_params']))

            # # Print enabled events
            # enabled_events = self.current_status['enabled_events'].array[0]
            # print("[Task Manager]: Enabled_events --> ", enabled_events)

            # # Print current states
            # print("[Task Manager]: Current states: ")
            # for s in self.current_status['states'].values[0]:
            #     print(f"\t{s.upper()}: {self.current_status['states'].values[0][s]}")

            #Verify if the task has been acomplished
            if self.main_task and (self.main_task.next_event(states.values(), last_event, param) == 'task_done'):
                print("[Task Manager]: TASK '{}' accomplished!!!!!!".format(self.main_task_id))
                g_var.manager_info['tasks'][self.main_task_id] = 'finished'

                # Reset task
                self.main_task = None

            # Signal that a new event was received
            self.update_flag.acquire()
            self.update_flag.notify()
            self.update_flag.release()


    def updatePriorities(self):
        '''
        Create a dictionary with the execution priority of each event
            # 0: controllable events not required
            # 1: uncontrollable event not excpected
            # 2: controllable event that is required for the task execution
        '''
        next_task_events = []

        #Reset all priorities
        for x in self.events:
            if self.events[x].is_controllable():
                self.events_priority[x] = 0
            else:
                self.events_priority[x] = 1

        #######################################################################################
        # Verify the state of the plant to define if the main task is executed or a backup plan
        states = self.current_status['states'].values[0]
        last_event = self.current_status['event'].array[0]
        param = self.current_status['event_params'].values[0]

        #Select the task to be executed (the main_task or backup behaviors)
        if last_event == 'victim_found':
            self.current_task = tasks.V_Found()
            self.foundB = True
        elif last_event == 'gas_found':
            self.current_task = tasks.G_Found()
            self.foundB = True
        
        if (self.foundB == True) and (not self.current_task.next_event(states.values(), last_event)):
            self.foundB = False
        
        if not self.foundB:
            if (states['battery_monitor'] == 'BAT_LOW') or (states['failures'] == 'SIMPLE_FAILURE'):
                g_var.manager_info['status'] = 'unable'                         # The robot is not allowed to receive new tasks
                # if self.main_task:
                    # g_var.manager_info['tasks'][self.main_task_id] = 'aborted'
                if self.current_task != self.BB:
                    self.BB.atBase = False
                    self.current_task = self.BB
                    if self.main_task:
                        self.main_task.restart()
            
            elif any([states['battery_monitor'] == 'BAT_CRITICAL', states['failures'] == 'CRITIC_FAILURE']):
                # insert here sensors failures if the current main_task depends on it
                self.current_task = self.Abort
                g_var.manager_info['status'] = 'unable'
                if self.main_task:
                    g_var.manager_info['tasks'][self.main_task_id] = 'aborted'
                    self.main_task = None

            else:
                if self.main_task:
                    # Execute main task
                    self.current_task = self.main_task
                    
                    # Update task variable
                    g_var.manager_info['status'] = 'busy'
                    g_var.manager_info['tasks'][self.main_task_id] = 'executing'
                else:
                    self.current_task = None
                    g_var.manager_info['status'] = 'lazy'

        #Get next events allowed by the current selected task
        if self.current_task:
            next_task_events = self.current_task.next_event(states.values(), last_event, param)
        else:
            next_task_events = []
       
        print("Next required events: {}".format(next_task_events))

        #######################################################################################
        # Set priorities according status of the events
        for e in next_task_events:
            if self.events[e].is_controllable() and (e in self.current_status['enabled_events'].array[0]):
                    self.events_priority[e] = 2                     # Controllable and enabled event

    def run(self):
        '''
            Main loop where the next event is executed according the priority table
        '''
        while True:
            # Wait till an event occurs or a new task is received
            self.update_flag.acquire()
            self.update_flag.wait()
            self.update_flag.release()

            self.updatePriorities()
            # print(self.events_priority)

            next_event = max(self.events_priority,key=self.events_priority.get)
            # print(next_event)
            if self.events[next_event].is_controllable():
                if next_event in P_EVENTS:
                    print(self.current_task.getTaskParam())
                    trigger_event(next_event, self.current_task.getTaskParam())          # Call the execution of the controllable event
                else:
                    trigger_event(next_event)                                            # Call the execution of the controllable event

