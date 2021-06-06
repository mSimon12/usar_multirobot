from time import sleep

class Task(object):

    def __init__(self, param=[], vs_req = False, gs_req = False):
        self._param = param                                           # Atribute to save the parameter of the task
        self.__sensors = {'vs': vs_req, 'gs': gs_req}                 # Save the required status of the sensors
        self._motion_done = False                                     # Monitor the motion execution
        self._last_task_aborted = False                               # Variable to abort last maneuver

    def getTaskParam(self):
        '''
            Return the parameter of the task
        '''
        return self._param
    
    def getSensors(self):
        return [sensor for sensor in self.__sensors if self.__sensors[sensor] == True]

    def _sensors2turnOFF(self,states):
        '''
            Return list of commands to turn sensors OFF
        '''
        if ('VS_ON' in states) and ('GS_ON' in states):
            return ['uav_off_vs','uav_off_gs']
        elif ('VS_ON' in states):
            return ['uav_off_vs']
        elif ('GS_ON' in states):
            return ['uav_off_gs']
        else:
            return False
    
    def _sensors2turnON(self,states):
        '''
            Return list of commands to turn sensors ON
        '''
        if all(['VS_OFF' in states, 'GS_OFF' in states, self.__sensors['vs']==True, self.__sensors['gs']==True]):
            return ['uav_on_vs','uav_on_gs']
        elif ('VS_OFF' in states) and (self.__sensors['vs']==True):
            return ['uav_on_vs']
        elif ('GS_OFF' in states) and (self.__sensors['gs']==True):
            return ['uav_on_gs']
        else:
            return False

    def _abort_last_M(self, states):
        if not self._last_task_aborted:
                # Abort the execution of the last task
                for i in ['APP_EXE','SEARCH_EXE','ASSESS_EXE','VSV_EXE','RB_EXE']:
                    if i in states:
                        return ['uav_sus_app','uav_sus_v_search', 'uav_sus_assess', 'uav_sus_vsv', 'uav_sus_rb']
                for i in ['APP_SUSP','SEARCH_SUSP', 'ASSESS_SUSP','VSV_SUSP','RB_SUSP']:
                    if i in states:
                        return ['uav_abort_app','uav_abort_v_search','uav_abort_assess', 'uav_abort_vsv', 'uav_abort_rb']
            
        self._last_task_aborted = True
        return []

    def next_event(self, states, last_event, event_param):
        pass

    def restart(self):
        self._motion_done = False
        self._last_task_aborted = False


##########################################################################################################
# --- UAV ---
class UAV_approach(Task):

    def __init__(self, param, vs_req = True, gs_req = False):
        super().__init__(param, vs_req, False)
        self.last_task_aborted = False

    def next_event(self, states, last_event, event_param):
        '''
            Approach sequence: on_vs -> uav_st_app -> (uav_rsm_app, uav_end_app) -> uav_off_vs
        '''
        if (not self._motion_done) and (last_event == 'uav_end_app') and (event_param == self._param):
            self._motion_done = True
        elif (not self._motion_done):
            # Before the motion have been considered as executed
            
            # Verify if the last maneuver must be aborted 
            event_to_abort = self._abort_last_M(states)
            if event_to_abort:
                return event_to_abort

            # Verify if required sensors are ON
            events = self._sensors2turnON(states)
            if events:
                return events
            else:
                # Start motion after the required sensors have been activated
                if 'APP_IDLE' in states:
                    return ['uav_st_app']
                else:
                    return ['uav_rsm_app', 'uav_end_app']

        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'

class UAV_assessment(Task):

    def __init__(self, param, vs_req = True, gs_req = True):
        super().__init__(param, vs_req, False)

    def next_event(self, states, last_event, event_param = []):
        '''
            Assessment sequence: > uav_st_assess -> (uav_rsm_assess, uav_end_assess) 
        '''        
        if (not self._motion_done) and (last_event == 'uav_end_assess') and (event_param == self._param):
            self._motion_done = True
        elif (not self._motion_done):
            # Before the motion have been considered as executed

            # Verify if the last maneuver must be aborted 
            event_to_abort = self._abort_last_M(states)
            if event_to_abort:
                return event_to_abort

            # Verify if required sensors are ON
            events = self._sensors2turnON(states)
            if events:
                return events
            else:
                # Start motion after the required sensors have been activated
                if 'ASSESS_IDLE' in states:
                    return ['uav_st_assess']
                else:
                    return ['uav_rsm_assess', 'uav_end_assess']

        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'

