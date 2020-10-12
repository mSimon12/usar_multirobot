
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

    def _sensors2turnOFF(self,states):
        '''
            Return list of commands to turn sensors OFF
        '''
        if ('VS_ON' in states) and ('GS_ON' in states):
            return ['off_vs','off_gs']
        elif ('VS_ON' in states):
            return ['off_vs']
        elif ('GS_ON' in states):
            return ['off_gs']
        else:
            return False
    
    def _sensors2turnON(self,states):
        '''
            Return list of commands to turn sensors ON
        '''
        if all(['VS_OFF' in states, 'GS_OFF' in states, self.__sensors['vs']==True, self.__sensors['gs']==True]):
            return ['on_vs','on_gs']
        elif ('VS_OFF' in states) and (self.__sensors['vs']==True):
            return ['on_vs']
        elif ('GS_OFF' in states) and (self.__sensors['gs']==True):
            return ['on_gs']
        else:
            return False

    def _abort_last_M(self, states):
        if not self._last_task_aborted:
                # Abort the execution of the last task
                for i in ['APP_EXE','EXP_EXE','VSV_EXE','RB_EXE']:
                    if i in states:
                        return ['sus_app','sus_exp', 'sus_vsv', 'sus_rb']
                for i in ['APP_SUSP','EXP_SUSP','VSV_SUSP','RB_SUSP']:
                    if i in states:
                        return ['abort_app','abort_exp', 'abort_vsv', 'abort_rb']
            
        self._last_task_aborted = True
        return []

    def next_event(self, states, last_event, event_param):
        pass

    def restart(self):
        self._motion_done = False
        self._last_task_aborted = False


##########################################################################################################
# --- PIONEER3AT ---
class UGV_approach(Task):

    def __init__(self, param, vs_req = True, gs_req = False):
        super().__init__(param, True, gs_req)
        self.last_task_aborted = False

    def next_event(self, states, last_event, event_param):
        '''
            Approach sequence: on_vs -> st_app -> (rsm_app, end_app) -> off_vs
        '''
        if (not self._motion_done) and (last_event == 'end_app') and (event_param == self._param):
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
                    return ['st_app']
                else:
                    return ['rsm_app', 'end_app']

        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'


class UGV_exploration(Task):

    def __init__(self, param, vs_req = True, gs_req = True):
        super().__init__(param, True, True)

    def next_event(self, states, last_event, event_param = []):
        '''
            Exploration sequence: on_vs -> on_gs -> st_exp -> (rsm_exp, end_exp) -> off_gs -> off_vs
        '''        
        if (not self._motion_done) and (last_event == 'end_exp') and (event_param == self._param):
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
                if 'EXP_IDLE' in states:
                    return ['st_exp']
                else:
                    return ['rsm_exp', 'end_exp']

        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'


class UGV_verification(Task):

    def __init__(self, param, vs_req = True, gs_req = True):
        super().__init__(param, True, True)

    def next_event(self, states, last_event, event_param = []):
        '''
            VSV sequence: on_vs -> on_gs -> st_vsv -> (rsm_vsv, end_vsv) -> off_gs -> off_vs
        '''
        if (not self._motion_done) and (last_event == 'end_vsv') and (event_param == self._param):
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
                    return ['st_vsv']
                else:
                    return ['rsm_vsv', 'end_vsv']

        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'


class UGV_return(Task):

    def __init__(self, param, vs_req = False, gs_req = False):
        super().__init__(param, vs_req, gs_req)

    def next_event(self, states, last_event, event_param = []):
        '''
            Return to Base sequence:  st_rb -> (rsm_rb, end_rb)
        '''
        if (not self._motion_done) and (last_event == 'end_rb'):
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
                    return ['st_rb']
                else:
                    return ['rsm_rb', 'end_rb']

        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'


