#!/usr/bin/env python

# General libs
import os
import inspect
import pandas as pd
import PySimpleGUI as sg

# Supervisor libs
import OP.EVENTS as events_module
import OP.STATES as states_module

# ROS libs
import rospy
# from actionlib import SimpleActionClient
# from move_base_msgs.msg import MoveBaseAction
from interfaces.msg import trace_events


class EventInterface(object):
    '''
        Interface for executing events and visualizing automata.
    '''
    def __init__(self, robots_names):

        # Set environment variable required for the Interface execution
        os.environ["DISPLAY"]=":0"

        # Events trace
        self.trace = pd.DataFrame(columns = ['robot', 'event', 'event_type', 'param', 'enabled_events', 'time'])
        
        # Variable that maitaints the allowed events
        self.robots_events = {}
        for r in robots_names:
            self.robots_events[r] = []

        #################################################################################
        #### -- Auxiliary variables -- ##################################################
        
        # Control of the tracer
        self.events_counter = 0
        # self.current_status_id = -1
        self.new_trace = False
        self.update_allowed_events = False

        # Get name of the Machines
        machines = [s[0] for s in inspect.getmembers(states_module,inspect.isclass)]

        # Get all events call in the module
        self.__events = {}
        for x in inspect.getmembers(events_module,inspect.isclass):
            self.__events[x[0]] = x[1]  

        # Get controllable events
        self.__cont_e = [e for e in self.__events if self.__events[e].is_controllable()]
       
        # Get uncontrollable events
        self.__not_cont_e = [e for e in self.__events if not self.__events[e].is_controllable()]

        # Get translation table
        self.translation_table = pd.read_csv("OP/translation_table.csv")

        self.robots = ['all']
        self.robots[1:] = robots_names

        #################################################################################
        #### -- Layout of the Window -- #################################################
        self.layout = [
            # TRACE: 
            [sg.Frame('TRACE:',[
                [sg.InputCombo(values = self.robots, default_value= self.robots[0], key='trace_option', enable_events=True, size= (25,10))],
                [sg.Text("Id"), sg.Text("Robot"), sg.Text("Event"), sg.Text("Parameters"), sg.Text("Time")],
                [sg.Multiline(size=(45,35), key='tracer', disabled=True, autoscroll=True, )],
                [sg.Input(visible=False, enable_events=True, key='save'), sg.FileSaveAs("SAVE", file_types = (("ALL Files", "*.*"),("CSV text",".csv")), target='save', enable_events=True), 
                    sg.Button("REFRESH", key='refresh')]
                ]),
            # TRIGGER
            sg.Column([
                [sg.Frame('TRRIGER EVENT:',[
                        [sg.Text("Robot: "), sg.InputCombo(values = self.robots[1:], default_value= self.robots[1], size=(20,10), key='selected_robot', enable_events=True)],
                        [sg.Text("Event: "),sg.InputCombo(values = [], default_value= '', size=(20,10), key='selected_event')],
                        [sg.HorizontalSeparator()],
                        [sg.Text('Parameters:')],
                        [sg.Input(key='new_param',enable_events=True, size=(25,5)),
                            sg.Button("+", key='add_param', size=(1,1), button_color=('white','green'))],
                        [sg.Listbox('', key='param_list', size=(30, 4))],
                        [sg.Button("-", key='remove_param', size=(28,1), button_color=('white','red'))],
                        [sg.Button('TRIGGER', key='trigger', size=(28,1))]
                        ])],
                [sg.Button('Vizualize Models', key='models', size=(28,1))]
            ])] 
        ]

        self.models_layout = [
            # MODELS
            [sg.Text("Model: "), sg.InputCombo(values = ['v1', 'v2'], key = 'model_selected', enable_events = True)]
        ] 
        
        # start the Window
        self.window = sg.Window("EVENTS TRIGGER INTERFACE", size=(650,500)).layout(self.layout)
        
        
    def events_callback(self,msg):
        '''
            Receives trace events
            event_trace = ['robot', 'event', 'event_type', 'param', 'enabled_events', 'time']
        '''
        if msg.last_event:

            self.events_counter += 1
            
            ## Get event type
            if self.__events[msg.last_event].is_controllable():
                event_type = 'controllable'
            else:
                event_type = 'uncontrollable'        

            ## Insert new trace event
            self.trace.loc[self.events_counter] = [msg.robot, msg.last_event, event_type, msg.param, msg.possible_events, msg.event_time]
            self.new_trace = True

        # Update allowed uncontrollable events
        self.robots_events[msg.robot] = [e for e in msg.possible_events if not self.__events[e].is_controllable()]
        self.update_allowed_events = True     


    def run(self):
        '''
            Main loop of the interface for generating events
        '''
        self.events_sub = rospy.Subscriber("/events_trigger_ihm_in", trace_events, self.events_callback) 

        self.param = []                                                     # Parameters of the event

        while not rospy.is_shutdown():
            #Get data from the Window
            event, values = self.window.Read(timeout=10)
            if event in (None, 'Cancel'):                                   # If user closes window or clicks cancel
                print('\nCLOSING EVENT INTERFACE ...\n')
                break

            elif event == 'models':
                pop = sg.Window("MODELS VISUALIZER", size=(200,200)).layout(self.models_layout)

            # Change on trace option
            if event in ['trace_option', 'refresh']:
                self.window['tracer'].update('')
                #Refresh tracer
                if not self.trace.empty: 
                    for i in self.trace.index:
                        if (values['trace_option'] == self.trace.at[i,'robot']) or (values['trace_option'] == 'all'):
                            if self.trace.at[i,'event_type'] == 'controllable':
                                color = 'blue'
                            else:
                                color = 'red'

                            if self.__events[self.trace.at[i,'event']].is_controllable():
                                color = 'blue'
                            else:
                                color = 'red'
                            text = self.trace.loc[[i]].drop(columns=['event_type','enabled_events']).to_string(header=False, justify='left')
                            self.window['tracer'].print(text, text_color=color) 
                        
            elif event == 'save':
                # Save content of tracer into a csv file
                filename = values['save']
                if filename:
                    if '.' not in filename:
                        filename += ".csv"

                    if '.csv' in filename:
                        self.trace.to_csv(filename)
                    else:
                        sg.Popup('Wrong file extension!', title='Saving failure!')
                    self.window['save'].update(value='')

            ## TRIGGER EVENTS

            elif event == 'selected_robot':
                # Update events to trigger
                self.window.Element('selected_event').update('')
                self.window.Element('selected_event').update(values = self.robots_events[values['selected_robot']])
            
            # if event == 'trigger':
            #     # An event is triggered
            #     if values['controllable'] == True:
            #         trigger_event(values['selected_event'], self.param)                             # Call the execution of the controllable event
            #     else:
            #         # Trigger uncontrollable events
            #         event = values['selected_event']

            #         # Translate non-controllable events to low-level call
            #         ll_event = self.translation_table[(self.translation_table['high-level']==event)]['low-level'].array[0]
            #         topic = self.translation_table[(self.translation_table['high-level']==event)]['topic'].array[0]

            #         # Fake uncontrollable events
            #         if 'erro' in ll_event:
            #             if 'maneuvers/out' in topic:
            #                 # Fake maneuver error
            #                 move_base_client = SimpleActionClient("{}move_base".format(rospy.get_namespace()), MoveBaseAction)     # Get move_base service
            #                 move_base_client.wait_for_server()
            #                 move_base_client.cancel_all_goals()                                         # Cancel the current motion
            #             elif ('gas_sensor/out' in topic) or ('victim_sensor/out' in topic):
            #                 # Fake sensor error
            #                 topic = topic.replace('/out','/in')                                         # Get sensor/in topic to fake a failure
            #                 pub = rospy.Publisher("/{}".format(topic), events_message, queue_size=10) 
            #                 msg = events_message()
            #                 msg.event = ll_event
            #                 pub.publish(msg)                                                            # Publish to the sensor topic
            #         elif 'bat_' in event:
            #             # Fake battery state change
            #             topic = topic.replace('/out','/in')                                             # Get battery_monitor/in topic
            #             pub = rospy.Publisher("/{}".format(topic), events_message, queue_size=10) 
            #             msg = events_message()
            #             msg.event = ll_event
            #             if event == 'bat_OK':
            #                 msg.param.append(60.0)                                                      # At level = 60 the system consider bat_OK
            #             elif event == 'bat_L':
            #                 msg.param.append(30.0)                                                      # At level = 30 the system consider bat_L
            #             elif event == 'bat_LL':
            #                 msg.param.append(9.0)                                                       # At level = 9 the system consider bat_LL
            #             pub.publish(msg)                                                                # Publish to the battery_monitor topic
            #         elif 'failure' in ll_event:
            #             # Fake failures
            #             topic = topic.replace('/out','/in')                                             # Get failures_monitor/in topic
            #             pub = rospy.Publisher("/{}".format(topic), events_message, queue_size=10) 
            #             msg = events_message()
            #             msg.event = ll_event
            #             pub.publish(msg)                                                                # Publish to the failures_monitor topic
            #         elif 'ihm' in topic:
            #             # Fake commander comands
            #             pub = rospy.Publisher("/{}".format(topic), events_message, queue_size=10) 
            #             msg = events_message()
            #             msg.event = ll_event
            #             pub.publish(msg)                                                                # Publish to the IHM/out topic

            #     self.param = []                                                                         # Clear param
            #     self.window['param_list'].Update(values=self.param)                                     # Clear param screen
            
                    
            elif event == 'add_param':
                # Add a new item as parameter for the event
                if values['new_param']:
                    self.param.append(eval(values['new_param'])) 
                    self.window['new_param'].update('')
                    self.window['param_list'].Update(values=self.param)

            elif event == 'remove_param':
                # Remove an item from the list of parameters
                if self.window['param_list'].GetIndexes():
                    item = self.window['param_list'].GetIndexes()[0]
                    self.param.pop(item)
                    self.window['param_list'].Update(values=self.param) 
            
            
            # New event occured
            if self.new_trace:
                self.new_trace = False

                # Update tracer screen
                # if self.trace.tail(1).index[0] > 0:
                if (values['trace_option'] == 'all') or (values['trace_option'] == self.trace.tail(1).iloc[0]['robot']):
                    if self.trace.tail(1).iloc[0]['event_type'] == 'controllable':
                        color = 'blue'
                    else:
                        color = 'red'
                    text = self.trace.tail(1).drop(columns=['event_type','enabled_events']).to_string(header=False, justify='left')
                    self.window['tracer'].print(text, text_color=color)     

            if self.update_allowed_events:
                self.update_allowed_events = False

                # Update events to trigger
                self.window.Element('selected_event').update('')
                self.window.Element('selected_event').update(values = self.robots_events[values['selected_robot']])
                    

        self.window.Close()

    ###############################################################################################

if __name__ == '__main__':
    try:
        #Change to the current directory
        path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path)

        robots = rospy.get_param("robots", default = [])

        rospy.init_node('events_trigger', anonymous=False)      # Initialize the node of the interface
        interface = EventInterface(robots)                            # Initialize Interface object

        interface.run()                                         # Start main loop
        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass