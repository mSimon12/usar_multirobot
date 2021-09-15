
from time import sleep

class Task(object):

    def __init__(self, param=[], vs_req = False, gs_req = False):
        self._param = param                                           # Atribute to save the parameter of the task
        self.__sensors = {'on_vs': vs_req, 'on_gs': gs_req}           # Save the required status of the sensors
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
                'off_gs':11, 'off_vs':11, #'on_gs':0, 'on_vs':0,
                'rep_gas':15, 'rep_victim':15, 'req_assist':15,
                # 'st_app':0, 'st_exp':0, 'st_rb':0, 'st_tele':0, 'st_vsv':0,
                'sus_app':11, 'sus_exp':11, 'sus_rb':11, 'sus_vsv':11,
                # 'rsm_app':0, 'rsm_exp':0, 'rsm_rb':0, 'rsm_vsv':0,
                'abort_app':11, 'abort_exp':11, 'abort_rb':11, 'abort_vsv':11,
                'rst_app':5, 'rst_exp':5, 'rst_rb':5, 'rst_tele':5, 'rst_vsv':5,
            #Uncontrollable
                # 'bat_L':1, 'bat_LL':1, 'bat_OK':1,
                # 'fail':1, 'pos_fail':1, 'critic_fail':1,
                # 'gas_found':1, 'victim_found':1, 'call_tele':1,
                # 'end_app':1, 'end_exp':1, 'end_rb':1, 'end_tele':1, 'end_vsv':1,
                # 'er_app':1, 'er_exp':1, 'er_rb':1, 'er_tele':1, 'er_vsv':1,
                # 'er_gs':1, 'er_vs':1,
                # 'rst_f':1, 'rst_gs':1, 'rst_vs':1
                }

        return table

    def restart(self):
        self._motion_done = False
        self._last_task_aborted = False


##########################################################################################################
# --- PIONEER3AT ---
class UGV_approach(Task):

    def __init__(self, param, vs_req = True, gs_req = False):
        super().__init__(param, True, gs_req)
        self.maneuver_started = False

    def next_event(self, states, last_event, event_param):
        '''
            Approach sequence: on_vs -> st_app -> (rsm_app, end_app) -> off_vs
        '''
        if last_event == 'st_app':
            self.maneuver_started = True
        elif last_event == 'end_app' and self.maneuver_started:
            self.maneuver_started = False
            return 'task_done'

        return ['st_app', 'rsm_app', 'end_app'] + self.getSensors()         # events before maneuver is executed
        

    def get_priorities_table(self):
        '''
            Priority of events affected by this mode of operation
        '''    
        table = super().get_priorities_table()
        if self.maneuver_started:
            table['sus_app'] = 3
            table['abort_app'] = 3
        if 'on_vs' in self.getSensors():
            table['off_vs'] = 5
        if 'on_gs' in self.getSensors():
            table['off_gs'] = 5
        return table

class UGV_exploration(Task):

    def __init__(self, param, vs_req = True, gs_req = True):
        super().__init__(param, True, True)
        self.maneuver_started = False

    def next_event(self, states, last_event, event_param = []):
        '''
            Exploration sequence: on_vs -> on_gs -> st_exp -> (rsm_exp, end_exp) -> off_gs -> off_vs
        '''        
        if last_event == 'st_exp':
            self.maneuver_started = True
        elif last_event == 'end_exp' and self.maneuver_started:
            self.maneuver_started = False
            return 'task_done'

        return ['st_exp', 'rsm_exp', 'end_exp'] + self.getSensors()       # events before maneuver is executed


    def get_priorities_table(self):
        '''
            Priority of events affected by this mode of operation
        '''    
        table = super().get_priorities_table()
        if self.maneuver_started:
            table['sus_exp'] = 3
            table['abort_exp'] = 3
        if 'on_vs' in self.getSensors():
            table['off_vs'] = 5
        if 'on_gs' in self.getSensors():
            table['off_gs'] = 5
        return table