class UGV_teleoperation(Task):

    def __init__(self, param, vs_req = False, gs_req = False):
        super().__init__(param, vs_req, gs_req)

    def next_event(self, states, last_event, event_param = []):
        '''
            Teleoperation sequence:  st_tele -> (rsm_tele, end_tele)
        '''
        if (not self._motion_done) and (last_event == 'end_tele'):
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
                if 'TELE_IDLE' in states:
                    return ['st_tele']
                else:
                    return ['end_tele']

        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'

##########################################################################################################
# --- QUADCOPTER ---
class AGV_approach(Task):

    def __init__(self, param, vs_req = False):
        super().__init__(param, vs_req, False)

    def next_event(self, states, last_event, event_param = []):
        '''
            Approach sequence: st_app -> (rsm_app, end_app)
        '''
        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'
        else:
            # Before the motion have been considered as executed
            if last_event == 'end_app':
                self._motion_done = True

            # Verify if required sensors are ON
            events = self._sensors2turnON(states)
            if events:
                return events
            else:
                # Start motion after the required sensors have been activated
                if 'APP_IDLE' in states:
                    return ['st_app']
                else:
                    return ['rsm_app', 'end_app']


class AGV_assessment(Task):

    def __init__(self, param, vs_req = False):
        super().__init__(param, vs_req, False)

    def next_event(self, states, last_event, event_param = []):
        '''
            Approach sequence: -> st_assess -> (rsm_assess, end_assess) -> off_gs -> off_vs
        '''
        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'
        else:
            # Before the motion have been considered as executed
            if last_event == 'end_assess':
                self._motion_done = True

            # Verify if required sensors are ON
            events = self._sensors2turnON(states)
            if events:
                return events
            else:
                # Start motion after the required sensors have been activated
                if 'ASSESS_IDLE' in states:
                    return ['st_assess']
                else:
                    return ['rsm_assess', 'end_assess']


class AGV_v_search(Task):

    def __init__(self, param, vs_req = True):
        super().__init__(param, True, False)

    def next_event(self, states, last_event, event_param = []):
        '''
            Approach sequence: on_vs -> st_v_search -> (rsm_v_search, end_v_search) -> off_vs
        '''
        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'
        else:
            # Before the motion have been considered as executed
            if last_event == 'end_v_search':
                self._motion_done = True

            # Verify if required sensors are ON
            events = self._sensors2turnON(states)
            if events:
                return events
            else:
                # Start motion after the required sensors have been activated
                if 'SEARCH_IDLE' in states:
                    return ['st_v_search']
                else:
                    return ['rsm_v_search', 'end_v_search']


class AGV_verification(Task):

    def __init__(self, param, vs_req = True):
        super().__init__(param, True, False)

    def next_event(self, states, last_event, event_param = []):
        '''
            Approach sequence: on_vs -> st_vsv -> (rsm_vsv, end_vsv) -> off_vs
        '''
        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'
        else:
            # Before the motion have been considered as executed
            if last_event == 'end_vsv':
                self._motion_done = True

            # Verify if required sensors are ON
            events = self._sensors2turnON(states)
            if events:
                return events
            else:
                # Start motion after the required sensors have been activated
                if 'VSV_IDLE' in states:
                    return ['st_vsv']
                else:
                    return ['rsm_vsv', 'end_vsv']


class AGV_return(Task):

    def __init__(self, param, vs_req = False, gs_req = False):
        super().__init__(param, vs_req, False)

    def next_event(self, states, last_event, event_param = []):
        '''
            Approach sequence:  st_rb -> (rsm_rb, end_rb)
        '''
        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'
        else:
            # Before the motion have been considered as executed
            if last_event == 'end_rb':
                self._motion_done = True

            # Verify if required sensors are ON
            events = self._sensors2turnON(states)
            if events:
                return events
            else:
                # Start motion after the required sensors have been activated
                if 'RB_IDLE' in states:
                    return ['st_rb']
                else:
                    return ['rsm_rb', 'end_rb']


