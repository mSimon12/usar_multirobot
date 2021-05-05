#!/usr/bin/env python3

# General libs
import os
import time

import pandas as pd
import PySimpleGUI as sg
from threading import Condition

# ROS libs
import rospy

from system_msgs.msg import mission, missions_feedback, events_message
from Mission import Mission

# msg for pose monitor
from nav_msgs.msg import Odometry


class CommanderInterface(object):
    '''
        Interface for executing events and visualizing automata.
    '''
    def __init__(self, robots_names):

        # Set environment variable required for the Interface execution
        # os.environ["DISPLAY"]=":0"

        self.path = os.path.dirname(os.path.abspath(__file__))

        self.mission_pub = rospy.Publisher('/missions', mission, queue_size=10)
        self.missions = pd.DataFrame(columns = ['priority', 'n_tasks', 'current_task', 'progress', 'status', 'object'])
        self.missions_details = {}
        self.sended_missions = []

        self.robots = robots_names
        self.robots_buttons= {}

        # Intitialize variable to control reset butotns and teleoperation call
        for r in self.robots:
            self.robots_buttons[r] = {'tele': True, 'rst_f': False, 'rst_vs': False, 'rst_gs': False}

        ###############################################################################################
        #### -- Layout of the Window -- ###############################################################
        self.header_list = ['id', 'priority', 'n_tasks', 'current_task', 'progress (%)', 'status']
        self.tasks_menu = ['sequence', 'maneuver', 'agent', 'position', 'region', 'victim sensor', 'gas sensor']

        self.main = [
            # MISSIONS:
            [sg.Frame('MISSIONS:',[
                [sg.Table(values = [['','','','','','']], size = (70,18), background_color='white', text_color='black', col_widths=[5,15,15,15,15,30], auto_size_columns=False,
                          justification='left', key='missions', headings = self.header_list, right_click_menu = ['&Right', ['Add', 'Load', 'View/Edit', 'Send', 'Remove']])],
                          [sg.Button('ADD', key='Add', size=(5,1)),
                           sg.Button('LOAD', key='Load', size=(5,1)),
                           sg.Button('VIEW/EDIT', key='View/Edit', size=(8,1)),
                           sg.Button('SEND', key='Send', size=(5,1)),
                           sg.Button('REMOVE', key= 'Remove', size=(5,1))]
            ]),
            sg.Frame('CALLS:',[
                [sg.Text('Robot:'), sg.InputCombo(robots,default_value = robots[0], key='robot_to_call', size=(20,1), enable_events= True)],
                [sg.Button('call teleoperation', key = 'tele', button_color = ('white', 'green'), disabled_button_color = ('white', 'red'), use_ttk_buttons=True, size = (30,1))], 
                [sg.Button('reset failure', key = 'rst_f', button_color = ('white', 'green'), disabled_button_color = ('white', 'red'), use_ttk_buttons=True, disabled= True, size = (30,1))],
                [sg.Button('reset victim sensor', key = 'rst_vs', button_color = ('white', 'green'), disabled_button_color = ('white', 'red'), use_ttk_buttons=True, disabled= True, size = (30,1))], 
                [sg.Button('reset gas sensor', key = 'rst_gs', button_color = ('white', 'green'), disabled_button_color = ('white', 'red'), use_ttk_buttons=True, disabled= True, size = (30,1))]
            ], vertical_alignment= "top")],
            [sg.Frame('ROBOTS:',[
                [sg.Table(values = [['','','']], size = (90,10), background_color='white', text_color='black', col_widths=[15,12,28,35], auto_size_columns=False,
                          justification='left', key='robots_info', headings = ['robot', 'battery (%)', 'pose (m)', 'status'])],
            ])]
        ]
        
        # start the Window
        self.window = sg.Window("COMMANDER IHM", size=(1150,550),layout = self.main, resizable= True)
        ###############################################################################################

        self.last_time = {}
        for r in self.robots:
            self.last_time[r] = time.time()

        #### TOPICS SUBSCRIPTIONS
        # Missions feedback
        rospy.Subscriber('/missions_feedback',missions_feedback, self.missionsCallback)

        # Pose topics
        self.robots_info = {}
        self.status = {}
        self.odometry_me = Condition()
        for r in self.robots:
            self.odometry_me.acquire()
            self.robots_info[r] = [r, '','','OK']             # robot, battery, pose, status
            self.status[r] = ['OK', 'OK', 'OK']
            if 'pioneer3at' in r:
                rospy.Subscriber("/{}/odom".format(r), Odometry, self.poseCallback, callback_args = r)
                rospy.Subscriber("/{}/gas_sensor/out".format(r), events_message, self.statusCallback, callback_args = [r, 'gs'])
            elif 'UAV' in r:
                rospy.Subscriber("/{}/ground_truth/state".format(r), Odometry, self.poseCallback, callback_args = r)

            rospy.Subscriber("/{}/battery_monitor/out".format(r), events_message, self.batCallback, callback_args = r)
            rospy.Subscriber("/{}/failures_monitor/out".format(r), events_message, self.statusCallback, callback_args = [r, 'failures'])
            rospy.Subscriber("/{}/victim_sensor/out".format(r), events_message, self.statusCallback, callback_args = [r, 'vs'])
            
            self.odometry_me.release()
        self.update_robot_info = True

        #### TOPICS PUBLISHERS
        self.publishers = pd.DataFrame(columns = ['fail_monitor', 'vs', 'gs'])
        self.update_calls = False
        for r in self.robots:
            f_pub = rospy.Publisher("/{}/failures_monitor/in".format(r), events_message, queue_size = 10)
            vs_pub = rospy.Publisher("/{}/victim_sensor/in".format(r), events_message, queue_size = 10)
            gs_pub = None
            if 'pioneer3at' in r:
                gs_pub = rospy.Publisher("/{}/gas_sensor/in".format(r), events_message, queue_size = 10)

            self.publishers.loc[r] = [f_pub, vs_pub, gs_pub]
    

    def poseCallback(self, odometry, robot):
        '''
            Monitor the current position of the robot
        '''
        t = time.time()

        if t - self.last_time[robot] > 1.0:
            self.last_time[robot] = t

            self.odometry_me.acquire()
            self.robots_info[robot][2] = "x: {:.2f}  y: {:.2f}  z: {:.2f}".format(odometry.pose.pose.position.x, odometry.pose.pose.position.y, odometry.pose.pose.position.z)
            self.update_robot_info = True
            self.odometry_me.release()


    def batCallback(self, msg, robot):
        '''
            Monitor the battery level of the robot
        '''
        self.odometry_me.acquire()
        self.robots_info[robot][1] = "{:.2f}%".format(msg.param[0])
        self.update_robot_info = True
        self.odometry_me.release()


    def statusCallback(self, msg, args):
        '''
            Monitor the status of the robot
        '''
        robot = args[0]
        source = args[1]

        self.odometry_me.acquire()
        if source == 'failures':
            if msg.event == 'position_failure':
                self.status[robot][0] = 'POSITION FAILURE'
                self.robots_buttons[robot]['rst_f'] = True
            elif msg.event == 'slight_failure':
                self.status[robot][0] = 'SIMPLE FAILURE'
                self.robots_buttons[robot]['rst_f'] = True
            elif msg.event == 'critic_failure':
                self.status[robot][0] = 'CRITIC FAILURE'
                self.robots_buttons[robot]['rst_f'] = True
            elif msg.event == 'reset':
                self.status[robot][0] = 'OK'
                self.robots_buttons[robot]['rst_f'] = False
        
        elif source == 'vs':
            if msg.event == 'erro':
                self.status[robot][1] = 'VS_ERRO'
                self.robots_buttons[robot]['rst_vs'] = True
            elif msg.event == 'reset':
                self.status[robot][1] = 'OK'
                self.robots_buttons[robot]['rst_vs'] = False

        elif source == 'gs':
            if msg.event == 'erro':
                self.status[robot][2] = 'GS_ERRO'
                self.robots_buttons[robot]['rst_gs'] = True
            elif msg.event == 'reset':
                self.status[robot][2] = 'OK'
                self.robots_buttons[robot]['rst_gs'] = False
        
        if all(status == 'OK' for status in self.status[robot]):
            self.robots_info[robot][3] = 'OK'
        else:
            status_text = ''
            count = sum(status != 'OK' for status in self.status[robot])
            current = 1
            for s in self.status[robot]:
                if s != 'OK':
                    status_text += s
                    if current < count:
                        status_text += ' & '
                    current += 1

            self.robots_info[robot][3] = status_text
        self.update_robot_info = True
        self.odometry_me.release()

    def missionsCallback(self, msg):
        '''
            Monitors updates on missions status.
        '''
        for m in msg.missions:
            self.missions.loc[m.id, 'progress'] = m.progress
            
            if m.status == 'finished':
                self.missions.loc[m.id, 'status'] = 'mission complete'
                self.missions.loc[m.id, 'current_task'] = '-'
            else:
                self.missions.loc[m.id, 'current_task'] = int(m.status.replace(m.id + '_', ''))
                if m.robot:
                    self.missions.loc[m.id, 'status'] = m.robot + ' executing task'
                else:
                    self.missions.loc[m.id, 'status'] = 'idle'
        
        self.update_missions = True


    def run(self):
        '''
            Main loop of the interface for generating events
        '''
        self.update_missions = False                     # Flag the need of update of the table
        edit_mission_window = None                  # Singal if the Edit window is ON
        selected_mission = None                     # Current selected mission ID

        while not rospy.is_shutdown():
            #Get data from the Window
            event, values = self.window.Read(timeout=100)
            if event in (None, 'Cancel'):                                   # If user closes window or clicks cancel
                print('\nCLOSING COMMANDER INTERFACE ...\n')
                break

            if edit_mission_window:
                event, m_values = edit_mission_window.Read(timeout=10)
                if event in (None, 'Cancel'): 
                    edit_mission_window.Close()
                    edit_mission_window = None
                else:
                    values = {**values, **m_values}

            # Get selected mission id
            if values['missions'] and not edit_mission_window:
                table = self.window.Element('missions').Get()
                selected_mission = table[values['missions'][0]][0]

            msg = events_message()

            if (event == 'robot_to_call') or self.update_robot_info:
                for b in self.robots_buttons[values['robot_to_call']]:
                    self.window[b].update(disabled = not self.robots_buttons[values['robot_to_call']][b])
            elif event == 'tele':
                msg.event = 'call_teleoperation'
                self.publishers.loc[values['robot_to_call'],'fail_monitor'].publish(msg)
                pass
            elif event == 'rst_f':
                msg.event = 'reset'
                self.publishers.loc[values['robot_to_call'],'fail_monitor'].publish(msg)
            elif event == 'rst_vs':
                msg.event = 'reset'
                self.publishers.loc[values['robot_to_call'],'vs'].publish(msg)
            elif event == 'rst_gs':
                msg.event = 'reset'
                self.publishers.loc[values['robot_to_call'],'gs'].publish(msg)

            elif event == 'Add':
                add_layout = [
                    [sg.Text('Mission ID:', size = (17,1)), sg.Input(key='m_id', size=(10,1))],
                    [sg.Text('Mission PRIORITY:', size = (17,1)), sg.Input(key='m_p', size=(10,1))],
                    [sg.OK(), sg.Cancel()]
                ]
                add_window = sg.Window('NEW MISSION', layout = add_layout, size = (250,100))
                add_event, add_values = add_window.Read()
                add_window.Close()

                if add_event == 'OK':
                    if add_values['m_id'] not in self.missions.index:
                        if (int(float(add_values['m_p'])) < 10) and (int(float(add_values['m_p'])) >= 0): 
                            self.missions.loc[add_values['m_id']] = [int(float(add_values['m_p'])),0,0,0,'empty', Mission(add_values['m_id'], int(float(add_values['m_p'])))]
                            self.update_missions = True

                            self.missions_details[add_values['m_id']] = []      
                        else:
                            sg.popup_error('WRONG MISSION PRIORITY','Mission PRIORITY must be between 0 and 10!')
                    else:
                            sg.popup_error('WRONG MISSION ID','Mission ID already exist!')

            elif event == 'Load':
                load_path = sg.popup_get_file('Mission to load')

                if load_path:
                    loaded_mission = Mission()
                    loaded_mission.load(load_path)

                    mission_id = loaded_mission.id
                    mission_priority = loaded_mission.priority
                    n_tasks = len(loaded_mission.tasks.index)

                    self.missions.loc[mission_id] = [int(float(mission_priority)),n_tasks,0,0,'not sended', Mission(mission_id, int(float(mission_priority)))]
                    self.missions_details[mission_id] = [] 
                    seq = 0
                    for t in loaded_mission.tasks.index:
                        if not loaded_mission.tasks.loc[t,'agent']:
                            agent = ''
                        else:
                            agent = loaded_mission.tasks.loc[t,'agent']
                        maneuver = loaded_mission.tasks.loc[t,'maneuver']
                        vs = loaded_mission.tasks.loc[t,'vs']
                        gs = loaded_mission.tasks.loc[t,'gs']
                    
                        if maneuver == 'approach':
                            p = loaded_mission.tasks.loc[t,'position']
                            pos = [p['x'], p['y'], p['z'], p['theta']]
                            reg = []
                        elif maneuver in ['assessment','search']:
                            r = loaded_mission.tasks.loc[t,'region']
                            pos = []
                            reg = [r['x0'], r['y0'], r['x1'], r['y1']]
                        task = [seq, maneuver, agent, pos, reg, vs, gs]
                        seq += 1

                        self.missions_details[mission_id].append(task)

                    self.update_missions = True
            
            elif (event == 'View/Edit') and (not edit_mission_window) and selected_mission: 
                edit_m_layout = [
                    [sg.Table(values = [['','','','','']], size = (70,18), background_color='white', text_color='black', col_widths=[15,15,15,15,15,20,15], auto_size_columns=False,
                                justification='left', key='tasks', headings = self.tasks_menu)],
                    [sg.Button('ADD TASK', key='add_task', size=(6,1), button_color=('white','green')), 
                    sg.Button('REMOVE TASK', key='remove_task', size=(10,1), button_color=('white','red')),
                    sg.Button('/\\', key='task_up', size=(3,1), button_color=('white','purple')), 
                    sg.Button('\\/', key='task_down', size=(3,1), button_color=('white','purple'))]
                ]
                edit_mission_window = sg.Window('MISSION DETAILS', layout = edit_m_layout, size=(1050,370), finalize = True, resizable= True)

                if self.missions_details[selected_mission]:
                    edit_mission_window.Element('tasks').update(values = self.missions_details[selected_mission])

                event, m_values = edit_mission_window.Read(timeout=10)
                values = {**values, **m_values}

            # {'agent': None, 'position': None, 'region': None, 'vs': False, 'gs': False, 'maneuver': None}
            # ['sequence', 'maneuver', 'agent', 'position', 'region', 'victim sensor', 'gas sensor']
            elif (event == 'Send') and selected_mission and (selected_mission not in self.sended_missions):
                if self.missions_details[selected_mission]:
                    for t in self.missions_details[selected_mission]:
                        task = self.missions.loc[selected_mission, 'object'].get_std_task()
                        task['maneuver'] = t[1]
                        task['agent'] = t[2]
                        if t[3]:
                            task['position'] = {'x': float(t[3][0]), 'y': float(t[3][1]), 'z': float(t[3][2]), 'theta': float(t[3][3])}
                        if t[4]:
                            task['region'] = {'x0': float(t[4][0]), 'y0': float(t[4][1]), 'x1': float(t[4][2]), 'y1': float(t[4][3])}
                        task['vs'] = t[5]
                        task['gs'] = t[6]
                    
                        task = self.missions.loc[selected_mission, 'object'].add_task(task)

                    self.sended_missions.append(selected_mission)

                    #Send mission to task allocator
                    path = os.path.dirname(os.path.abspath(__file__))
                    mission_path = path + '/missions/{}.xml'.format(selected_mission)
                    self.missions.loc[selected_mission, 'object'].save(mission_path)

                    self.missions.at[selected_mission,'status'] = 'idle'

                    msg = mission()
                    msg.id = selected_mission
                    msg.filename = mission_path
                    msg.priority = self.missions.at[selected_mission,'priority']
                    self.mission_pub.publish(msg)

                    self.update_missions = True
                else:
                    sg.popup_error('EMPTY MISSION','Can not send empty mission!')

            elif (event == 'Remove') and selected_mission:
                # Send abort mission to task allocator

                if selected_mission in self.sended_missions:
                    msg = mission()
                    msg.id = selected_mission
                    msg.priority = -1
                    self.mission_pub.publish(msg)

                self.missions.drop(selected_mission, inplace = True)
                self.missions_details.pop(selected_mission)
                self.update_missions = True


            ## EDIT MISSION Window events ####################
            # Get selected task
            if edit_mission_window and values['tasks']:
                task_table = edit_mission_window.Element('tasks').Get()
                selected_task = task_table[values['tasks'][0]][0]
            else:
                selected_task = None

            if selected_mission not in self.sended_missions:

                if event == 'add_task':
                    robots = ['']
                    robots += self.robots

                    maneuvers = ['approach', 'assessment', 'search', 'return_to_base']

                    add_t_layout = [
                        [sg.Text('Agent:', size = (9,1)), sg.InputCombo(robots, default_value = '', key = 'agent', size = (17,1), enable_events = True)],
                        [sg.Text('Maneuver:', size = (9,1)), sg.InputCombo(maneuvers, default_value = maneuvers[0], key = 'maneuver', size = (17,1), enable_events = True)],
                        [sg.Frame('Position',[
                            [sg.Text('x:', size = (3,1)), sg.Input(key='pos_x', size=(6,1), disabled=False), 
                            sg.Text('y:', size = (3,1)), sg.Input(key='pos_y', size=(6,1), disabled=False)], 
                            [sg.Text('z:', size = (3,1)), sg.Input(key='pos_z', size=(6,1), disabled=False), 
                            sg.Text('\u03F4:', size = (3,1)), sg.Input(key='theta', size=(6,1), disabled=False)]
                        ])],
                        [sg.Frame('Region',[
                            [sg.Text('x0:', size = (3,1)), sg.Input(key='reg_x0', size=(6,1), disabled=True), sg.Text('y0:', size = (3,1)), sg.Input(key='reg_y0', size=(6,1), disabled=True)],
                            [sg.Text('\u0394x:', size = (3,1)), sg.Input(key='reg_x', size=(6,1), disabled=True), sg.Text('\u0394y:', size = (3,1)), sg.Input(key='reg_y', size=(6,1), disabled=True)],
                        ])],
                        [sg.Text('Victim Sensor Status:', size = (21,1)), sg.InputCombo([False, True], default_value = 'False', key = 'vs_status')],
                        [sg.Text('Gas Sensor Status:', size = (21,1)), sg.InputCombo([False, True], default_value = 'False', key = 'gs_status')],
                        [sg.OK(), sg.Cancel()]
                    ]
                    add_window = sg.Window('NEW TASK', layout = add_t_layout, size = (250,300), finalize=True)
                    
                    # ['sequence', 'maneuver', 'agent', 'position', 'region', 'victim sensor', 'gas sensor']
                    while True:
                        e, v = add_window.Read()

                        if e in (None, 'Cancel'):
                            add_window.Close()
                            break
                        elif e == 'OK':
                            ## Tasks is the next on the mission
                            if not self.missions_details[selected_mission]:
                                seq = 0
                            else:
                                seq = len(self.missions_details[selected_mission])

                            ok = True
                            for x in ['pos_x','pos_y','pos_z','theta','reg_x0','reg_y','reg_x','reg_y']:
                                if v[x] and not v[x].replace('.','',1).isdigit():
                                    ok = False

                            if ok:
                                if v['maneuver'] == 'approach':
                                    pos = [v['pos_x'], v['pos_y'], v['pos_z'], v['theta']]
                                    reg = []
                                elif v['maneuver'] in ['assessment','search']:
                                    pos = []
                                    reg = [v['reg_x0'], v['reg_y0'], v['reg_x'], v['reg_y']]
                                else:
                                    pos = []
                                    reg = []

                                task = [seq, v['maneuver'], v['agent'], pos, reg, v['vs_status'], v['gs_status']]
                                self.missions_details[selected_mission].append(task)
                                self.missions.loc[selected_mission, 'n_tasks'] += 1
                                self.missions.loc[selected_mission, 'status']  = 'not sended'
                                add_window.Close()

                                edit_mission_window.Element('tasks').update(values = self.missions_details[selected_mission])
                                self.update_missions = True
                            else:
                                sg.popup_error('WRONG VALUES ATTRIBUTION','Position and Region must be a number!')

                        elif e == 'agent':
                            if 'UAV' in v['agent']:
                                add_window['maneuver'].update(values = ['approach', 'assessment', 'search', 'return_to_base'])
                                add_window['gs_status'].update(values = [False])
                            elif 'pioneer3at' in v['agent']:
                                add_window['maneuver'].update(values = ['approach', 'search', 'return_to_base'])
                                add_window['gs_status'].update(values = [False, True])
                            else: 
                                add_window['maneuver'].update(values = ['approach', 'assessment', 'search', 'return_to_base'])
                                add_window['gs_status'].update(values = [False, True])

                        elif e == 'maneuver' :    
                            if v['maneuver'] in ['assessment', 'search']:
                                add_window['pos_x'].update(disabled = True)
                                add_window['pos_y'].update(disabled = True)
                                add_window['pos_z'].update(disabled = True)

                                add_window['reg_x0'].update(disabled = False)
                                add_window['reg_y0'].update(disabled = False)
                                add_window['reg_x'].update(disabled = False)
                                add_window['reg_y'].update(disabled = False)

                            elif v['maneuver'] == 'approach':
                                add_window['pos_x'].update(disabled = False)
                                add_window['pos_y'].update(disabled = False)
                                add_window['pos_z'].update(disabled = False)

                                add_window['reg_x0'].update(disabled = True)
                                add_window['reg_y0'].update(disabled = True)
                                add_window['reg_x'].update(disabled = True)
                                add_window['reg_y'].update(disabled = True)
                            else:
                                add_window['pos_x'].update(disabled = True)
                                add_window['pos_y'].update(disabled = True)
                                add_window['pos_z'].update(disabled = True)

                                add_window['reg_x0'].update(disabled = True)
                                add_window['reg_y0'].update(disabled = True)
                                add_window['reg_x'].update(disabled = True)
                                add_window['reg_y'].update(disabled = True)

                elif (event == 'remove_task') and selected_task != None:
                    # Não esta removendo o primeiro

                    self.missions_details[selected_mission]
                    self.missions_details[selected_mission].pop(selected_task)

                    for i in self.missions_details[selected_mission][selected_task:]:
                        self.missions_details[selected_mission][i[0]-1][0] = i[0]-1
                    self.missions.loc[selected_mission, 'n_tasks'] -= 1
                    edit_mission_window.Element('tasks').update(values = self.missions_details[selected_mission])
                    if not self.missions_details[selected_mission]:
                        self.missions.loc[selected_mission, 'status']  = 'empty'
                    self.update_missions = True
            
                elif event == 'task_up' and selected_task != None:
                    if selected_task > 0:
                        temp = self.missions_details[selected_mission][selected_task-1]
                        self.missions_details[selected_mission][selected_task][0] -= 1
                        self.missions_details[selected_mission][selected_task-1] = self.missions_details[selected_mission][selected_task]

                        self.missions_details[selected_mission][selected_task] = temp
                        self.missions_details[selected_mission][selected_task][0] += 1
                        edit_mission_window.Element('tasks').update(values = self.missions_details[selected_mission])
                
                elif event == 'task_down' and selected_task != None:
                    if selected_task < len(self.missions_details[selected_mission]):
                        temp = self.missions_details[selected_mission][selected_task+1]
                        self.missions_details[selected_mission][selected_task][0] += 1
                        self.missions_details[selected_mission][selected_task+1] = self.missions_details[selected_mission][selected_task]

                        self.missions_details[selected_mission][selected_task] = temp
                        self.missions_details[selected_mission][selected_task][0] -= 1
                        edit_mission_window.Element('tasks').update(values = self.missions_details[selected_mission])
            else:
                if event in ['add_task', 'remove_task', 'task_up', 'task_down']:
                    sg.popup_error('NOT EDITABLE','Already sended missions are not editable!')

            ##################################################

            if self.update_missions:
                self.update_missions = False
                table = []

                self.window.Element('missions').update(values = [])
                for m in self.missions.index:

                    table.append([m, self.missions.at[m,'priority'], self.missions.at[m,'n_tasks'],self.missions.at[m,'current_task'], self.missions.at[m,'progress'],self.missions.at[m,'status']])
                    self.window.Element('missions').update(values = table)

            if self.update_robot_info:
                self.update_robot_info = False
                v = []
                for r in self.robots_info:
                    v.append(self.robots_info[r])
                self.window.Element('robots_info').update(values = v)


        self.window.Close()

    ###############################################################################################

if __name__ == '__main__':
    try:
        #Change to the current directory
        path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path)

        robots = rospy.get_param("robots", default = [])
        # robots =  ['pioneer3at_1', 'UAV_1']     #rospy.get_param("robots", default = [])

        rospy.init_node('commander_ihm', anonymous=False)               # Initialize the node of the interface
        interface = CommanderInterface(robots)                            # Initialize Interface object

        interface.run()                                         # Start main loop
        rospy.spin()
            
    except rospy.ROSInterruptException:
        pass
