
from time import sleep

class Task(object):

    def __init__(self, param=[], vs_req = False, gs_req = False):
        self._param = param                                           # Atribute to save the parameter of the task
        self.__sensors = {'uav_on_vs': vs_req, 'uav_on_gs': gs_req}           # Save the required status of the sensors
        self._motion_done = False                                     # Monitor the motion execution
        self._last_task_aborted = False                               # Variable to abort last maneuver

    def getTaskParam(self):
        '''
            Return the parameter of the task
        '''
        return self._param
    
    def getSensors(self):
        return [sensor for sensor in self.__sensors if self.__sensors[sensor] == True]


    def next_event(self, states, last_event, event_param):
        return []

    
    def get_priorities_table(self):
        '''
            Priority of events affected by this mode of operation
        '''    
        table = {
            #Controllable
                'uav_off_vs':11, # 'uav_on_vs':0,
                'uav_rep_victim':15, 'uav_req_assist':15,
                # 'uav_st_app':0, 'uav_st_assess':0, 'uav_st_rb':0, 'uav_st_safe_land':0, 'uav_st_tele':0, 'uav_st_v_search':0, 'uav_st_vsv':0, 
                'uav_sus_app':11, 'uav_sus_assess':11, 'uav_sus_rb':11, 'uav_sus_v_search':11, 'uav_sus_vsv':11,
                # 'uav_rsm_app':0, 'uav_rsm_assess':0, 'uav_rsm_rb':0, 'uav_rsm_v_search':0, 'uav_rsm_vsv':0, 
                'uav_abort_app':11, 'uav_abort_assess':11, 'uav_abort_rb':11, 'uav_abort_v_search':11, 'uav_abort_tele':11, 'uav_abort_vsv':11, 
                'uav_rst_app':5, 'uav_rst_assess':5, 'uav_rst_rb':5, 'uav_rst_safe_land':5, 'uav_rst_tele':5, 'uav_rst_v_search':5, 'uav_rst_vsv':5, 

            #Uncontrollable
                # 'uav_bat_L':1, 'uav_bat_LL':1, 'uav_bat_OK':1,
                # 'uav_fail':1, 'uav_pos_fail':1, 'uav_critic_fail':1,
                # 'uav_victim_found':1, 'uav_call_tele':1,
                # 'uav_end_app':1, 'uav_end_assess':1, 'uav_end_rb':1, 'uav_end_safe_land':1, 'uav_end_tele':1, 'uav_end_v_search':1, 'uav_end_vsv':1,
                # 'uav_er_app':1, 'uav_er_assess':1, 'uav_er_rb':1, 'uav_er_safe_land':1, 'uav_er_tele':1, 'uav_er_v_search':1, 'uav_er_vsv':1, 
                # 'uav_er_vs':1,
                # 'uav_rst_f':1, 'uav_rst_vs':1
                }

        return table

    def restart(self):
        self._motion_done = False
        self._last_task_aborted = False


##########################################################################################################
# --- UAV ---
class UAV_approach(Task):

    def __init__(self, param, vs_req = True, gs_req = False):
        super().__init__(param, vs_req, False)
        self.maneuver_started = False

    def next_event(self, states, last_event, event_param):
        '''
            Approach sequence: on_vs -> uav_st_app -> (uav_rsm_app, uav_end_app) -> uav_off_vs
        '''
        if last_event == 'uav_st_app':
            self.maneuver_started = True
        elif last_event == 'uav_end_app' and self.maneuver_started:
            self.maneuver_started = False
            return 'task_done'

        return ['uav_st_app', 'uav_rsm_app', 'uav_end_app'] + self.getSensors()         # events before maneuver is executed
        

    def get_priorities_table(self):
        '''
            Priority of events affected by this mode of operation
        '''    
        table = super().get_priorities_table()
        table['uav_sus_app'] = 3
        table['uav_abort_app'] = 3
        if 'uav_on_vs' in self.getSensors():
            table['uav_off_vs'] = 5
        return table


