#!/usr/bin/env python

import os

# Supervisor libs
from lib.Automaton import MultiAutomata
from lib.StateMachine import StateMachine, Supervisor
from lib.ProductSystem import ProductSystem
from Intereface import EventInterface
# from ugv.TaskManager_UGV import TaskManager
from lib.EventReceiver import EventReceiver
from lib.EventsFilter import EventsFilter

# ROS libs
from system_msgs.msg import task_message, events_message
import rospy
import importlib

#Change to the current directory
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

if __name__ == "__main__":
    NAME = rospy.get_param("robot_name", default="")
    ROBOT_TYPE = rospy.get_param("supervisor/robot_type", default="")

    rospy.init_node("supervisor", anonymous=False)

    # Set the models to be applied
    if ROBOT_TYPE == "pioneer3at":
        PLANT_FILE = "plant_pioneer3at"
        SUP_FILE = "sup_pioneer3at"
        module = importlib.import_module('ugv.TaskManager_UGV')
        TaskManager = module.TaskManager
    elif ROBOT_TYPE == "uav":
        PLANT_FILE = "plant_uav"
        SUP_FILE = "sup_uav"
        module = importlib.import_module('uav.TaskManager_UAV')
        TaskManager = module.TaskManager


    #############################################################################
    #### Create Multiple State Machines from one file  #################
    G = MultiAutomata("{}_PLANT".format(NAME))
    G.read_xml("files/{}.xml".format(PLANT_FILE))         # File with multiple Automata
    SM = {}
    for aut in G.get_automata().values():
        size = len("{}_PLANT-".format(NAME))
        name = aut.get_name()
        if name.startswith("{}_PLANT".format(NAME)):
            name = name[size:]
        SM[name] = StateMachine(aut)

    #############################################################################
    #### Create Multiple Supervisors from one file  ###################
    S = MultiAutomata("{}_SUP".format(NAME))
    S.read_xml("files/{}.xml".format(SUP_FILE))         # File with multiple Automata
    SUP = {}
    for aut in S.get_automata().values():
        size = len("{}_SUP-".format(NAME))
        name = aut.get_name()
        if name.startswith("{}_SUP".format(NAME)):
            name = name[size:]
        SUP[name] = Supervisor(aut)

    #############################################################################
    #### Start the Task Manager  ################################################
    tm = TaskManager()
    rospy.Subscriber("task", task_message, tm.taskCallback)

    #############################################################################
    #### Start the Events Filter ####################################################
    e_filter = EventsFilter()

    #############################################################################
    #### Start the Interface ####################################################
    # interface = EventInterface()
    # interface.start()

    #############################################################################
    #### Start Product System ###################################################
    ps =  ProductSystem(SM, SUP)
    ps.start()

    #############################################################################
    #### Start the Events Receiver  #############################################
    receiver = EventReceiver()
    #Start a subscrier for all topics that may generate an event
    # namespace = rospy.get_namespace()

    rospy.Subscriber("battery_monitor/out",events_message, receiver.receive_event, '{}/battery_monitor/out'.format(NAME))
    rospy.Subscriber("failures_monitor/out",events_message, receiver.receive_event, '{}/failures_monitor/out'.format(NAME))
    rospy.Subscriber("maneuvers/out",events_message, receiver.receive_event, '{}/maneuvers/out'.format(NAME))
    rospy.Subscriber("victim_sensor/out",events_message, receiver.receive_event, '{}/victim_sensor/out'.format(NAME))
    if(ROBOT_TYPE == "pioneer3at"):
        rospy.Subscriber("gas_sensor/out",events_message, receiver.receive_event, '{}/gas_sensor/out'.format(NAME))

    rospy.Subscriber("ihm/out",events_message, receiver.receive_event, 'ihm/out')