import time
import inspect
from uav.tasks_UAV import AbortM
import pandas as pd
from threading import Thread, Condition
import rospy

# import ugv.tasks_UGV_samples as tasks       # To implement wrong sequences
import ugv.tasks_UGV as tasks
from lib.ProductSystem import g_var, trigger_event
from system_msgs.msg import task_message, events_message, required_events

import OP.EVENTS as events_module

# List of events that require a parameter
P_EVENTS = ['st_app','st_vsv','st_exp','rep_victim','rep_gas']      
BASELINE_PRIORITY = 10  

'''
Behaviors types priorities:
    1 - CRITIC_FAILURE and CRITICAL_BAT
    2 - teleoperation required by the commander
    3 - Mi_ERROR or POS_ERROR (require teleoperation)
    4 - victim found
    5 - gas found
    6 - BAT_LOW and SIMPLE_FAILURE
    7 - main_tasks
    8 - nothing

    * Then verify if the selected tasks can be executed due to VS_ERROR or GS_ERROR
'''


class TaskManager(Thread):
    '''
        This class implements the Task Manager, component responsible for deciding wich 
        enabled event to be triggered in the next step.

        This is a Thread, so you can implement a loop into the 'run' method that constantly
        updates the event to be executed.
    '''

    def __init__(self):
        Thread.__init__(self)

        self.robot_name = rospy.get_param("robot_name", default="")
        self.req_event_pub = rospy.Publisher("/deliberative_layer_required_events", required_events, queue_size=10)

        # Variables to control the reception of new events or tasks
        self.update_flag = Condition()              # Flag to signal new cycle
        self.__last_id = -1                         # Variable to control new events received

        # Variables to control current task and main task (task required by the commander)
        self.main_task = None
        self.main_task_id = None
        self.current_task = None

        # Varible to activate a behavior when something is found
        self.foundV = False
        # self.foundG = None 
        self.tele_ok = True  
        self.teleB = False                
 
        #BACKUP BEHAVIORS
        self.CM = tasks.CriticSystem()
        self.TeleM = tasks.HRI()
        self.DM1 = tasks.DegradedMode1()
        self.DM2 = tasks.DegradedMode2()
        self.VM = tasks.Victim()  

        # self.BB = tasks.GoBackToBase()                      # Behavior to return to base
        # self.Abort = tasks.AbortM()                         # Behavior to abort current task and turn off sensors
        # self.Pose_Erro = tasks.PosErro()
        # self.teleoperation = None

        # Variable to control events priorities
        self.events_priority = {}

        # Get all events call in the module
        self.events = {}
        for x in inspect.getmembers(events_module,inspect.isclass):
            if not 'uav' in x[0]:
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
        elif len(task.position) == 1:
            task_position.append(task.position[0].linear.x)
            task_position.append(task.position[0].linear.y)
            task_position.append(task.position[0].angular.z)

        valid_task = False

        # Create the main_task according the type of action required by the Commander
        if task.task == 'approach':
            self.main_task = tasks.UGV_approach(task_position, task.victim_sensor, task.gas_sensor)              #Create object of the main task
            valid_task = True
        elif task.task == 'exploration':
            self.main_task = tasks.UGV_exploration(task_position, task.victim_sensor, task.gas_sensor)           #Create object of the main task
            valid_task = True
        # elif task.task == 'verification':
        #     self.main_task = tasks.UGV_verification(task_position, task.victim_sensor, task.gas_sensor)          #Create object of the main task
        elif task.task == 'return_to_base':
            self.main_task = tasks.UGV_return(task_position, task.victim_sensor, task.gas_sensor)                #Create object of the main task
            valid_task = True

        elif not task.id:
            if self.main_task_id:
                g_var.manager_info_flag.acquire()
                g_var.manager_info['tasks'][self.main_task_id] = 'aborted'      # Update info about last task status
                g_var.manager_info['status'] = 'idle'
                g_var.manager_info_flag.notify()
                g_var.manager_info_flag.release()
            self.main_task = None                                    # Select abort as current task
            self.main_task_id = None

        if valid_task:
            # Subscribe the last task by the new one, flaging that the last one is aborted
            g_var.manager_info_flag.acquire()

            #Update last task
            if self.main_task_id:
                g_var.manager_info['tasks'][self.main_task_id] = 'aborted'

            # Save the new id of the task
            self.main_task_id = task.id
            g_var.manager_info['tasks'][self.main_task_id] = 'executing'

            #Update new task
            g_var.manager_info['current_task'] = self.main_task_id
            g_var.manager_info['status'] = 'busy'
            g_var.manager_info_flag.notify()
            g_var.manager_info_flag.release()

        ###############################################################
        

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

            # Get last event, states of the plant and the parameter of the event that just occured
            last_event = self.current_status['event'].array[0]
            states = self.current_status['states'].values[0]
            param = self.current_status['event_params'].values[0]

            # Print the event that just occured
            # print("\n[Task Manager]: Last event --> {} (param = {})".format(last_event, self.current_status['event_params']))

            # # Print enabled events
            # enabled_events = self.current_status['enabled_events'].array[0]
            # print("[Task Manager]: Enabled_events --> ", enabled_events)

            # # Print current states
            # print("[Task Manager]: Current states: ")
            # for s in self.current_status['states'].values[0]:
            #     print(f"\t{s.upper()}: {self.current_status['states'].values[0][s]}")

            #Verify if the main task has been acomplished
            if self.main_task and (self.main_task.next_event(states.values(), last_event, param) == 'task_done'):
                rospy.loginfo("[Task Manager]: TASK '{}' accomplished!!!!!!".format(self.main_task_id))
                g_var.manager_info_flag.acquire()
                g_var.manager_info['tasks'][self.main_task_id] = 'finished'
                if g_var.manager_info['status'] == 'busy':
                    g_var.manager_info['status'] = 'idle'
                # Reset task
                self.main_task = None
                self.main_task_id = None
                g_var.manager_info_flag.notify()
                g_var.manager_info_flag.release()

                

            # Signal that a new event was received
            self.update_flag.acquire()
            self.update_flag.notify()
            self.update_flag.release()


    def updatePriorities(self):
        '''
        Create a dictionary with the execution priority of each event
            # 0: disabled controllable events
            # 1: uncontrollable events
            # 2 - n: enabled controllable events that are required by the deliberative layer
        '''

        #Reset all priorities
        for x in self.events:
            if self.events[x].is_controllable():            # Controllable events receive priority 0
                self.events_priority[x] = 0
            else:                                           # Uncontrollable events receive priority 1
                self.events_priority[x] = 1

        ##########################################################################################################
        # Verify the state of the plant to define if the main task is executed or a backup plan

        # Get last event, states of the plant and the parameter of the event that just occured
        states = self.current_status['states'].values[0]
        last_event = self.current_status['event'].array[0]
        param = self.current_status['event_params'].values[0]

        # g_var.manager_info['status'] = 'idle'      

        # VERIFY EVENTS AND STATES THAT TRIGGER BACKUP BEHAVIORS ###############################################################################

        # Teleoperation control START and STOP condition
        if (last_event == 'call_tele'):
            self.teleB = True
        elif (last_event in ['er_tele', 'end_tele']) and (isinstance(self.current_task, tasks.HRI)):
            self.teleB = False

        # VICTIM behavior START and STOP condition
        if (last_event == 'victim_found'):
            self.foundV = True
        elif (self.foundV) and (last_event in ['end_vsv']) and (isinstance(self.current_task, tasks.Victim)):
            self.foundV = False

        ########################################################################################################################################

        ##### Select the task to be executed (the main_task or backup behaviors) #####
        # if self.main_task_id:
        g_var.manager_info_flag.acquire()

        # BEHAVIOR 1 -> CRITICAL SYSTEM
        if (any([states['battery_monitor'] == 'BAT_CRITICAL', states['failures'] == 'CRITIC_FAILURE'])):
            self.current_task = self.CM           # Get mode of operation object            

            ## Set status for ALLOCATION SYSTEM
            g_var.manager_info['status'] = 'unable'
            if self.main_task_id:
                g_var.manager_info['tasks'][self.main_task_id] = 'aborted'
                self.main_task = None

        # BEHAVIORS 2 -> HUMAN ROBOT INTERFACE
        elif self.teleB or (any([states['approach'] == 'APP_ERROR', states['exploration'] == 'EXP_ERROR', states['victims_surroundings_verification'] == 'VSV_ERROR', states['return_to_base'] == 'RB_ERROR'])):
            self.current_task = self.TeleM            # Get mode of operation object 

            ## Set status for ALLOCATION SYSTEM
            # g_var.manager_info['status'] = 'busy'
            if self.main_task_id:
                g_var.manager_info['tasks'][self.main_task_id] = 'suspended'     
            
        # BEHAVIOR 3 -> DEGRADED MODE 2
        elif (states['failures'] == 'POS_FAILURE') or (self.main_task and any([(states['victims_recognition_system'] == 'VS_ERROR') and ('vs' in self.current_task.getSensors()), 
                                                        (states['gas_sensor'] == 'GS_ERROR') and ('gs' in self.current_task.getSensors())])):
            self.current_task = self.DM2            # Get mode of operation object 

            ## Set status for ALLOCATION SYSTEM
            g_var.manager_info['status'] = 'unable'
            if self.main_task_id:
                g_var.manager_info['tasks'][self.main_task_id] = 'aborted'
                self.main_task = None

        # BEHAVIOR 4 -> VICTIM FOUND
        elif self.foundV:        
            self.current_task = self.VM            # Get mode of operation object 

            ## Set status for ALLOCATION SYSTEM
            # g_var.manager_info['status'] = 'busy'
            if self.main_task_id:
                g_var.manager_info['tasks'][self.main_task_id] = 'suspended'
                # self.main_task = None

        # BEHAVIOR 5 -> DEGRADED MODE 1                          
        elif (states['battery_monitor'] == 'BAT_LOW') or (states['failures'] == 'SIMPLE_FAILURE'):
            if self.current_task != self.DM1:
                        self.DM1.restart()
            self.current_task = self.DM1            # Get mode of operation object 

            ## Set status for ALLOCATION SYSTEM
            g_var.manager_info['status'] = 'unable'                         # The robot is not allowed to receive new tasks
            if self.main_task and (last_event == 'st_rb'):
                # g_var.manager_info['status'] = 'unable'                         # The robot is not allowed to receive new tasks
                # g_var.manager_info['tasks'][self.main_task_id] = 'aborted'
                self.main_task = None
                self.main_task_id = None

        # ASSIGNED BEHAVIOR -> execute the task assigned by the Task Alocator
        else:
            if self.main_task:
                # Execute main task
                self.current_task = self.main_task
                
                # Update task variable
                g_var.manager_info['status'] = 'busy'
                if self.main_task_id:
                    g_var.manager_info['tasks'][self.main_task_id] = 'executing'
            else:
                # if((not isinstance(self.current_task, tasks.AbortM)) or (not self.current_task.next_event(states.values(), last_event))):
                self.current_task = tasks.Task()

                g_var.manager_info['status'] = 'idle'
        
        g_var.manager_info_flag.notify()
        g_var.manager_info_flag.release()
        # else:
        #      self.current_task = self.main_task

        ##########################################################################################################
        table = []
        baseline_events = []

        if self.current_task:
            # Get table of priorities
            table = self.current_task.get_priorities_table()

            #Get next events allowed by the current selected task
            baseline_events = self.current_task.next_event(states.values(), last_event, param)
        rospy.loginfo("Next required events: {}".format(baseline_events))

        ## Publish next required event or events
        req_event_msg = required_events()
        req_event_msg.robot = self.robot_name

        if baseline_events:
            for e in baseline_events:
                req_event_msg.desired_events.append(e)
        self.req_event_pub.publish(req_event_msg)

        rospy.loginfo("Baseline: {}".format(baseline_events))
        rospy.loginfo("Table: {}".format(table))

        # Set events priorities for events in table
        if table:
            for e in table:
                self.events_priority[e] = table[e]

        # Set priorities according table of the current mode of operation
        if baseline_events:
            for e in baseline_events:
                self.events_priority[e] = BASELINE_PRIORITY

        # Set the event priority to zero if it is disabled by the supervisor
        for e in self.events:
            if self.events[e].is_controllable() and (e not in self.current_status['enabled_events'].array[0]):
                    self.events_priority[e] = 0                     # Controllable and disabled event



        self.events_priority = {k: v for k, v in sorted(self.events_priority.items(), key=lambda item: item[1])}
        print("PRIORITIES:\n")
        for e in self.events_priority:
            print("{} -> {}\n".format(e,self.events_priority[e]))


    # def updatePriorities(self):
    #     '''
    #     Create a dictionary with the execution priority of each event
    #         # 0: controllable events not required
    #         # 1: uncontrollable events
    #         # 2: controllable event that is required for the task execution
    #     '''
    #     next_task_events = []

    #     #Reset all priorities
    #     for x in self.events:
    #         if self.events[x].is_controllable():
    #             self.events_priority[x] = 0
    #         else:
    #             self.events_priority[x] = 1

    #     ##########################################################################################################
    #     # Verify the state of the plant to define if the main task is executed or a backup plan

    #     # Get last event, states of the plant and the parameter of the event that just occured
    #     states = self.current_status['states'].values[0]
    #     last_event = self.current_status['event'].array[0]
    #     param = self.current_status['event_params'].values[0]

    #     # g_var.manager_info['status'] = 'idle'

    #     #### CLEAR VARIABLES RELATED TO MANEUVERS ############################################################################
    #     if (last_event == 'er_tele') and (isinstance(self.teleoperation,tasks.ReqHelp)):
    #         g_var.manager_info['status'] = 'unable'
    #         g_var.manager_info['tasks'][self.main_task_id] = 'aborted'
    #         self.main_task = None
    #         self.main_task_id = None
    #         self.tele_ok = False
        
    #     # Teleoperation control
    #     if self.teleoperation and (not self.teleoperation.next_event(states.values(), last_event, param)):
    #         self.teleoperation = None


    #     # Verify if 'Found behaviors' have been accomplished
    #     if (self.foundV) and (not self.foundV.next_event(states.values(), last_event)):
    #         self.foundV = None
    #     elif (self.foundG) and (not self.foundG.next_event(states.values(), last_event)):
    #         self.foundG = None
    #     ######################################################################################################################

    #     # VERIFY EVENTS AND STATES THAT TRIGGER BACKUP BEHAVIORS ##############################################################################

    #     # Verify events that afect the behavior
    #     if (last_event == 'victim_found'):
    #         self.foundV = tasks.V_Found(param) 
    #     elif (last_event == 'gas_found'):
    #         self.foundG = tasks.G_Found(param) 
    #     # BEHAVIOR 2 -> human assistance due to maneuvers errors
    #     elif self.tele_ok and (any([states['approach'] == 'APP_ERROR', states['exploration'] == 'EXP_ERROR',
    #         states['victims_surroundings_verification'] == 'VSV_ERROR', states['return_to_base'] == 'RB_ERROR'])):
    #         if not self.current_task == self.teleoperation:
    #             self.teleoperation = tasks.ReqHelp()
    #     # BEHAVIOR 3 -> teleoperation required by the Commander 
    #     elif (last_event == 'call_tele'):
    #         self.teleoperation = tasks.TeleCalled()
    #         self.tele_ok = True
    #     ########################################################################################################################################


    #     ##### Select the task to be executed (the main_task or backup behaviors) #####
    #     # if self.main_task_id:
    #     g_var.manager_info_flag.acquire()
    #     # BEHAVIOR 1 -> System on Critical state
    #     if (any([states['battery_monitor'] == 'BAT_CRITICAL', states['failures'] == 'CRITIC_FAILURE'])):
    #             if self.current_task != self.Abort:  
    #                 self.Abort.restart()
    #             self.current_task = self.AbortDEGR
    #             g_var.manager_info['status'] = 'unable'
    #             if self.main_task_id:
    #                 g_var.manager_info['tasks'][self.main_task_id] = 'aborted'
    #                 self.main_task = None
    #     else:
    #         # BEHAVIORS 2 and 3 -> teleoperation required by the Commander or due to failures
    #         if self.teleoperation:
    #             self.current_task = self.teleoperation
    #             # g_var.manager_info['status'] = 'busy'
    #             if self.main_task_id:
    #                 g_var.manager_info['tasks'][self.main_task_id] = 'suspended'     
            
    #         # BEHAVIOR 4 -> position failure    
    #         elif states['failures'] == 'POS_FAILURE':
    #             if self.current_task != self.Pose_Erro:  
    #                 self.Pose_Erro.restart()
    #             self.current_task = self.Pose_Erro
    #             g_var.manager_info['status'] = 'unable'
    #             if self.main_task_id:
    #                 g_var.manager_info['tasks'][self.main_task_id] = 'aborted'
    #                 self.main_task = None    
    #         else:
    #             # BEHAVIOR 5 -> report victim pose and execute VSV
    #             if self.foundV:        
    #                 self.current_task = self.foundV  
    #                 g_var.manager_info['status'] = 'busy'
    #                 if self.main_task_id:
    #                     g_var.manager_info['tasks'][self.main_task_id] = 'suspended'
    #                     # self.main_task = None
    #             # BEHAVIOR 6 -> report gas leak position                           
    #             elif self.foundG:            
    #                 self.current_task = self.foundG
    #                 # if self.main_task_id:
    #                 #     g_var.manager_info['tasks'][self.main_task_id] = 'suspended'
    #             else:
    #                 # BEHAVIOR 7 -> finish the last task and return to base
    #                 if (states['battery_monitor'] == 'BAT_LOW') or (states['failures'] == 'SIMPLE_FAILURE'):
    #                     g_var.manager_info['status'] = 'unable'                         # The robot is not allowed to receive new tasks
    #                     if self.current_task != self.BB:
    #                         self.BB.restart()
    #                         self.current_task = self.BB
    #                         if self.main_task and (last_event == 'st_rb'):
    #                             # g_var.manager_info['status'] = 'unable'                         # The robot is not allowed to receive new tasks
    #                             # g_var.manager_info['tasks'][self.main_task_id] = 'aborted'
    #                             self.main_task = None
    #                             self.main_task_id = None
    #                 else:
    #                     # ASSIGNED BEHAVIOR -> execute the task assigned by the Task Alocator
    #                     if self.main_task:
    #                         # Execute main task
    #                         self.current_task = self.main_task
                            
    #                         # Update task variable
    #                         if not isinstance(self.main_task , tasks.AbortM):
    #                             g_var.manager_info['status'] = 'busy'
    #                             if self.main_task_id:
    #                                 g_var.manager_info['tasks'][self.main_task_id] = 'executing'
    #                     else:
    #                         if((not isinstance(self.current_task, tasks.AbortM)) or (not self.current_task.next_event(states.values(), last_event))):
    #                             self.current_task = None
    #                         if not self.tele_ok:
    #                             g_var.manager_info['status'] = 'unable'
    #                         else: 
    #                             g_var.manager_info['status'] = 'idle'
        
    #     # Verify if the current task can be executed due to Sensor ERRORS
    #     if self.current_task and any([(states['victims_recognition_system'] == 'VS_ERROR') and ('vs' in self.current_task.getSensors()), 
    #                 (states['gas_sensor'] == 'GS_ERROR') and ('gs' in self.current_task.getSensors())]):
            
    #         if self.main_task and (self.current_task == self.main_task):
    #             # Set the main task as aborted but does not make the robot unable to execute missions
    #             g_var.manager_info['status'] = 'idle'
    #             if self.main_task_id:
    #                 g_var.manager_info['tasks'][self.main_task_id] = 'aborted'
    #             self.main_task = None
            
    #         if self.current_task != self.Abort:  
    #             self.Abort.restart()
    #         self.current_task = self.Abort

    #     g_var.manager_info_flag.notify()
    #     g_var.manager_info_flag.release()
    #     # else:
    #     #      self.current_task = self.main_task

    #     ##########################################################################################################

    #     #Get next events allowed by the current selected task
    #     if self.current_task:
    #         next_task_events = self.current_task.next_event(states.values(), last_event, param)
    #     else:
    #         next_task_events = []
    #     rospy.loginfo("Next required events: {}".format(next_task_events))

    #     ## Publish next required event or events
    #     req_event_msg = required_events()
    #     req_event_msg.robot = self.robot_name
    #     for e in next_task_events:
    #         req_event_msg.desired_events.append(e)
    #     self.req_event_pub.publish(req_event_msg)

    #     # Set priorities according status of the events
    #     for e in next_task_events:
    #         if self.events[e].is_controllable() and (e in self.current_status['enabled_events'].array[0]):
    #                 self.events_priority[e] = 2                     # Controllable and enabled event

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
                    rospy.loginfo(self.current_task.getTaskParam())
                    trigger_event(next_event, self.current_task.getTaskParam())          # Call the execution of the controllable event
                else:
                    trigger_event(next_event)                                            # Call the execution of the controllable event