class UAV_assessment(Task):

    def __init__(self, param, vs_req = True, gs_req = True):
        super().__init__(param, vs_req, False)
        self.maneuver_started = False

    def next_event(self, states, last_event, event_param = []):
        '''
            Assessment sequence: > uav_st_assess -> (uav_rsm_assess, uav_end_assess) 
        '''        
        if last_event == 'uav_st_assess':
            self.maneuver_started = True
        elif last_event == 'uav_end_assess' and self.maneuver_started:
            self.maneuver_started = False
            return 'task_done'

        return ['uav_st_assess', 'uav_rsm_assess', 'uav_end_assess'] + self.getSensors()         # events before maneuver is executed
        

    def get_priorities_table(self):
        '''
            Priority of events affected by this mode of operation
        '''    
        table = super().get_priorities_table()
        table['uav_sus_assess'] = 3
        table['uav_abort_assess'] = 3
        if 'uav_on_vs' in self.getSensors():
            table['uav_off_vs'] = 5
        return table


class UAV_v_search(Task):

    def __init__(self, param, vs_req = True, gs_req = True):
        super().__init__(param, True, False)
        self.maneuver_started = False

    def next_event(self, states, last_event, event_param = []):
        '''
            Victim Search sequence: on_vs --> uav_st_v_search -> (uav_rsm_v_search, uav_end_v_search) -> off_vs
        '''        
        if last_event == 'uav_st_v_search':
            self.maneuver_started = True
        elif last_event == 'uav_end_v_search' and self.maneuver_started:
            self.maneuver_started = False
            return 'task_done'

        return ['uav_st_v_search', 'uav_rsm_v_search', 'uav_end_v_search'] + self.getSensors()         # events before maneuver is executed
        

    def get_priorities_table(self):
        '''
            Priority of events affected by this mode of operation
        '''    
        table = super().get_priorities_table()
        table['uav_sus_v_search'] = 3
        table['uav_abort_v_search'] = 3
        if 'uav_on_vs' in self.getSensors():
            table['uav_off_vs'] = 5
        return table


class UAV_verification(Task):

    def __init__(self, param, vs_req = True, gs_req = True):
        super().__init__(param, True, False)
        self.maneuver_started = False

    def next_event(self, states, last_event, event_param = []):
        '''
            VSV sequence: on_vs -> uav_st_vsv -> (uav_rsm_vsv, uav_end_vsv)  -> off_vs
        '''
        if last_event == 'uav_st_vsv':
            self.maneuver_started = True
        elif last_event == 'uav_end_vsv' and self.maneuver_started:
            self.maneuver_started = False
            return 'task_done'

        return ['uav_st_vsv', 'uav_rsm_vsv', 'uav_end_vsv'] + self.getSensors()         # events before maneuver is executed
        

    def get_priorities_table(self):
        '''
            Priority of events affected by this mode of operation
        '''    
        table = super().get_priorities_table()
        table['uav_sus_vsv'] = 3
        table['uav_abort_vsv'] = 3
        if 'uav_on_vs' in self.getSensors():
            table['uav_off_vs'] = 5
        return table


class UAV_return(Task):

    def __init__(self, param, vs_req = False, gs_req = False):
        super().__init__(param, vs_req, False)
        self.maneuver_started = False

    def next_event(self, states, last_event, event_param = []):
        '''
            Return to Base sequence:  st_rb -> (rsm_rb, end_rb)
        '''
        if last_event == 'uav_st_rb':
            self.maneuver_started = True
        elif last_event == 'uav_end_rb' and self.maneuver_started:
            self.maneuver_started = False
            return 'task_done'

        return ['uav_st_rb', 'uav_rsm_rb', 'uav_end_rb'] + self.getSensors()         # events before maneuver is executed
        

    def get_priorities_table(self):
        '''
            Priority of events affected by this mode of operation
        '''    
        table = super().get_priorities_table()
        table['uav_sus_rb'] = 3
        table['uav_abort_rb'] = 3
        if 'uav_on_vs' in self.getSensors():
            table['uav_off_vs'] = 5
        return table