class UAV_v_search(Task):

    def __init__(self, param, vs_req = True, gs_req = True):
        super().__init__(param, True, False)

    def next_event(self, states, last_event, event_param = []):
        '''
            Victim Search sequence: on_vs --> uav_st_v_search -> (uav_rsm_v_search, uav_end_v_search) -> off_vs
        '''        
        if (not self._motion_done) and (last_event == 'uav_end_v_search') and (event_param == self._param):
            self._motion_done = True
        elif (not self._motion_done):
            # Before the motion have been considered as executed

            # Verify if the last maneuver must be aborted 
            event_to_abort = self._abort_last_M(states)
            if event_to_abort:
                return event_to_abort

            # Verify if required sensors are ON
            events = self._sensors2turnON(states)
            if events:
                return events
            else:
                # Start motion after the required sensors have been activated
                if 'SEARCH_IDLE' in states:
                    return ['uav_st_v_search']
                else:
                    return ['uav_rsm_v_search', 'uav_end_v_search']

        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'

class UAV_verification(Task):

    def __init__(self, param, vs_req = True, gs_req = True):
        super().__init__(param, True, False)

    def next_event(self, states, last_event, event_param = []):
        '''
            VSV sequence: on_vs -> uav_st_vsv -> (uav_rsm_vsv, uav_end_vsv)  -> off_vs
        '''
        if (not self._motion_done) and (last_event == 'uav_end_vsv') and (event_param == self._param):
            self._motion_done = True
        elif (not self._motion_done):
            # Before the motion have been considered as executed

            # Verify if the last maneuver must be aborted 
            event_to_abort = self._abort_last_M(states)
            if event_to_abort:
                return event_to_abort

            # Verify if required sensors are ON
            events = self._sensors2turnON(states)
            if events:
                return events
            else:
                # Start motion after the required sensors have been activated
                if 'VSV_IDLE' in states:
                    return ['uav_st_vsv']
                else:
                    return ['uav_rsm_vsv', 'uav_end_vsv']

        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'

class UAV_return(Task):

    def __init__(self, param, vs_req = False, gs_req = False):
        super().__init__(param, vs_req, False)

    def next_event(self, states, last_event, event_param = []):
        '''
            Return to Base sequence:  st_rb -> (rsm_rb, end_rb)
        '''
        if (not self._motion_done) and (last_event == 'uav_end_rb'):
            self._motion_done = True
        elif (not self._motion_done):
            # Before the motion have been considered as executed

            # Verify if the last maneuver must be aborted 
            event_to_abort = self._abort_last_M(states)
            if event_to_abort:
                return event_to_abort

            # Verify if required sensors are ON
            events = self._sensors2turnON(states)
            if events:
                return events
            else:
                # Start motion after the required sensors have been activated
                if 'RB_IDLE' in states:
                    return ['uav_st_rb']
                else:
                    return ['uav_rsm_rb', 'uav_end_rb']

        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'


##########################################################################################################
# --- BACKUP BEHAVIORS ---

