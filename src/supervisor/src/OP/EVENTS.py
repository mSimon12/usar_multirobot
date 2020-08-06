import pandas as pd
import os
import importlib
import rospy

'''
	This file contains all the events (controllable and non-controllable)
	related to the Automata created. Each high-level event has a call method
	that is responsible for executing the event.

	The procedures related to each event must be implemented into the 'handler' method.

	*If desired, the hl_2_ll function can be called into the handler to translate the
	current high-level event to a low-level signal configured on the translation_table.csv
'''

def hl_2_ll(hl_event):
	'''
	This function is responsible for translating high-level events into low-level signals.
	'''
	# Change directory
	path = os.path.dirname(os.path.abspath(__file__))
	os.chdir(path)

	# Get translation table (high-level -> low-level)
	filename = 'translation_table.csv'
	translation_table = pd.read_csv(filename)
	answer = {}
	answer['ll_event'] = translation_table[(translation_table['high-level']==hl_event)]['low-level'].array[0]		# Translate event
	answer['topic'] = translation_table[(translation_table['high-level']==hl_event)]['topic'].array[0]				# Get topic
	return answer


##### -- abort_app call & handler -- ########################################
class abort_app(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event abort_app...')
		msg = abort_app.module.events_message()
		msg.event = abort_app.output['ll_event']
		abort_app.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(abort_app.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return abort_app.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		abort_app.__enabled[name] = status


##### -- end_app call & handler -- ########################################
class end_app(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event end_app...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(end_app.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return end_app.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		end_app.__enabled[name] = status


##### -- er_app call & handler -- ########################################
class er_app(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event er_app...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(er_app.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return er_app.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		er_app.__enabled[name] = status


##### -- rsm_app call & handler -- ########################################
class rsm_app(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rsm_app...')
		msg = rsm_app.module.events_message()
		msg.event = rsm_app.output['ll_event']
		rsm_app.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rsm_app.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rsm_app.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rsm_app.__enabled[name] = status


##### -- rst_app call & handler -- ########################################
class rst_app(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rst_app...')
		msg = rst_app.module.events_message()
		msg.event = rst_app.output['ll_event']
		rst_app.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rst_app.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rst_app.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rst_app.__enabled[name] = status


##### -- st_app call & handler -- ########################################
class st_app(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event st_app...')
		msg = st_app.module.events_message()
		msg.event = st_app.output['ll_event']
		try:
			geometry = importlib.import_module('geometry_msgs.msg')
			point = geometry.Pose2D()
			point.x = param[0]
			point.y = param[1]
			point.theta = param[2]
			msg.position.append(point)
			st_app.pub.publish(msg)									#Publish message
			return True
		except:
			rospy.logwarn("ERRO!!!!\nAproach need three paramenters -> [x,y,theta].")
			return False

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(st_app.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return st_app.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		st_app.__enabled[name] = status


##### -- sus_app call & handler -- ########################################
class sus_app(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event sus_app...')
		msg = sus_app.module.events_message()
		msg.event = sus_app.output['ll_event']
		sus_app.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(sus_app.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return sus_app.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		sus_app.__enabled[name] = status


##### -- bat_L call & handler -- ########################################
class bat_L(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event bat_L...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(bat_L.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return bat_L.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		bat_L.__enabled[name] = status


##### -- bat_LL call & handler -- ########################################
class bat_LL(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event bat_LL...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(bat_LL.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return bat_LL.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		bat_LL.__enabled[name] = status


##### -- bat_OK call & handler -- ########################################
class bat_OK(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event bat_OK...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(bat_OK.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return bat_OK.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		bat_OK.__enabled[name] = status


##### -- call_tele call & handler -- ########################################
class call_tele(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event call_tele...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(call_tele.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return call_tele.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		call_tele.__enabled[name] = status


##### -- no_rb_pref call & handler -- ########################################
class no_rb_pref(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event no_rb_pref...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(no_rb_pref.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return no_rb_pref.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		no_rb_pref.__enabled[name] = status


##### -- rb_pref call & handler -- ########################################
class rb_pref(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rb_pref...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rb_pref.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rb_pref.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rb_pref.__enabled[name] = status


##### -- rep_gas call & handler -- ########################################
class rep_gas(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rep_gas...')
		msg = rep_gas.module.events_message()
		msg.event = rep_gas.output['ll_event']
		try:
			geometry = importlib.import_module('geometry_msgs.msg')
			point = geometry.Pose2D()
			point.x = param[0]
			point.y = param[1]
			point.theta = 0
			msg.position.append(point)
			rep_gas.pub.publish(msg)									#Publish message
			return True
		except:
			rospy.logwarn("ERRO!!!!\nReport gas need gas position [x,y].")
			return False


	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rep_gas.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rep_gas.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rep_gas.__enabled[name] = status


##### -- rep_victim call & handler -- ########################################
class rep_victim(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rep_victim...')
		msg = rep_victim.module.events_message()
		msg.event = rep_victim.output['ll_event']
		try:
			geometry = importlib.import_module('geometry_msgs.msg')
			point = geometry.Pose2D()
			point.x = param[0]
			point.y = param[1]
			point.theta = 0
			msg.position.append(point)
			rep_victim.pub.publish(msg)									#Publish message
			return True
		except:
			rospy.logwarn("ERRO!!!!\nReport victim need victim position [x,y].")
			return False

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rep_victim.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rep_victim.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rep_victim.__enabled[name] = status


##### -- req_assist call & handler -- ########################################
class req_assist(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event req_assist...')
		msg = req_assist.module.events_message()
		msg.event = req_assist.output['ll_event']
		req_assist.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(req_assist.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return req_assist.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		req_assist.__enabled[name] = status


##### -- abort_exp call & handler -- ########################################
class abort_exp(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event abort_exp...')
		msg = abort_exp.module.events_message()
		msg.event = abort_exp.output['ll_event']
		abort_exp.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(abort_exp.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return abort_exp.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		abort_exp.__enabled[name] = status


##### -- end_exp call & handler -- ########################################
class end_exp(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event end_exp...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(end_exp.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return end_exp.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		end_exp.__enabled[name] = status


##### -- er_exp call & handler -- ########################################
class er_exp(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event er_exp...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(er_exp.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return er_exp.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		er_exp.__enabled[name] = status


##### -- rsm_exp call & handler -- ########################################
class rsm_exp(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rsm_exp...')
		msg = rsm_exp.module.events_message()
		msg.event = rsm_exp.output['ll_event']
		rsm_exp.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rsm_exp.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rsm_exp.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rsm_exp.__enabled[name] = status


##### -- rst_exp call & handler -- ########################################
class rst_exp(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rst_exp...')
		msg = rst_exp.module.events_message()
		msg.event = rst_exp.output['ll_event']
		rst_exp.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rst_exp.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rst_exp.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rst_exp.__enabled[name] = status


##### -- st_exp call & handler -- ########################################
class st_exp(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event st_exp...')
		msg = st_exp.module.events_message()
		msg.event = st_exp.output['ll_event']
		try:
			geometry = importlib.import_module('geometry_msgs.msg')
			for p in param:
				point = geometry.Pose2D()
				point.x = p[0]
				point.y = p[1]
				point.theta = 0
				msg.position.append(point)						#Insert polygon points
			st_exp.pub.publish(msg)									#Publish message
			return True
		except:
			rospy.logwarn("ERRO!!!!\nExploration need at leat three polygon points.")
			return False

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(st_exp.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return st_exp.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		st_exp.__enabled[name] = status


##### -- sus_exp call & handler -- ########################################
class sus_exp(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event sus_exp...')
		msg = sus_exp.module.events_message()
		msg.event = sus_exp.output['ll_event']
		sus_exp.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(sus_exp.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return sus_exp.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		sus_exp.__enabled[name] = status


##### -- critic_fail call & handler -- ########################################
class critic_fail(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event critic_fail...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(critic_fail.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return critic_fail.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		critic_fail.__enabled[name] = status


##### -- fail call & handler -- ########################################
class fail(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event fail...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(fail.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return fail.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		fail.__enabled[name] = status


##### -- pos_fail call & handler -- ########################################
class pos_fail(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event pos_fail...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(pos_fail.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return pos_fail.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		pos_fail.__enabled[name] = status


##### -- rst_f call & handler -- ########################################
class rst_f(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rst_f...')
		msg = rst_f.module.events_message()
		msg.event = rst_f.output['ll_event']
		rst_f.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rst_f.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rst_f.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rst_f.__enabled[name] = status


##### -- er_gs call & handler -- ########################################
class er_gs(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event er_gs...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(er_gs.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return er_gs.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		er_gs.__enabled[name] = status


##### -- gas_found call & handler -- ########################################
class gas_found(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event gas_found...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(gas_found.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return gas_found.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		gas_found.__enabled[name] = status


##### -- off_gs call & handler -- ########################################
class off_gs(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event off_gs...')
		msg = off_gs.module.events_message()
		msg.event = off_gs.output['ll_event']
		off_gs.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(off_gs.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return off_gs.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		off_gs.__enabled[name] = status


##### -- on_gs call & handler -- ########################################
class on_gs(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event on_gs...')
		msg = on_gs.module.events_message()
		msg.event = on_gs.output['ll_event']
		on_gs.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(on_gs.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return on_gs.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		on_gs.__enabled[name] = status


##### -- rst_gs call & handler -- ########################################
class rst_gs(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rst_gs...')
		msg = rst_gs.module.events_message()
		msg.event = rst_gs.output['ll_event']
		rst_gs.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rst_gs.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rst_gs.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rst_gs.__enabled[name] = status


##### -- move_to call & handler -- ########################################
class move_to(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event move_to...')
		msg = move_to.module.events_message()
		msg.event = move_to.output['ll_event']
		move_to.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(move_to.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return move_to.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		move_to.__enabled[name] = status


##### -- abort_rb call & handler -- ########################################
class abort_rb(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event abort_rb...')
		msg = abort_rb.module.events_message()
		msg.event = abort_rb.output['ll_event']
		abort_rb.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(abort_rb.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return abort_rb.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		abort_rb.__enabled[name] = status


##### -- end_rb call & handler -- ########################################
class end_rb(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event end_rb...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(end_rb.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return end_rb.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		end_rb.__enabled[name] = status


##### -- er_rb call & handler -- ########################################
class er_rb(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event er_rb...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(er_rb.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return er_rb.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		er_rb.__enabled[name] = status


##### -- rsm_rb call & handler -- ########################################
class rsm_rb(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rsm_rb...')
		msg = rsm_rb.module.events_message()
		msg.event = rsm_rb.output['ll_event']
		rsm_rb.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rsm_rb.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rsm_rb.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rsm_rb.__enabled[name] = status


##### -- rst_rb call & handler -- ########################################
class rst_rb(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rst_rb...')
		msg = rst_rb.module.events_message()
		msg.event = rst_rb.output['ll_event']
		rst_rb.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rst_rb.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rst_rb.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rst_rb.__enabled[name] = status


##### -- st_rb call & handler -- ########################################
class st_rb(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event st_rb...')
		msg = st_rb.module.events_message()
		msg.event = st_rb.output['ll_event']
		st_rb.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(st_rb.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return st_rb.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		st_rb.__enabled[name] = status


##### -- sus_rb call & handler -- ########################################
class sus_rb(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event sus_rb...')
		msg = sus_rb.module.events_message()
		msg.event = sus_rb.output['ll_event']
		sus_rb.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(sus_rb.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return sus_rb.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		sus_rb.__enabled[name] = status


##### -- end_tele call & handler -- ########################################
class end_tele(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event end_tele...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(end_tele.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return end_tele.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		end_tele.__enabled[name] = status


##### -- er_tele call & handler -- ########################################
class er_tele(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event er_tele...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(er_tele.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return er_tele.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		er_tele.__enabled[name] = status


##### -- rst_tele call & handler -- ########################################
class rst_tele(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rst_tele...')
		msg = rst_tele.module.events_message()
		msg.event = rst_tele.output['ll_event']
		rst_tele.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rst_tele.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rst_tele.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rst_tele.__enabled[name] = status


##### -- st_tele call & handler -- ########################################
class st_tele(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event st_tele...')
		msg = st_tele.module.events_message()
		msg.event = st_tele.output['ll_event']
		st_tele.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(st_tele.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return st_tele.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		st_tele.__enabled[name] = status


##### -- abort_vsv call & handler -- ########################################
class abort_vsv(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event abort_vsv...')
		msg = abort_vsv.module.events_message()
		msg.event = abort_vsv.output['ll_event']
		abort_vsv.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(abort_vsv.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return abort_vsv.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		abort_vsv.__enabled[name] = status


##### -- end_vsv call & handler -- ########################################
class end_vsv(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event end_vsv...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(end_vsv.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return end_vsv.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		end_vsv.__enabled[name] = status


##### -- er_vsv call & handler -- ########################################
class er_vsv(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event er_vsv...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(er_vsv.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return er_vsv.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		er_vsv.__enabled[name] = status


##### -- rsm_vsv call & handler -- ########################################
class rsm_vsv(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rsm_vsv...')
		msg = rsm_vsv.module.events_message()
		msg.event = rsm_vsv.output['ll_event']
		rsm_vsv.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rsm_vsv.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rsm_vsv.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rsm_vsv.__enabled[name] = status


##### -- rst_vsv call & handler -- ########################################
class rst_vsv(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rst_vsv...')
		msg = rst_vsv.module.events_message()
		msg.event = rst_vsv.output['ll_event']
		rst_vsv.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rst_vsv.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rst_vsv.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rst_vsv.__enabled[name] = status


##### -- st_vsv call & handler -- ########################################
class st_vsv(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event st_vsv...')
		msg = st_vsv.module.events_message()
		msg.event = st_vsv.output['ll_event']
		try:
			msg.info = param[0]
			
			geometry = importlib.import_module('geometry_msgs.msg')
			point = geometry.Pose2D()
			point.x = param[1]
			point.y = param[2]
			point.theta = 0

			msg.position.append(point)
			st_vsv.pub.publish(msg)								#Publish message
			return True
		except:
			rospy.logwarn("ERRO!!!!\nSurroundings verification need at a victim id and position -> [id,x,y]")
			return False

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(st_vsv.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return st_vsv.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		st_vsv.__enabled[name] = status


##### -- sus_vsv call & handler -- ########################################
class sus_vsv(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event sus_vsv...')
		msg = sus_vsv.module.events_message()
		msg.event = sus_vsv.output['ll_event']
		sus_vsv.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(sus_vsv.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return sus_vsv.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		sus_vsv.__enabled[name] = status


##### -- er_vs call & handler -- ########################################
class er_vs(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event er_vs...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(er_vs.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return er_vs.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		er_vs.__enabled[name] = status


##### -- off_vs call & handler -- ########################################
class off_vs(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event off_vs...')
		msg = off_vs.module.events_message()
		msg.event = off_vs.output['ll_event']
		off_vs.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(off_vs.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return off_vs.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		off_vs.__enabled[name] = status


##### -- on_vs call & handler -- ########################################
class on_vs(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event on_vs...')
		msg = on_vs.module.events_message()
		msg.event = on_vs.output['ll_event']
		on_vs.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(on_vs.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return on_vs.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		on_vs.__enabled[name] = status


##### -- rst_vs call & handler -- ########################################
class rst_vs(object):
	__enabled = {}
	__type = 'controllable'

	# For ROS
	module = importlib.import_module('pioneer3at_controllers.msg')
	output = hl_2_ll(__qualname__)
	pub = rospy.Publisher('/{}'.format(output['topic']), module.events_message, queue_size=10)

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event rst_vs...')
		msg = rst_vs.module.events_message()
		msg.event = rst_vs.output['ll_event']
		rst_vs.pub.publish(msg)					#Publish message
		return True

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(rst_vs.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return rst_vs.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		rst_vs.__enabled[name] = status


##### -- victim_found call & handler -- ########################################
class victim_found(object):
	__enabled = {}
	__type = 'uncontrollable'

	@classmethod
	def handler(cls, param = None):
		##### >>>>>>>>>>>>>>>>>>>>>    WRITE YOUR CODE HERE    <<<<<<<<<<<<<<<<<<<<<<< #####
		print('Executing event victim_found...')

	@classmethod
	def get_status(cls):
		'''
		True: event enabled;
		False: event not allowed.
		'''
		return all(victim_found.__enabled.values())

	@classmethod
	def is_controllable(cls):
		return victim_found.__type == 'controllable'

	@classmethod
	def set_status(cls, name, status):
		victim_found.__enabled[name] = status