##########################################################################################################
# --- BACKUP BEHAVIORS ---

class CriticSystem(Task):
    '''
        Behavior if the robot has a CRITICAL FAILURE or if the battery level become CRITIC

        - the robot must attempt a safe land and turn off all sensors
    '''
    def __init__(self):
        super().__init__()
        self._safe_land_executed = False
        self.victims_pose = None

    '''
        Function to get baseline events --> stop current maneuver, execute safe land and turn sensors off
    '''
    def next_event(self, states, last_event, event_param = []):
        if last_event == 'uav_end_safe_land':
            self._safe_land_executed = True
        
        if not self._safe_land_executed:
            return ['uav_on_vs', 'uav_rst_safe_land', 'uav_st_safe_land']

        return []

    '''
        Priority of events affected by this mode of operation
    '''    
    def get_priorities_table(self):
        table = {
            #Controllable
                'uav_off_vs':5, 'uav_on_vs':0,
                'uav_rep_victim':11, 'uav_req_assist':11,
                'uav_st_app':0, 'uav_st_assess':0, 'uav_st_rb':0, 'uav_st_safe_land':0, 'uav_st_tele':0, 'uav_st_v_search':0, 'uav_st_vsv':0, 
                'uav_sus_app':9, 'uav_sus_assess':9, 'uav_sus_rb':9, 'uav_sus_v_search':9, 'uav_sus_vsv':9,
                'uav_rsm_app':0, 'uav_rsm_assess':0, 'uav_rsm_rb':0, 'uav_rsm_v_search':0, 'uav_rsm_vsv':0, 
                'uav_abort_app':9, 'uav_abort_assess':9, 'uav_abort_rb':4, 'uav_abort_v_search':9, 'uav_abort_tele':9, 'uav_abort_vsv':9, 
                'uav_rst_app':0, 'uav_rst_assess':0, 'uav_rst_rb':0, 'uav_rst_safe_land':0, 'uav_rst_tele':0, 'uav_rst_v_search':0, 'uav_rst_vsv':0, 

            #Uncontrollable
                'uav_bat_L':1, 'uav_bat_LL':1, 'uav_bat_OK':1,
                'uav_fail':1, 'uav_pos_fail':1, 'uav_critic_fail':1,
                'uav_victim_found':1, 'uav_call_tele':1,
                'uav_end_app':1, 'uav_end_assess':1, 'uav_end_rb':1, 'uav_end_safe_land':1, 'uav_end_tele':1, 'uav_end_v_search':1, 'uav_end_vsv':1,
                'uav_er_app':1, 'uav_er_assess':1, 'uav_er_rb':1, 'uav_er_safe_land':1, 'uav_er_tele':1, 'uav_er_v_search':1, 'uav_er_vsv':1, 
                'uav_er_vs':1,
                'uav_rst_f':1, 'uav_rst_vs':1
                }
        return table

    def getTaskParam(self):
        '''
            Return the parameter of the task
        '''
        return self.victims_pose

    def restart(self, victims):
        self.victims_pose = victims
        self._safe_land_executed = False


