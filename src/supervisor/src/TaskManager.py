import time
import inspect
import pandas as pd
from threading import Thread, Condition

from lib.ProductSystem import g_var, trigger_event
from system_msgs.msg import task_message, events_message

from lib.Automaton import MultiAutomata
import OP.EVENTS as events_module

class TaskManager(Thread):
    '''
        This class implements the Task Manager, component responsible for deciding wich 
        enabled event to be triggered in the next step.

        This is a Thread, so you can implement a loop into the 'run' method that constantly
        updates the event to be executed.
    '''

    def __init__(self):
        Thread.__init__(self)

        self.__last_id = -1                                             # Variable to control new events received

        aut = MultiAutomata('Behaviors')
        aut.read_xml('files/behaviors.xml')         # File with multiple Automata

        # Get representation of tasks
        self.B = pd.DataFrame(columns=['current_state','states','events','transitions'])        # Initialize a DataFrame to save all tasks status
        for b in aut.get_automata().values():
            states = b.get_states()
            current_state = states.loc[states['initial'] == True].index[0]                      # Get initial state
            self.B.loc[b.get_name()] = [current_state, states, b.get_events(), b.get_transitions()]
        self.main_task = ''
 
        # Variable to control events priorities
        self.events_priority = {}

        # Get all events call in the module
        self.events = {}
        for x in inspect.getmembers(events_module,inspect.isclass):
            self.events[x[0]] = x[1]  

        # Flag to signal new cycle
        self.update_flag = Condition()

        # Start the TaskManager
        self.start() 

        # Start thread for the tracer monitor
        trace_receiver = Thread(target=self.wait_events)              
        trace_receiver.start() 


    def taskCallback(self,task):
        '''
            Callback that subscribe to topic were tasks are received.
        '''
        self.main_task = task.task

        # Signal that a new task was received
        self.update_flag.acquire()
        self.update_flag.notify()
        self.update_flag.release()
        pass


    def wait_events(self):
        '''
            Wait till a new event is received.
        '''
        while True:
            g_var.trace_update_flag.acquire()
            g_var.trace_update_flag.wait()

            self.current_status = g_var.events_trace.tail(1)      # Get the last update
            self.__last_id = self.current_status.index[0]              # Get id of the last occured event

            g_var.trace_update_flag.release()

            # #Print the event that just occured
            # last_event = self.current_status['event'].array[0]
            # print("\n[Task Manager]: Last event --> {} (param = {})".format(last_event, self.current_status['event_params']))

            # # Print enabled events
            # enabled_events = self.current_status['enabled_events'].array[0]
            # print("[Task Manager]: Enabled_events --> ", enabled_events)

            # # Print current states
            # print("[Task Manager]: Current states: ")
            # for s in self.current_status['states'].values[0]:
            #     print(f"\t{s.upper()}: {self.current_status['states'].values[0][s]}")
        
            # Signal that a new event was received
            self.update_flag.acquire()
            self.update_flag.notify()
            self.update_flag.release()


    def updatePriorities(self):
        '''
        Create a dictionary with the execution priority of each event
            # 0: controllable events not required
            # 1: uncontrollable event not excpected
            # 2: controllable or uncontrollable event that is required for the task execution
        '''
        next_task_events = []

        for x in self.events:
            if self.events[x].is_controllable():
                self.events_priority[x] = 0
            else:
                self.events_priority[x] = 1

        #######################################################################################
        # Verify the state of the plant to define if the main task is executed or a backup plan
        states = self.current_status['states'].values[0]

        if states['battery_monitor'] == 'LOW':
            pass
        else:
            # Execute main task
            current_task = self.main_task

        if current_task:
            transitions = self.B.loc[current_task,'transitions']
            next_task_events = transitions.loc[transitions['st_node'] == self.B.loc[current_task,'current_state'],'event'].values

        #######################################################################################
        # Set priorities according status of the events
        for e in next_task_events:
            if self.events[e].is_controllable():
                if e in self.current_status['enabled_events'].array[0]:
                    self.events_priority[e] = 2                     # Controllable and enabled event
            else:
                self.events_priority[e] = 2                         # Uncontrollable event


    def run(self):
        while True:
            # Wait till an event occurs or a new task is received
            self.update_flag.acquire()
            self.update_flag.wait()
            self.update_flag.release()

            self.updatePriorities()

            print(self.events_priority)

            next_event = max(self.events_priority,key=self.events_priority.get)
            print(next_event)
            if self.events[next_event].is_controllable():
                trigger_event(next_event)                                             # Call the execution of the controllable event
