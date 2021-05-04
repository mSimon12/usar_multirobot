import pandas as pd
import inspect

import rospy

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

        self.NAME = rospy.get_param("robot_name", default="")
        self.ROBOT_TYPE = rospy.get_param("supervisor/robot_type", default="")

        # Variables for conversion control
        if self.ROBOT_TYPE == 'uav':
            self.__last_battery = 'uav_bat_OK'
        else:
            self.__last_battery = 'bat_OK'

    def receive_event(self, msg, topic):
        '''
            Here you implement the system responsible for receiving

            As an example, you could run this method as a Thread that monitor the occurance of low-level inputs
            and apply the following code to translate it to high-level event
        '''
        hl_event = None
        ll_event = msg.event                                                        # Get the name of the low-level event

        # rospy.loginfo("LOW EVENT: {}".format(ll_event))
        # rospy.loginfo("FROM TOPIC: {}".format(topic))

        size = len("{}/".format(self.NAME))
        if topic.startswith("{}/".format(self.NAME)):
            topic = topic[size:]

        # The topic from table that is ralated to the current event and robot type
        try:
            topic_on_table = self.__translation_table[(self.__translation_table['low-level']==ll_event) &
                            (self.__translation_table['robot_type']==self.ROBOT_TYPE)]['topic'].array[0]
        except:
            rospy.logwarn("No match for received low level event!!!")


        ############################### UGV procedures ######################################
        if (self.ROBOT_TYPE == 'pioneer3at'):
            if (ll_event == 'battery_level') and (topic == topic_on_table):
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
                    size = len("/{}/".format(self.NAME))
                    if topic.startswith("/{}/".format(self.NAME)):
                        topic = topic[size:]
                    hl_event = self.__translation_table[(self.__translation_table['low-level']==ll_event) & (self.__translation_table['topic']==topic)
                                                                    & (self.__translation_table['robot_type']==self.ROBOT_TYPE)]['high-level'].array[0]        # Translate event
                except:
                    pass

            # Get the parameters
            param = []
            if msg.info:
                param.append(msg.info)
            if msg.param:
                for p in msg.param:
                    param.append(p)
            if msg.position:
                if len(msg.position) > 1:
                    # Create a vector of multiple points
                    for p in msg.position:
                        param.append((p.linear.x, p.linear.y))
                else:
                    param.append(msg.position[0].linear.x)
                    param.append(msg.position[0].linear.y)
                    param.append(msg.position[0].angular.z)
                # param.append(msg.position)


        ############################### UAV procedures ######################################
        elif (self.ROBOT_TYPE == 'uav'):
            if (ll_event == 'battery_level') and (topic == topic_on_table):
                # Convert battery level to high_level event
                battery_level = msg.param[0]                                            # Get battery level            
                if (battery_level < 10) and (self.__last_battery != 'uav_bat_LL'):
                    hl_event = 'uav_bat_LL'
                    self.__last_battery = hl_event
                elif (battery_level > 10) and (battery_level < 50) and (self.__last_battery != 'uav_bat_L'):
                    hl_event = 'uav_bat_L'
                    self.__last_battery = hl_event 
                elif (battery_level >= 50) and (self.__last_battery != 'uav_bat_OK'):
                    hl_event = 'uav_bat_OK'
                    self.__last_battery = hl_event 
            else:
                try:
                    size = len("/{}/".format(self.NAME))
                    if topic.startswith("/{}/".format(self.NAME)):
                        topic = topic[size:]
                    hl_event = self.__translation_table[(self.__translation_table['low-level']==ll_event) & (self.__translation_table['topic']==topic)
                                                                    & (self.__translation_table['robot_type']==self.ROBOT_TYPE)]['high-level'].array[0]        # Translate event
                except:
                    pass

            # Get the parameters
            param = []
            if msg.info:
                param.append(msg.info)
            if msg.param:
                param.append(msg.param)
            if msg.position:
                if len(msg.position) > 1:
                    # Create a vector of multiple points
                    for p in msg.position:
                        param.append((p.linear.x, p.linear.y))
                else:
                    param.append(msg.position[0].linear.x)
                    param.append(msg.position[0].linear.y)
                    param.append(msg.position[0].linear.z)
                    param.append(msg.position[0].angular.z)
                # param.append(msg.position)

        # rospy.loginfo("EVENT: {}".format(hl_event))

        if hl_event:
            trigger_event(hl_event, param)                                              # Trigger the received eventparametersparameters