class HRI(Task):
    '''
        Behavior if the robot has a MANEUVER ERROR or if commander called teleoperation

        - In case of maneuver error, the robot wait require human assistance and wait for it;
        - In case of teleoperation requisition by the commander, the robots start tele mode.
    '''
    def __init__(self):
        super().__init__()
        self._tele_executed = False
    
    def next_event(self, states, last_event, event_param = []):

        if last_event == 'uav_st_tele':
            self._tele_executed = True

        if not self._tele_executed:
            for s in ['APP_EXE','ASSESS_EXE', 'V_SEARCH_EXE', 'VSV_EXE','RB_EXE']:
                if s in states:
                    return ['uav_sus_app', 'uav_sus_assess', 'uav_sus_v_search', 'uav_sus_vsv', 'uav_sus_rb']        # suspend current maneuver

            if 'TELE_EXE' not in states:
                return ['uav_rst_tele', 'uav_st_tele']        # try to start teleoperation

        else:
            if 'TELE_EXE' in states:
                return ['uav_end_tele', 'uav_er_tele']

            for s in ['APP_ERROR','ASSESS_ERROR', 'V_SEARCH_ERROR', 'VSV_ERROR','RB_ERROR']:
                if s in states: 
                    return  ['uav_rst_app', 'uav_rst_assess', 'uav_rst_v_search', 'uav_rst_vsv', 'uav_rst_rb']

        self._tele_executed = False
        return []

    '''
        Priority of events affected by this mode of operation
    '''    
    def get_priorities_table(self):
        table = {
            #Controllable
                'uav_off_vs':5, 'uav_on_vs':0,
                'uav_rep_victim':11, 'uav_req_assist':11,
                'uav_st_app':0, 'uav_st_assess':0, 'uav_st_rb':0, 'uav_st_safe_land':0, 'uav_st_tele':0, 'uav_st_v_search':0, 'uav_st_vsv':0, 
                'uav_sus_app':4, 'uav_sus_assess':4, 'uav_sus_rb':4, 'uav_sus_v_search':4, 'uav_sus_vsv':4,
                'uav_rsm_app':0, 'uav_rsm_assess':0, 'uav_rsm_rb':0, 'uav_rsm_v_search':0, 'uav_rsm_vsv':0, 
                'uav_abort_app':4, 'uav_abort_assess':4, 'uav_abort_rb':4, 'uav_abort_v_search':4, 'uav_abort_tele':0, 'uav_abort_vsv':4, 
                'uav_rst_app':0, 'uav_rst_assess':0, 'uav_rst_rb':0, 'uav_rst_safe_land':0, 'uav_rst_tele':0, 'uav_rst_v_search':0, 'uav_rst_vsv':0, 

            #Uncontrollable
                'uav_bat_L':1, 'uav_bat_LL':1, 'uav_bat_OK':1,
                'uav_fail':1, 'uav_pos_fail':1, 'uav_critic_fail':1,
                'uav_victim_found':1, 'uav_call_tele':1,
                'uav_end_app':1, 'uav_end_assess':1, 'uav_end_rb':1, 'uav_end_safe_land':1, 'uav_end_tele':1, 'uav_end_v_search':1, 'uav_end_vsv':1,
                'uav_er_app':1, 'uav_er_assess':1, 'uav_er_rb':1, 'uav_er_safe_land':1, 'uav_er_tele':1, 'uav_er_v_search':1, 'uav_er_vsv':1, 
                'uav_er_vs':1,
                'uav_rst_f':1, 'uav_rst_vs':1
                }
        return table

    def restart(self):
        super().restart()
        self._tele_executed = False


