#!/usr/bin/env python3

# General libs
import os
import time
import inspect
import glob

import pandas as pd
import PySimpleGUI as sg

# Supervisor libs
import OP.EVENTS as events_module
import OP.STATES as states_module

# ROS libs
import rospy
from geometry_msgs.msg import Twist
# from actionlib import SimpleActionClient
# from move_base_msgs.msg import MoveBaseAction
from interfaces.msg import trace_events
from system_msgs.msg import events_message


trace_filename = None

class EventInterface(object):
    '''
        Interface for executing events and visualizing automata.
    '''
    def __init__(self, robots_names, sm_path):

        # Set environment variable required for the Interface execution
        # os.environ["DISPLAY"]=":0"

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
        self.new_trace = False
        self.update_allowed_events = False
        self.update_model = False

        # Get name of the Machines
        self.sm_path = sm_path
        self.models = None

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
        self.main = [
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
        
        # start the Window
        # self.window = sg.Window("EVENTS TRIGGER INTERFACE", size=(650,500)).layout(self.main)
        self.window = sg.Window("EVENTS TRIGGER INTERFACE", size=(650,500),layout = self.main, resizable = True)

        self.models_window = None
        
        
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
        self.robots_events[msg.robot] = [e for e in msg.possible_events if ((not self.__events[e].is_controllable()) and ('end' not in e))]
        self.update_allowed_events = True     

        # Update models images
        self.models = [os.path.basename(x) for x in glob.glob(self.sm_path + "*.png")]
        self.update_model = True


    def run(self):
        '''
            Main loop of the interface for generating events
        '''
        self.events_sub = rospy.Subscriber("/events_trigger_ihm_in", trace_events, self.events_callback) 

        pub = None
        rate = rospy.Rate(10)
        self.param = []                                                     # Parameters of the event

        while not rospy.is_shutdown():
            #Get data from the Window
            event, values = self.window.Read(timeout=10)
            if event in (None, 'Cancel'):                                   # If user closes window or clicks cancel
                print('\nCLOSING EVENT INTERFACE ...\n')
                break

            if self.models_window:
                event, m_values = self.models_window.Read(timeout=10)
                if event in (None, 'Cancel'): 
                    self.models_window.Close()
                    self.models_window = None
                else:
                    values = {**values, **m_values}

            ## Second Window events ####################
            if (event == 'models') and (not self.models_window):
                initial_model = [e for e in self.models if (self.robots[1] + '_PLANT') in e][0]
                initial_path = self.sm_path + initial_model
                initial_values = [e for e in self.models if (self.robots[1] + '_PLANT') in e]
                self.models_layout = [
                    # MODELS
                    [sg.Text("Model type: "), sg.Radio("PLANT", "type", key= 'plant_model', default = True, enable_events= True), sg.Radio("SUPERVISOR", "type", key = 'sup_model', enable_events= True)],
                    [sg.Text("Robot: "), sg.InputCombo(values = self.robots[1:], default_value= self.robots[1], key = 'models_robot_selected', size = (30,10), enable_events = True)],
                    [sg.Text("Model: "), sg.InputCombo(values = initial_values, default_value = initial_model, key = 'selected_model', size = (30,10), enable_events = True)],
                    [sg.Image(filename = initial_path, key="_IMAGE_", background_color="white")],
                ] 
                self.models_window = sg.Window("MODELS VISUALIZER", size=(650,500),layout = self.models_layout, finalize = True, resizable = True)

            elif event == 'plant_model':
                self.models_window.Element('selected_model').update(values = [e for e in self.models if (values['models_robot_selected'] + '_PLANT') in e])

            elif event == 'sup_model':
                self.models_window.Element('selected_model').update(values = [e for e in self.models if (values['models_robot_selected'] + '_SUP') in e])

            elif event == 'models_robot_selected':
                if values['plant_model']:
                    self.models_window.Element('selected_model').update(values = [e for e in self.models if (values['models_robot_selected'] + '_PLANT') in e])
                else:
                    self.models_window.Element('selected_model').update(values = [e for e in self.models if (values['models_robot_selected'] + '_SUP') in e])

            elif event == 'selected_model':
                #Update the Automaton Image
                try:
                    self.models_window.Element("_IMAGE_").update(filename = self.sm_path + values['selected_model'])
                except:
                    pass
            ##############################################

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
            
            if event == 'trigger':
                # An event is triggered
                try:
                    robot_namespace = '/' + values['selected_robot'] + '/'
                    event = values['selected_event']

                    # Translate non-controllable events to low-level call
                    ll_event = self.translation_table[(self.translation_table['high-level'] == event)]['low-level'].array[0]
                    topic = robot_namespace + self.translation_table[(self.translation_table['high-level'] == event)]['topic'].array[0]

                    if 'bat_' in event:
                        # Fake battery state change
                        topic = topic.replace('/out','/in')                                             # Get battery_monitor/in topic
                        pub = rospy.Publisher("{}".format(topic), events_message, queue_size=10) 
                        msg = events_message()
                        msg.event = ll_event
                        if (event == 'bat_OK') or (event == 'uav_bat_OK'):
                            msg.param.append(70.0)                                                      # At level = 60 the system consider bat_OK
                        elif (event == 'bat_L') or (event == 'uav_bat_L'):
                            msg.param.append(24.5)                                                      # At level = 25 the system consider bat_L
                        elif (event == 'bat_LL') or (event == 'uav_bat_LL'):
                            msg.param.append(9.0)                                                       # At level = 9 the system consider bat_LL

                    elif 'failure' in ll_event or 'rst_f' in event:
                        # Fake failures
                        topic = topic.replace('/out','/in')                                             # Get failures_monitor/in topic
                        pub = rospy.Publisher("{}".format(topic), events_message, queue_size=10) 
                        msg = events_message()
                        msg.event = ll_event

                    elif ('gas_sensor/out' in topic) or ('victim_sensor/out' in topic):
                        # Fake sensor error
                        if ll_event in ['erro','reset']:
                            topic = topic.replace('/out','/in')                                         # Get sensor/in topic to fake a failure
                            pub = rospy.Publisher("{}".format(topic), events_message, queue_size=10) 
                            msg = events_message()
                            msg.event = ll_event
                        elif ll_event in ['gas_leak', 'victim_recognized']:
                            if len(self.param) > 2:
                                pub = rospy.Publisher("{}".format(topic), events_message, queue_size=10) 
                                msg = events_message()
                                msg.event = ll_event

                                p = Twist()
                                p.linear.x = self.param[0]
                                p.linear.y = self.param[1]
                                p.linear.z = self.param[2]

                                msg.param.append(p)
                            else:
                                sg.popup_error('Param error!')

                    elif 'error' in ll_event:
                        # Fake errors
                        topic = topic.replace('/out','/in')                                             # Get failures_monitor/in topic
                        pub = rospy.Publisher("{}".format(topic), events_message, queue_size=10) 
                        msg = events_message()
                        msg.event = ll_event

                    else:
                        # Another events
                        pub = rospy.Publisher("{}".format(topic), events_message, queue_size=10) 
                        msg = events_message()
                        msg.event = ll_event

                    if pub:
                        while pub.get_num_connections() < 1:
                            rate.sleep()
                        pub.publish(msg)
                    self.param = []                                                                         # Clear param
                    self.window['param_list'].Update(values=self.param)                                     # Clear param screen
                except:
                    sg.popup_error("No robot or event selected!")

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

                self.trace.to_csv(trace_filename)

            if self.update_allowed_events:
                self.update_allowed_events = False

                # Update events to trigger
                self.window.Element('selected_event').update('')
                self.window.Element('selected_event').update(values = self.robots_events[values['selected_robot']])

            if self.update_model:
                if self.models_window:
                    self.models_window.Element("_IMAGE_").update(filename= self.sm_path + values['selected_model'])
                self.update_model = False
                    

        self.window.Close()

    ###############################################################################################

if __name__ == '__main__':
    try:
        #Change to the current directory
        path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path)

        trace_filename = path + '/events_log/{}.csv'.format(time.strftime("%b-%d-%Y  %H:%M:%S"))

        robots = rospy.get_param("robots", default = [])
        state_machines = rospy.get_param("/events_trigger_interface/sm_path", default = '')

        rospy.init_node('events_trigger', anonymous=False)                            # Initialize the node of the interface
        interface = EventInterface(robots, state_machines)                            # Initialize Interface object

        interface.run()                                         # Start main loop
        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass
