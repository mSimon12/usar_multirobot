import pandas as pd
import inspect

from lib.ProductSystem import trigger_event

class EventReceiver(object):
    '''
        Class responsible for translating input signals, coming from the real system,
        to responses that are sent to the Product System.

        *To acomplish the translation this class use an auxiliar csv file were the equivalente
        low-level input is associated to an event recognised by the Plant.
            -> At this point is only possible to associate only a single input to each event.
    '''

    def __init__(self):
        # Get translation table (low-level -> high-level)
        filename = "OP/translation_table.csv"
        self.__translation_table = pd.read_csv(filename)

        # Variables for conversion control
        self.__last_battery = 'bat_OK'

    def receive_event(self, msg, topic):
        '''
            Here you implement the system responsible for receiving

            As an example, you could run this method as a Thread that monitor the occurance of low-level inputs
            and apply the following code to translate it to high-level event
        '''
        hl_event = None
        ll_event = msg.event                                                        # Get the name of the low-level event

        if (ll_event == 'battery_level') and (topic == self.__translation_table[(self.__translation_table['low-level']==ll_event)]['topic'].array[0]):
            # Convert battery level to high_level event
            battery_level = msg.param[0]                                            # Get battery level            
            if (battery_level < 10) and (self.__last_battery != 'bat_LL'):
                hl_event = 'bat_LL'
                self.__last_battery = hl_event
            elif (battery_level > 10) and (battery_level < 50) and (self.__last_battery != 'bat_L'):
                hl_event = 'bat_L'
                self.__last_battery = hl_event 
            elif (battery_level >= 50) and (self.__last_battery != 'bat_OK'):
                hl_event = 'bat_OK'
                self.__last_battery = hl_event 
        else:
            try:
                hl_event = self.__translation_table[(self.__translation_table['low-level']==ll_event) & (self.__translation_table['topic']==topic)]['high-level'].array[0]        # Translate event
            except:
                pass
            
        # Get the parameters
        param = []
        if msg.info:
            param.append(msg.info)
        if msg.param:
            param.append(msg.param)
        if msg.position:
            param.append(msg.position)

        if hl_event:
            trigger_event(hl_event, param)                                              # Trigger the received eventparametersparameters