class DegradedMode2(Task):
    '''
        Behavior if the robot has a POSITION FAILURE or SENSOR ERROR with current task depending on it

        - the robot must abort all maneuvers (except teleoperation) and stop sensors.
    '''
    def __init__(self):
        super().__init__()

    '''
        Function to get baseline events --> stop current maneuver and turn sensors off
    '''
    def next_event(self, states, last_event, event_param = []):
        for s in ['APP_EXE', 'ASSESS_EXE', 'V_SEARCH_EXE', 'VSV_EXE', 'RB_EXE', 'APP_SUSP', 'ASSESS_SUSP', 'V_SEARCH_SUSP', 'VSV_SUSP', 'RB_SUSP', 'VS_ON']:
            if s in states:
                return ['uav_sus_app', 'uav_sus_assess', 'uav_sus_v_search', 'uav_sus_vsv', 'uav_sus_rb',                      # suspend current maneuver
                        'uav_abort_app', 'uav_abort_assess', 'uav_abort_v_search', 'uav_abort_vsv', 'uav_abort_rb',            # abort current maneuver
                        'uav_off_vs']                                                                                              # stop sensors
        return []

    '''
        Priority of events affected by this mode of operation
    '''    
    def get_priorities_table(self):
        table = {
            #Controllable
                'uav_off_vs':5, 'uav_on_vs':0,
                'uav_rep_victim':11, 'uav_req_assist':11,
                'uav_st_app':0, 'uav_st_assess':0, 'uav_st_rb':0, 'uav_st_safe_land':0, 'uav_st_tele':0, 'uav_st_v_search':0, 'uav_st_vsv':0, 
                'uav_sus_app':4, 'uav_sus_assess':4, 'uav_sus_rb':4, 'uav_sus_v_search':4, 'uav_sus_vsv':4,
                'uav_rsm_app':0, 'uav_rsm_assess':0, 'uav_rsm_rb':0, 'uav_rsm_v_search':0, 'uav_rsm_vsv':0, 
                'uav_abort_app':4, 'uav_abort_assess':4, 'uav_abort_rb':4, 'uav_abort_v_search':4, 'uav_abort_tele':4, 'uav_abort_vsv':4, 
                'uav_rst_app':5, 'uav_rst_assess':5, 'uav_rst_rb':5, 'uav_rst_safe_land':5, 'uav_rst_tele':5, 'uav_rst_v_search':5, 'uav_rst_vsv':5, 

            #Uncontrollable
                'uav_bat_L':1, 'uav_bat_LL':1, 'uav_bat_OK':1,
                'uav_fail':1, 'uav_pos_fail':1, 'uav_critic_fail':1,
                'uav_victim_found':1, 'uav_call_tele':1,
                'uav_end_app':1, 'uav_end_assess':1, 'uav_end_rb':1, 'uav_end_safe_land':1, 'uav_end_tele':1, 'uav_end_v_search':1, 'uav_end_vsv':1,
                'uav_er_app':1, 'uav_er_assess':1, 'uav_er_rb':1, 'uav_er_safe_land':1, 'uav_er_tele':1, 'uav_er_v_search':1, 'uav_er_vsv':1, 
                'uav_er_vs':1,
                'uav_rst_f':1, 'uav_rst_vs':1
                }
        return table


class DegradedMode1(Task):
    '''
        Behavior if the robot has a SIMPLE FAILURE or if the battery level become LOW

        - the robot must return to base.
    '''
    def __init__(self):
        super().__init__()
        self.atBase = False

    '''
        Function to get baseline events --> wait execution of current maneuver, turn sensors off and return to base
    '''
    def next_event(self, states, last_event, event_param = []):
        if last_event == 'uav_end_rb':
            self.atBase = True
        
        if not self.atBase:
            for s in ['APP_EXE', 'ASSESS_EXE', 'V_SEARCH_EXE', 'VSV_EXE', 'APP_SUSP', 'ASSESS_SUSP', 'V_SEARCH_SUSP', 'VSV_SUSP']:
                if s in states:
                    return ['uav_sus_app', 'uav_sus_assess', 'uav_sus_v_search', 'uav_sus_vsv',                      # suspend current maneuver
                            'uav_abort_app', 'uav_abort_assess', 'uav_abort_v_search', 'uav_abort_vsv']            # abort current maneuver      

            if 'VS_ON' in states:
                return ['uav_off_vs']

            for s in ['RB_IDLE', 'RB_SUSP']:
                if s in states:
                    return ['uav_st_rb','uav_rsm_rb']

            if 'RB_EXE' in states:
                return ['uav_end_rb']
    
    '''
        Priority of events affected by this mode of operation
    '''    
    def get_priorities_table(self):
        table = {
            #Controllable
                'uav_off_vs':5, 'uav_on_vs':0,
                'uav_rep_victim':11, 'uav_req_assist':11,
                'uav_st_app':0, 'uav_st_assess':0, 'uav_st_rb':0, 'uav_st_safe_land':0, 'uav_st_tele':0, 'uav_st_v_search':0, 'uav_st_vsv':0, 
                'uav_sus_app':4, 'uav_sus_assess':4, 'uav_sus_rb':4, 'uav_sus_v_search':4, 'uav_sus_vsv':4,
                'uav_rsm_app':0, 'uav_rsm_assess':0, 'uav_rsm_rb':0, 'uav_rsm_v_search':0, 'uav_rsm_vsv':0, 
                'uav_abort_app':4, 'uav_abort_assess':4, 'uav_abort_rb':4, 'uav_abort_v_search':4, 'uav_abort_tele':4, 'uav_abort_vsv':4, 
                'uav_rst_app':5, 'uav_rst_assess':5, 'uav_rst_rb':5, 'uav_rst_safe_land':5, 'uav_rst_tele':5, 'uav_rst_v_search':5, 'uav_rst_vsv':5, 

            #Uncontrollable
                'uav_bat_L':1, 'uav_bat_LL':1, 'uav_bat_OK':1,
                'uav_fail':1, 'uav_pos_fail':1, 'uav_critic_fail':1,
                'uav_victim_found':1, 'uav_call_tele':1,
                'uav_end_app':1, 'uav_end_assess':1, 'uav_end_rb':1, 'uav_end_safe_land':1, 'uav_end_tele':1, 'uav_end_v_search':1, 'uav_end_vsv':1,
                'uav_er_app':1, 'uav_er_assess':1, 'uav_er_rb':1, 'uav_er_safe_land':1, 'uav_er_tele':1, 'uav_er_v_search':1, 'uav_er_vsv':1, 
                'uav_er_vs':1,
                'uav_rst_f':1, 'uav_rst_vs':1
                }
        return table


    def restart(self):
        super().restart()
        self.atBase = False