class SafeLand(Task):

    def __init__(self, param = [], vs_req = False, gs_req = False):
        super().__init__(param, True, False)
        self.pose_reported = False

    def next_event(self, states, last_event, event_param = []):
        '''
            Safe Land sequence:  st_safe_land -> (rsm_safe_land, end_safe_land)
        '''
        if (last_event == 'uav_end_safe_land'):
            self._motion_done = True
        elif (last_event == 'uav_er_safe_land'):
            return["uav_rst_safe_land"]
        elif (not self._motion_done):
            # Before the motion have been considered as executed

            # Verify if the last maneuver must be aborted 
            event_to_abort = self._abort_last_M(states)
            if event_to_abort:
                return event_to_abort

            # Verify if required sensors are ON
            events = self._sensors2turnON(states)
            if events:
                return events
            else:
                # Start motion after the required sensors have been activated
                if 'LAND_IDLE' in states:
                    return ['uav_st_safe_land']
                else:
                    return ['uav_end_safe_land']

        if last_event == 'uav_rep_self_pos':
            self.pose_reported = True
        # elif not (('BAT_CRITICAL' in states) or ('CRITIC_FAILURE' in states)):
        #     self.pose_reported = False

        if self._motion_done:
            # After the motion have been executed
            if self.pose_reported:
                return []
            else:
                # After the maneuver have been aborted
                events = self._sensors2turnOFF(states)
                if events:
                    return events
                else:
                    return ['uav_rep_self_pos']

    def restart(self):
        super().restart()
        self.pose_reported = False


class GoBackToBase(Task):
    '''
        Behavior if the robot has a SIMPLE_FAILURE or if the battery level
        become LOW
    '''
    def __init__(self, param=[], vs_req = False, gs_req = False):
        super().__init__(param, False, False)
        self.atBase = False

    def next_event(self, states, last_event, event_param = []):
        if last_event == 'uav_end_rb':
            self.atBase = True
            return []
        elif last_event == 'uav_st_rb':
            return ['uav_end_rb']
        elif not self.atBase:
            # Verify if the last maneuver must be aborted 
            event_to_abort = self._abort_last_M(states)
            if event_to_abort:
                return event_to_abort

            # for i in ['APP_EXE','ASSESS_EXE','VSV_EXE','TELE_EXE','RB_EXE']:
            #     if i in states:
            #         return ['uav_end_app', 'uav_end_assess', 'uav_end_vsv', 'uav_end_tele', 'uav_end_rb']
            # After the maneuver have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return ['uav_st_rb']

    def restart(self):
        super().restart()
        self.atBase = False


class AbortM(Task):
    '''
        Abort maneuver if occurs a critic failure or if the robot
    '''
    def __init__(self, param=[], vs_req = False, gs_req = False):
        super().__init__(param, False, False)
        self.pose_reported = False

    def next_event(self, states, last_event, event_param = []):
        # abort any maneuver
        event_to_abort = self._abort_last_M(states)
        if event_to_abort:
            return event_to_abort

        # for i in ['APP_EXE','ASSESS_EXE','VSV_EXE','SEARCH_EXE','RB_EXE']:
        #     if i in states:
        #         return ['uav_sus_app', 'uav_sus_assess', 'uav_sus_vsv', 'uav_sus_rb', 'uav_sus_v_search']
        # for i in ['APP_SUSP','ASSESS_SUSP','VSV_SUSP','SEARCH_SUSP','RB_SUSP']:
        #     if i in states:
        #         return ['uav_abort_app', 'uav_abort_assess', 'uav_abort_vsv', 'uav_abort_rb','uav_abort_v_search']
        
        if last_event == 'uav_rep_self_pos':
            self.pose_reported = True

        if self.pose_reported:
            return []
        else:
            # After the maneuver have been aborted
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return ['uav_rep_self_pos']

    def restart(self):
        super().restart()
        self.pose_reported = False


class V_Found(Task):
    '''
        Report victim location and execute VSV if a victim is found
    '''
    def __init__(self, param=[], vs_req = False, gs_req = False):
        super().__init__(param, True, False)
        self.v_reported = False
        self._param = ['victim', param[0], param[1], param[2]]

    def next_event(self, states, last_event, event_param = []):
        # abort any maneuver
        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return []
        else:
            # Before the motion have been considered as executed
            if last_event == 'uav_end_vsv':
                self._motion_done = True
            elif last_event == 'uav_rep_victim':
                self.v_reported = True
                
            # Suspend current task
            for i in ['APP_EXE','ASSESS_EXE','RB_EXE', 'SEARCH_EXE']:
                if i in states:
                    return ['uav_sus_app', 'uav_sus_assess', 'uav_sus_rb', 'uav_sus_v_search']
            
            # Verify if the victim position was informed to the Commander
            if self.v_reported:
                # Verify if required sensors are ON
                events = self._sensors2turnON(states)
                if events:
                    return events
                else:
                    return ['uav_st_vsv']
            else:
                return ['uav_rep_victim']

    def restart(self):
        super().restart()
        self.v_reported = False   


