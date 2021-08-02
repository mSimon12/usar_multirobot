
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


##########################################################################################################
# --- BACKUP BEHAVIORS ---

class CriticSystem(Task):
    '''
        Behavior if the robot has a CRITICAL FAILURE or if the battery level become CRITIC

        - the robot must abort all maneuvers and stop sensors.
    '''
    def __init__(self):
        pass

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
        table = {}

        return table


class HRI(Task):
    '''
        Behavior if the robot has a MANEUVER ERROR or if commander called teleoperation

        - In case of maneuver error, the robot wait require human assistance and wait for it;
        - In case of teleoperation requisition by the commander, the robots start tele mode.
    '''
    def __init__(self):
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
        table = {}

        return table


class DegradedMode2(Task):
    '''
        Behavior if the robot has a POSITION FAILURE or SENSOR ERROR with current task depending on it

        - the robot must abort all maneuvers (except teleoperation) and stop sensors.
    '''
    def __init__(self):
        pass

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
        table = {}

        return table


class DegradedMode1(Task):
    '''
        Behavior if the robot has a SIMPLE FAILURE or if the battery level become LOW

        - the robot must abort all maneuvers (except teleoperation) and stop sensors.
    '''
    def __init__(self):
        self.atBase = False

    '''
        Function to get baseline events --> wait execution of current maneuver, turn sensors off and return to base
    '''
    def next_event(self, states, last_event, event_param = []):
        if last_event == 'end_rb':
            self.atBase = True
        
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
        table = {}

        return table


class Victim(Task):
    '''
        Behavior if the robot has found a VICTIM

        - the robot must suspend current maneuver and execute VICTIM SURROUNDINGS VERIFICATION
    '''
    def __init__(self):
        pass       

    def next_event(self, states, last_event, event_param = []):
        pass

    '''
        Priority of events affected by this mode of operation
    '''    
    def get_priorities_table(self):
        table = {}

        return table


#### OLD MODES ############################################################################################

# class GoBackToBase(Task):
#     '''
#         Behavior if the robot has a SIMPLE_FAILURE or if the battery level
#         become LOW
#     '''
#     def __init__(self, param=[], vs_req = False, gs_req = False):
#         super().__init__(param, False, False)
#         self.atBase = False

#     def next_event(self, states, last_event, event_param = []):
#         if last_event == 'end_rb':
#             self.atBase = True
#         elif last_event == 'st_rb':
#             return ['end_rb']
#         elif not self.atBase:
#             for i in ['APP_EXE','EXP_EXE','VSV_EXE','TELE_EXE','RB_EXE']:
#                 if i in states:
#                     return ['end_app', 'end_exp', 'end_vsv', 'end_tele', 'end_rb']
#             # After the maneuver have been executed
#             events = self._sensors2turnOFF(states)
#             if events:
#                 return events
#             else:
#                 return ['st_rb']
#         return []

#     def restart(self):
#         super().restart()
#         self.atBase = False


# class AbortM(Task):
#     '''
#         Abort maneuver if occurs a critic failure or if the robot
#     '''
#     def __init__(self, param=[], vs_req = False, gs_req = False):
#         super().__init__(param, False, False)
#         self.pose_reported = False

#     def next_event(self, states, last_event, event_param = []):
#         # Verify if the last maneuver must be aborted 
#         event_to_abort = self._abort_last_M(states)
#         if event_to_abort:
#             return event_to_abort
#         # for i in ['APP_EXE','EXP_EXE','VSV_EXE','TELE_EXE','RB_EXE']:
#         #     if i in states:
#         #         return ['sus_app', 'sus_exp', 'sus_vsv', 'sus_rb', 'abort_tele']
#         # for i in ['APP_SUSP','EXP_SUSP','VSV_SUSP','TELE_SUSP','RB_SUSP']:
#         #     if i in states:
#         #         return ['abort_app', 'abort_exp', 'abort_vsv', 'abort_rb']
        
#         if last_event == 'rep_self_pos':
#             self.pose_reported = True
#         # elif not (('BAT_CRITICAL' in states) or ('CRITIC_FAILURE' in states)):
#         #     self.pose_reported = False

#         if self.pose_reported:
#             return []
#         else:
#             # After the maneuver have been aborted
#             events = self._sensors2turnOFF(states)
#             if events:
#                 return events
#             else:
#                 return ['rep_self_pos']

#     def restart(self):
#         super().restart()
#         self.pose_reported = False


# class V_Found(Task):
#     '''
#         Report victim location and execute VSV if a victim is found
#     '''
#     def __init__(self, param=[], vs_req = False, gs_req = False):
#         super().__init__(param, True, True)
#         self.v_reported = False
#         self._param = ['victim', param[0], param[1]]