class Victim(Task):
    '''
        Behavior if the robot has found a VICTIM

        - the robot must suspend current maneuver and execute VICTIM SURROUNDINGS VERIFICATION
    '''
    def __init__(self, param=[]):
        super().__init__(param = ['victim', param[0], param[1], param[2]])

    def next_event(self, states, last_event, event_param = []):
        pass

    '''
        Priority of events affected by this mode of operation
    '''    
    def get_priorities_table(self):
        table = {
            #Controllable
                'uav_off_vs':5, 'uav_on_vs':6,
                'uav_rep_victim':11, 'uav_req_assist':11,
                'uav_st_app':0, 'uav_st_assess':0, 'uav_st_rb':0, 'uav_st_safe_land':0, 'uav_st_tele':0, 'uav_st_v_search':0, 'uav_st_vsv':8, 
                'uav_sus_app':3, 'uav_sus_assess':3, 'uav_sus_rb':3, 'uav_sus_v_search':3, 'uav_sus_vsv':0,
                'uav_rsm_app':3, 'uav_rsm_assess':3, 'uav_rsm_rb':3, 'uav_rsm_v_search':3, 'uav_rsm_vsv':8, 
                'uav_abort_app':0, 'uav_abort_assess':0, 'uav_abort_rb':0, 'uav_abort_v_search':0, 'uav_abort_tele':0, 'uav_abort_vsv':0, 
                'uav_rst_app':3, 'uav_rst_assess':3, 'uav_rst_rb':3, 'uav_rst_safe_land':3, 'uav_rst_tele':3, 'uav_rst_v_search':3, 'uav_rst_vsv':3, 

            #Uncontrollable
                'uav_bat_L':1, 'uav_bat_LL':1, 'uav_bat_OK':1,
                'uav_fail':1, 'uav_pos_fail':1, 'uav_critic_fail':1,
                'uav_victim_found':1, 'uav_call_tele':1,
                'uav_end_app':1, 'uav_end_assess':1, 'uav_end_rb':1, 'uav_end_safe_land':1, 'uav_end_tele':1, 'uav_end_v_search':1, 'uav_end_vsv':1,
                'uav_er_app':1, 'uav_er_assess':1, 'uav_er_rb':1, 'uav_er_safe_land':1, 'uav_er_tele':1, 'uav_er_v_search':1, 'uav_er_vsv':1, 
                'uav_er_vs':1,
                'uav_rst_f':1, 'uav_rst_vs':1
                }
        return table