class ReqHelp(Task):
    '''
        Require a human to help on the motion
    '''
    def __init__(self, param=[], vs_req = False, gs_req = False):
        super().__init__(param, False, False)
        self._assit_required = False
        self._tele_executed = False
        self._tele_required = False
    
    def next_event(self, states, last_event, event_param = []):
        event_to_abort = self._abort_last_M(states)
        if event_to_abort:
            return event_to_abort

        if last_event == 'uav_req_assist':
            self._assit_required = True
        elif last_event == 'uav_call_tele':
            self._tele_required = True
        elif last_event == 'uav_end_tele':
            self._tele_executed = True
        elif last_event in ['uav_rst_app', 'uav_rst_assess', 'uav_rst_vsv', 'uav_rst_rb', 'uav_rst_v_search','uav_er_tele']:
            return []
        
        if not self._assit_required:
            return ['uav_req_assist']
        else:  
            if self._tele_required:
                if self._tele_executed:
                    return ['uav_rst_app', 'uav_rst_assess', 'uav_rst_vsv', 'uav_rst_rb', 'uav_rst_v_search']
                elif 'TELE_IDLE' in states:
                    sleep(0.5)
                    return ['uav_st_tele']
                else:
                    return ['uav_end_tele','uav_er_tele']
            else:
                return ['uav_call_tele']

    def restart(self):
        super().restart()
        self._assit_required = False
        self._tele_executed = False
        self._tele_required = False


class TeleCalled(Task):
    '''
        Behavior if the Commander require teleoperation
    '''
    def __init__(self, param=[], vs_req = False, gs_req = False):
        super().__init__(param, False, False)

    def next_event(self, states, last_event, event_param = []):
        if last_event in ['uav_end_tele','uav_er_tele']:
            return []
        else:
            for i in ['APP_EXE','ASSESS_EXE','VSV_EXE','RB_EXE', 'V_SEARCH_EXE']:
                if i in states:
                    return ['uav_sus_app', 'uav_sus_assess', 'uav_sus_vsv', 'uav_sus_rb']
            for i in ['APP_ERROR','ASSESS_ERROR','VSV_ERROR','RB_ERROR', 'V_SEARCH_ERROR', 'SAFE_LAND_ERROR']:
                if i in states:
                    return ['uav_rst_app', 'uav_rst_assess', 'uav_rst_vsv', 'uav_rst_rb', 'uav_rst_v_search', 'uav_rst_safe_land']

            # After the maneuver have been executed
            if 'TELE_IDLE' in states:
                sleep(0.5)
                return ['uav_st_tele']
            elif 'TELE_ERROR' in states:
                return ['uav_rst_tele']
            else:
                return ['uav_end_tele']


class PosErro(Task):
    '''
        Abort maneuver if occurs a position failure and require human assistance withou automatically starting teleoperation
    '''
    def __init__(self, param=[], vs_req = False, gs_req = False):
        super().__init__(param, False, False)
        self.pose_reported = False
        self._assit_required = False

    def next_event(self, states, last_event, event_param = []):
        # Verify if the last maneuver must be aborted 
        event_to_abort = self._abort_last_M(states)
        if event_to_abort:
            return event_to_abort

        if last_event == 'uav_rep_self_pos':
            self.pose_reported = True
        elif last_event == 'uav_req_assist':
            self._assit_required = True

        if self.pose_reported:
            if not self._assit_required :
                return ['uav_req_assist']
            else:
                events = self._sensors2turnOFF(states)
                if events:
                    return events
                else:
                    return []
        else:
            return ['uav_rep_self_pos']

    def restart(self):
        super().restart()
        self.pose_reported = False
        self._assit_required = False