class UGV_verification(Task):

    def __init__(self, param, vs_req = True, gs_req = True):
        super().__init__(param, True, True)

    def next_event(self, states, last_event, event_param = []):
        '''
            VSV sequence: on_vs -> on_gs -> st_vsv -> (rsm_vsv, end_vsv) -> off_gs -> off_vs
        '''
        if last_event == 'st_vsv':
            self.maneuver_started = True
        elif last_event == 'end_vsv' and self.maneuver_started:
            self.maneuver_started = False
            return 'task_done'

        return ['st_vsv', 'rsm_vsv', 'end_vsv'] + self.getSensors()         # events before maneuver is executed
        

    def get_priorities_table(self):
        '''
            Priority of events affected by this mode of operation
        '''    
        table = super().get_priorities_table()
        if self.maneuver_started:
            table['sus_vsv'] = 3
            table['abort_vsv'] = 3
        if 'on_vs' in self.getSensors():
            table['off_vs'] = 5
        if 'on_gs' in self.getSensors():
            table['off_gs'] = 5
        return table


class UGV_return(Task):

    def __init__(self, param, vs_req = False, gs_req = False):
        super().__init__(param, vs_req, gs_req)
        self.maneuver_started = False

    def next_event(self, states, last_event, event_param = []):
        '''
            Return to Base sequence:  st_rb -> (rsm_rb, end_rb)
        '''
        if last_event == 'st_rb':
            self.maneuver_started = True
        elif last_event == 'end_rb' and self.maneuver_started:
            self.maneuver_started = False
            return 'task_done'

        return ['st_rb', 'rsm_rb', 'end_rb'] + self.getSensors()         # events before maneuver is executed
        

    def get_priorities_table(self):
        '''
            Priority of events affected by this mode of operation
        '''    
        table = super().get_priorities_table()
        if self.maneuver_started:
            table['sus_rb'] = 3
            table['abort_rb'] = 3
        if 'on_vs' in self.getSensors():
            table['off_vs'] = 5
        if 'on_gs' in self.getSensors():
            table['off_gs'] = 5
        return table


##########################################################################################################
# --- BACKUP BEHAVIORS ---

class CriticSystem(Task):
    '''
        Behavior if the robot has a CRITICAL FAILURE or if the battery level become CRITIC

        - the robot must abort all maneuvers and stop sensors.
    '''
    def __init__(self):
        super().__init__()

    '''
        Function to get baseline events --> stop current maneuver and turn sensors off
    '''
    def next_event(self, states, last_event, event_param = []):
        for s in ['APP_EXE','EXP_EXE','VSV_EXE','TELE_EXE','RB_EXE', 'APP_SUSP','EXP_SUSP','VSV_SUSP','RB_SUSP', 'VS_ON', 'GS_ON']:
            if s in states:
                return ['sus_app', 'sus_exp', 'sus_vsv', 'sus_rb', 'abort_tele',        # suspend current maneuver
                        'abort_app', 'abort_exp', 'abort_vsv', 'abort_rb',              # abort current maneuver
                        'off_vs','off_gs']                                              # stop sensors
        return []

    '''
        Priority of events affected by this mode of operation
    '''    
    def get_priorities_table(self):
        table = {
            #Controllable
                'off_gs':5, 'off_vs':5, 'on_gs':0, 'on_vs':0,
                'rep_gas':11, 'rep_victim':11, 'req_assist':11,
                'st_app':0, 'st_exp':0, 'st_rb':0, 'st_tele':0, 'st_vsv':0,
                'sus_app':4, 'sus_exp':4, 'sus_rb':4, 'sus_vsv':4,
                'rsm_app':0, 'rsm_exp':0, 'rsm_rb':0, 'rsm_vsv':0,
                'abort_app':4, 'abort_exp':4, 'abort_rb':4, 'abort_tele':4, 'abort_vsv':4,
                'rst_app':0, 'rst_exp':0, 'rst_rb':0, 'rst_tele':0, 'rst_vsv':0,
            #Uncontrollable
                'bat_L':1, 'bat_LL':1, 'bat_OK':1,
                'fail':1, 'pos_fail':1, 'critic_fail':1,
                'gas_found':1, 'victim_found':1, 'call_tele':1,
                'end_app':1, 'end_exp':1, 'end_rb':1, 'end_tele':1, 'end_vsv':1,
                'er_app':1, 'er_exp':1, 'er_rb':1, 'er_tele':1, 'er_vsv':1,
                'er_gs':1, 'er_vs':1,
                'rst_f':1, 'rst_gs':1, 'rst_vs':1}

        return table


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

        if last_event == 'st_tele':
            self._tele_executed = True

        if not self._tele_executed:
            for s in ['APP_EXE','EXP_EXE','VSV_EXE','RB_EXE']:
                if s in states:
                    return ['sus_app', 'sus_exp', 'sus_vsv', 'sus_rb']        # suspend current maneuver

            if 'TELE_EXE' not in states:
                return ['rst_tele', 'st_tele']        # try to start teleoperation

        else:
            if 'TELE_EXE' in states:
                return ['end_tele', 'er_tele']

            for s in ['APP_ERROR','EXP_ERROR','VSV_ERROR','TELE_ERROR','RB_ERROR']:
                if s in states: 
                    return  ['rst_app', 'rst_exp', 'rst_vsv', 'rst_rb']

        self._tele_executed = False
        return []

    '''
        Priority of events affected by this mode of operation
    '''    
    def get_priorities_table(self):
        table = {
            #Controllable
                'off_gs':5, 'off_vs':5, 'on_gs':0, 'on_vs':0,
                'rep_gas':11, 'rep_victim':11, 'req_assist':11,
                'st_app':0, 'st_exp':0, 'st_rb':0, 'st_tele':9, 'st_vsv':0,
                'sus_app':4, 'sus_exp':4, 'sus_rb':4, 'sus_vsv':4,
                'rsm_app':0, 'rsm_exp':0, 'rsm_rb':0, 'rsm_vsv':0,
                'abort_app':4, 'abort_exp':4, 'abort_rb':4, 'abort_tele':4, 'abort_vsv':4,
                'rst_app':0, 'rst_exp':0, 'rst_rb':0, 'rst_tele':0, 'rst_vsv':0,
            #Uncontrollable
                'bat_L':1, 'bat_LL':1, 'bat_OK':1,
                'fail':1, 'pos_fail':1, 'critic_fail':1,
                'gas_found':1, 'victim_found':1, 'call_tele':1,
                'end_app':1, 'end_exp':1, 'end_rb':1, 'end_tele':1, 'end_vsv':1,
                'er_app':1, 'er_exp':1, 'er_rb':1, 'er_tele':1, 'er_vsv':1,
                'er_gs':1, 'er_vs':1,
                'rst_f':1, 'rst_gs':1, 'rst_vs':1}

        return table

    def restart(self):
        super().restart()
        self._tele_executed = False