#     def next_event(self, states, last_event, event_param = []):
#         # abort any maneuver
#         if self._motion_done:
#             # After the motion have been executed
#             events = self._sensors2turnOFF(states)
#             if events:
#                 return events
#             else:
#                 return []
#         else:
#             # Before the motion have been considered as executed
#             if last_event == 'end_vsv':
#                 self._motion_done = True
#             elif last_event == 'rep_victim':
#                 self.v_reported = True
                
#             # Suspend current task
#             for i in ['APP_EXE','EXP_EXE','RB_EXE']:
#                 if i in states:
#                     return ['sus_app', 'sus_exp', 'sus_rb']
            
#             # Verify if the victim position was informed to the Commander
#             if self.v_reported:
#                 # Verify if required sensors are ON
#                 events = self._sensors2turnON(states)
#                 if events:
#                     return events
#                 else:
#                     return ['st_vsv']
#             else:
#                 return ['rep_victim']

#     def restart(self):
#         super().restart()
#         self.v_reported = False


# class G_Found(Task):
#     '''
#         Report gas location
#     '''
#     def __init__(self, param=[], vs_req = False, gs_req = False):
#         super().__init__(param, False, False)

#     def next_event(self, states, last_event, event_param = []):
#          # Verify if the gas leak position was informed to the Commander
#         if last_event != 'rep_gas':
#             return ['rep_gas']
#         else:
#             return []


# class ReqHelp(Task):
#     '''
#         Require a human to help on the motion
#     '''
#     def __init__(self, param=[], vs_req = False, gs_req = False):
#         super().__init__(param, False, False)
#         self._assit_required = False
#         self._tele_executed = False
#         self._tele_required = False
    
#     def next_event(self, states, last_event, event_param = []):
#         event_to_abort = self._abort_last_M(states)
#         if event_to_abort:
#             return event_to_abort

#         if last_event == 'req_assist':
#             self._assit_required = True
#         elif last_event == 'call_tele':
#             self._tele_required = True
#         elif last_event == 'end_tele':
#             self._tele_executed = True
#         elif last_event in ['rst_app', 'rst_exp', 'rst_vsv', 'rst_rb','er_tele']:
#             return []
        
#         if not self._assit_required:
#             return ['req_assist']
#         else:  
#             if self._tele_required:
#                 if self._tele_executed:
#                     return ['rst_app', 'rst_exp', 'rst_vsv', 'rst_rb']
#                 if 'TELE_IDLE' in states:
#                     sleep(0.5)
#                     return ['st_tele']
#                 else:
#                     return ['end_tele','er_tele']
#             else:
#                 return ['call_tele']

#     def restart(self):
#         super().restart()
#         self._assit_required = False
#         self._tele_executed = False
#         self._tele_required = False

        
# class TeleCalled(Task):
#     '''
#         Behavior if the Commander require teleoperation
#     '''
#     def __init__(self, param=[], vs_req = False, gs_req = False):
#         super().__init__(param, False, False)

#     def next_event(self, states, last_event, event_param = []):
#         if last_event in ['end_tele','er_tele']:
#             return []
#         else:
#             for i in ['APP_EXE','EXP_EXE','VSV_EXE','RB_EXE']:
#                 if i in states:
#                     return ['sus_app', 'sus_exp', 'sus_vsv', 'sus_rb']
#             for i in ['APP_ERROR','EXP_ERROR','VSV_ERROR','RB_ERROR']:
#                 if i in states:
#                     return ['rst_app', 'rst_exp', 'rst_vsv', 'rst_rb']
#             # After the maneuver have been executed
#             if 'TELE_IDLE' in states:
#                 sleep(0.5)
#                 return ['st_tele']
#             elif 'TELE_ERROR' in states:
#                 return ['rst_tele']
#             else:
#                 return ['end_tele']

# class PosErro(Task):
#     '''
#         Abort maneuver if occurs a position failure and require human assistance withou automatically starting teleoperation
#     '''
#     def __init__(self, param=[], vs_req = False, gs_req = False):
#         super().__init__(param, False, False)
#         self.pose_reported = False
#         self._assit_required = False

#     def next_event(self, states, last_event, event_param = []):
#         # Verify if the last maneuver must be aborted 
#         event_to_abort = self._abort_last_M(states)
#         if event_to_abort:
#             return event_to_abort

#         if last_event == 'rep_self_pos':
#             self.pose_reported = True
#         elif last_event == 'req_assist':
#             self._assit_required = True

#         if self.pose_reported:
#             if not self._assit_required :
#                 return ['req_assist']
#             else:
#                 events = self._sensors2turnOFF(states)
#                 if events:
#                     return events
#                 else:
#                     return []
#         else:
#             return ['rep_self_pos']

#     def restart(self):
#         super().restart()
#         self.pose_reported = False
#         self._assit_required = False