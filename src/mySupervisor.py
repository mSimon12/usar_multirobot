
from SCT import SupBuilder

sup1 = SupBuilder('mySupervisor')
sup1.insert_state('A')
sup1.insert_state('B')
sup1.insert_state('C')
sup1.insert_transition('t1','A','B')
sup1.insert_transition('t2','C','B')
sup1.insert_transition('t3','B','A')
sup1.insert_transition('t3','C','B')
sup1.show_states()

sup1.remove_transition('t1','B')
sup1.show_states()

sup1.remove_state('A')
sup1.show_states()

sup1.show_supervisor()

