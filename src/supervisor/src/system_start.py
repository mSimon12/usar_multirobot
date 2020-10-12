#!/usr/bin/env python

import os

# Supervisor libs
from lib.Automaton import MultiAutomata
from lib.StateMachine import StateMachine, Supervisor
from lib.ProductSystem import ProductSystem
from Intereface import EventInterface
from ugv.TaskManager_UGV import TaskManager
from lib.EventReceiver import EventReceiver

# ROS libs
from system_msgs.msg import task_message, events_message
import rospy

#Change to the current directory
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

if __name__ == "__main__":
    NAME = rospy.get_param("robot_name", default="")
    rospy.init_node("{}_supervisor".format(NAME), anonymous=False)

    #############################################################################
    #### Create Multiple State Machines from one file  #################
    G = MultiAutomata('Plant')
    G.read_xml('files/plant.xml')         # File with multiple Automata
    SM = {}
    for aut in G.get_automata().values():
        SM[aut.get_name()] = StateMachine(aut)


    #############################################################################
    #### Create Multiple Supervisors from one file  ###################
    S = MultiAutomata('Supervisors')
    S.read_xml('files/supervisors.xml')         # File with multiple Automata
    SUP = {}
    for aut in S.get_automata().values():
        SUP[aut.get_name()] = Supervisor(aut)


    #############################################################################
    #### Start the Task Manager  ################################################
    tm = TaskManager()
    rospy.Subscriber("task", task_message, tm.taskCallback)

    #############################################################################
    #### Start the Interface ####################################################
    interface = EventInterface()
    interface.start()

    #############################################################################
    #### Start Product System ###################################################
    ps =  ProductSystem(SM, SUP)
    ps.start()

    #############################################################################
    #### Start the Events Receiver  #############################################
    receiver = EventReceiver()
    #Start a subscrier for all topics that may generate an event
    # namespace = rospy.get_namespace()
    rospy.Subscriber("victim_sensor/out",events_message, receiver.receive_event, '{}/victim_sensor/out'.format(NAME))
    rospy.Subscriber("gas_sensor/out",events_message, receiver.receive_event, '{}/gas_sensor/out'.format(NAME))
    rospy.Subscriber("battery_monitor/out",events_message, receiver.receive_event, '{}/battery_monitor/out'.format(NAME))
    rospy.Subscriber("failures_monitor/out",events_message, receiver.receive_event, '{}/failures_monitor/out'.format(NAME))
    rospy.Subscriber("maneuvers/out",events_message, receiver.receive_event, '{}/maneuvers/out'.format(NAME))
    rospy.Subscriber("/ihm/out",events_message, receiver.receive_event, 'ihm/out')