class DegradedMode2(Task):
    '''
        Behavior if the robot has a POSITION FAILURE or SENSOR ERROR with current task depending on it

        - the robot must return to base after finishing the last task.
    '''
    def __init__(self):
        super().__init__()

    '''
        Function to get baseline events --> stop current maneuver and turn sensors off
    '''
    def next_event(self, states, last_event, event_param = []):
        for s in ['APP_EXE','EXP_EXE','VSV_EXE','RB_EXE', 'APP_SUSP','EXP_SUSP','VSV_SUSP','RB_SUSP', 'GS_ON', 'VS_ON']:
            if s in states:
                return ['sus_app', 'sus_exp', 'sus_vsv', 'sus_rb',                      # suspend current maneuver
                        'abort_app', 'abort_exp', 'abort_vsv', 'abort_rb',              # abort current maneuver
                        'off_vs','off_gs']                                              # stop sensors
        return []

    '''
        Priority of events affected by this mode of operation
    '''    
    def get_priorities_table(self):
        table = {
            #Controllable
                'off_gs':5, 'off_vs':5, 'on_gs':0, 'on_vs':0,
                'rep_gas':11, 'rep_victim':11, 'req_assist':11,
                'st_app':0, 'st_exp':0, 'st_rb':0, 'st_tele':0, 'st_vsv':0,
                'sus_app':4, 'sus_exp':4, 'sus_rb':4, 'sus_vsv':4,
                'rsm_app':0, 'rsm_exp':0, 'rsm_rb':0, 'rsm_vsv':0,
                'abort_app':4, 'abort_exp':4, 'abort_rb':4, 'abort_tele':4, 'abort_vsv':4,
                'rst_app':5, 'rst_exp':5, 'rst_rb':5, 'rst_tele':5, 'rst_vsv':5,
            #Uncontrollable
                'bat_L':1, 'bat_LL':1, 'bat_OK':1,
                'fail':1, 'pos_fail':1, 'critic_fail':1,
                'gas_found':1, 'victim_found':1, 'call_tele':1,
                'end_app':1, 'end_exp':1, 'end_rb':1, 'end_tele':1, 'end_vsv':1,
                'er_app':1, 'er_exp':1, 'er_rb':1, 'er_tele':1, 'er_vsv':1,
                'er_gs':1, 'er_vs':1,
                'rst_f':1, 'rst_gs':1, 'rst_vs':1}

        return table