class AGV_teleoperation(Task):

    def __init__(self, param, vs_req = False, gs_req = False):
        super().__init__(param, vs_req, False)

    def next_event(self, states, last_event, event_param = []):
        '''
            Approach sequence:  st_tele -> (rsm_tele, end_tele)
        '''
        if self._motion_done:
            # After the motion have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return 'task_done'
        else:
            # Before the motion have been considered as executed
            if last_event == 'end_tele':
                self._motion_done = True

            # Verify if required sensors are ON
            events = self._sensors2turnON(states)
            if events:
                return events
            else:
                # Start motion after the required sensors have been activated
                if 'TELE_IDLE' in states:
                    return ['st_tele']
                else:
                    return ['end_tele']


##########################################################################################################
# --- BACKUP BEHAVIORS ---

# class SensorError(Task):

#     def __init__(self, param=[], vs_req = False, gs_req = False):
#         super().__init__(param, False, False)

#     def next_event(self, states, last_event, event_param = []):
#         # abort current mission if depends on the sensor
#         for i in ['APP_EXE','EXP_EXE','VSV_EXE','RB_EXE']:
#             if i in states:
#                 return ['sus_app', 'sus_exp', 'sus_vsv', 'sus_rb']


class GoBackToBase(Task):
    '''
        Behavior if the robot has a SIMPLE_FAILURE or if the battery level
        become LOW
    '''
    def __init__(self, param=[], vs_req = False, gs_req = False):
        super().__init__(param, False, False)
        self.atBase = False

    def next_event(self, states, last_event, event_param = []):
        if last_event == 'end_rb':
            self.atBase = True
            return []
        else:
            for i in ['APP_EXE','EXP_EXE','VSV_EXE','TELE_EXE','RB_EXE']:
                if i in states:
                    return ['end_app', 'end_exp', 'end_vsv', 'end_tele', 'end_rb']
            # After the maneuver have been executed
            events = self._sensors2turnOFF(states)
            if events:
                return events
            else:
                return ['st_rb']


class AbortM(Task):
    '''
        Abort maneuver if occurs a critic failure or if the robot
    '''
    def __init__(self, param=[], vs_req = False, gs_req = False):
        super().__init__(param, False, False)

    def next_event(self, states, last_event, event_param = []):
        # abort any maneuver
        for i in ['APP_EXE','EXP_EXE','VSV_EXE','TELE_EXE','RB_EXE']:
            if i in states:
                return ['sus_app', 'sus_exp', 'sus_vsv', 'sus_rb', 'abort_tele']
        for i in ['APP_SUSP','EXP_SUSP','VSV_SUSP','TELE_SUSP','RB_SUSP']:
            if i in states:
                return ['abort_app', 'abort_exp', 'abort_vsv', 'abort_rb']
        
        # After the maneuver have been aborted
        events = self._sensors2turnOFF(states)
        if events:
            return events
        else:
            return []


class V_Found(Task):
    '''
        Report victim location and execute VSV if a victim is found
    '''
    def __init__(self, param=[], vs_req = False, gs_req = False):
        super().__init__(param, True, True)
        self.v_reported = False

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
            if last_event == 'end_vsv':
                self._motion_done = True
            elif last_event == 'rep_victim':
                self.v_reported = True
                
            for i in ['APP_EXE','EXP_EXE','VSV_EXE','RB_EXE']:
                if i in states:
                    return ['sus_app', 'sus_exp', 'sus_vsv', 'sus_rb']
            if self.v_reported:
                # Verify if required sensors are ON
                events = self._sensors2turnON(states)
                if events:
                    return events
                else:
                    return ['st_vsv']
            else:
                return ['rep_victim']


class G_Found(Task):
    '''
        Report gas location
    '''
    def __init__(self, param=[], vs_req = False, gs_req = False):
        super().__init__(param, False, False)

    def next_event(self, states, last_event, event_param = []):
        if last_event != 'rep_gas':
            return ['rep_gas']
        else:
            return []

# class reqtele()