class Victim(Task):
    '''
        Behavior if the robot has found a VICTIM

        - the robot must suspend current maneuver and execute VICTIM SURROUNDINGS VERIFICATION
    '''
    def __init__(self, param=[]):
        super().__init__(param = ['victim', param[0], param[1]])

    def next_event(self, states, last_event, event_param = []):
        pass

    '''
        Priority of events affected by this mode of operation
    '''    
    def get_priorities_table(self):
        table = {
            #Controllable
                'abort_app':0, 'abort_exp':0, 'abort_rb':0, 'abort_tele':0, 'abort_vsv':0,
                'off_gs':5, 'off_vs':5, 'on_gs':6, 'on_vs':6,
                'rep_gas':11, 'rep_victim':11, 'req_assist':11,
                'rsm_app':3, 'rsm_exp':3, 'rsm_rb':3, 'rsm_vsv':8,
                'rst_app':3, 'rst_exp':3, 'rst_rb':3, 'rst_tele':3, 'rst_vsv':3,
                'st_app':3, 'st_exp':3, 'st_rb':3, 'st_tele':3, 'st_vsv':8,
                'sus_app':6, 'sus_exp':6, 'sus_rb':6, 'sus_vsv':0,
            #Uontrollable
                'bat_L':1, 'bat_LL':1, 'bat_OK':1,
                'fail':1, 'pos_fail':1, 'critic_fail':1,
                'gas_found':1, 'victim_found':1, 'call_tele':1,
                'end_app':1, 'end_exp':1, 'end_rb':1, 'end_tele':1, 'end_vsv':1,
                'er_app':1, 'er_exp':1, 'er_rb':1, 'er_tele':1, 'er_vsv':1,
                'er_gs':1, 'er_vs':1,
                'rst_f':1, 'rst_gs':1, 'rst_vs':1}

        return table


class DegradedMode1(Task):
    '''
        Behavior if the robot has a SIMPLE FAILURE or if the battery level become LOW

        - the robot must abort all maneuvers (except teleoperation) and stop sensors.
    '''
    def __init__(self):
        super().__init__()
        self.atBase = False

    '''
        Function to get baseline events --> wait execution of current maneuver, turn sensors off and return to base
    '''
    def next_event(self, states, last_event, event_param = []):
        if last_event == 'end_rb':
            self.atBase = True
        
        if not self.atBase:
            for s in ['APP_EXE','EXP_EXE','VSV_EXE']:
                if s in states:
                    return ['end_app', 'end_exp', 'end_vsv', 'end_rb']

            for s in ['VS_ON', 'GS_ON']:
                if s in states:
                    return ['off_vs','off_gs']

            for s in ['RB_IDLE', 'RB_SUSP']:
                if s in states:
                    return ['st_rb','rsm_rb']

            if 'RB_EXE' in states:
                return ['end_rb']
    
    '''
        Priority of events affected by this mode of operation
    '''    
    def get_priorities_table(self):
        table = {
            #Controllable
                'off_gs':5, 'off_vs':5, 'on_gs':0, 'on_vs':0,
                'rep_gas':11, 'rep_victim':11, 'req_assist':11,
                'st_app':0, 'st_exp':0, 'st_rb':0, 'st_tele':0, 'st_vsv':0,
                'sus_app':4, 'sus_exp':4, 'sus_rb':4, 'sus_vsv':4,
                'rsm_app':0, 'rsm_exp':0, 'rsm_rb':0, 'rsm_vsv':0,
                'abort_app':4, 'abort_exp':4, 'abort_rb':4, 'abort_tele':4, 'abort_vsv':4,
                'rst_app':5, 'rst_exp':5, 'rst_rb':5, 'rst_tele':5, 'rst_vsv':5,
            #Uncontrollable
                'bat_L':1, 'bat_LL':1, 'bat_OK':1,
                'fail':1, 'pos_fail':1, 'critic_fail':1,
                'gas_found':1, 'victim_found':1, 'call_tele':1,
                'end_app':1, 'end_exp':1, 'end_rb':1, 'end_tele':1, 'end_vsv':1,
                'er_app':1, 'er_exp':1, 'er_rb':1, 'er_tele':1, 'er_vsv':1,
                'er_gs':1, 'er_vs':1,
                'rst_f':1, 'rst_gs':1, 'rst_vs':1}

        return table

    def restart(self):
        super().restart()
        self.atBase = False
