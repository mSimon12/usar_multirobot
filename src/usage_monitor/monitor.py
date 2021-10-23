#!/usr/bin/env python

import pandas as pd
from threading import Condition
from rosgraph_msgs.msg import Clock

import functools
import os
import subprocess

import rosnode
import rospy

import psutil

try:
  from xmlrpc.client import ServerProxy
except ImportError:
  from xmlrpclib import ServerProxy

from std_msgs.msg import Float32, UInt64


def ns_join(*names):
  return functools.reduce(rospy.names.ns_join, names, "")

class Node:
  def __init__(self, name, pid):
    self.name = name
    self.proc = psutil.Process(pid)
    self.cpu_publisher = rospy.Publisher(ns_join("~", name[1:], "cpu"), Float32, queue_size=20)
    self.mem_publisher = rospy.Publisher(ns_join("~", name[1:], "mem"), UInt64, queue_size=20)


  def alive(self):
    return self.proc.is_running()


time = 0
time_me = Condition()

def time_update(msg):
    time_me.acquire()
    global time
    time = msg.clock.secs + msg.clock.nsecs/1000000000
    time_me.release()

if __name__ == "__main__":
  rospy.init_node("cpu_monitor")
  master = rospy.get_master()

  poll_period = rospy.get_param('~poll_period', 1.0)

  this_ip = os.environ.get("ROS_IP")

  node_map = {}
  ignored_nodes = set()

  #Change to the current directory
  path = os.path.dirname(os.path.abspath(__file__))
  os.chdir(path)
  robots = ['UAV_1', 'UAV_2', 'pioneer3at_1', 'pioneer3at_2']
  cols = ['total_cpu', 'total_mem', 'gazebo_cpu', 'gazebo_mem']
  for r in robots:
    cols.append('{}_sup_cpu'.format(r))
    cols.append('{}_sup_mem'.format(r))
  usage_monitor = pd.DataFrame(columns=cols)

  rospy.Subscriber("/clock", Clock, time_update)

  while not rospy.is_shutdown():
    
    for node in rosnode.get_node_names():
      if node in node_map or node in ignored_nodes:
        continue

      node_api = rosnode.get_api_uri(master, node)[2]
      if not node_api:
        rospy.logerr("[cpu monitor] failed to get api of node %s (%s)" % (node, node_api))
        continue

      ros_ip = node_api[7:] # strip http://
      ros_ip = ros_ip.split(':')[0] # strip :<port>/
      local_node = "localhost" in node_api or \
                   "127.0.0.1" in node_api or \
                   (this_ip is not None and this_ip == ros_ip) or \
                   subprocess.check_output("hostname").decode('utf-8').strip() in node_api
      if not local_node:
        ignored_nodes.add(node)
        rospy.loginfo("[cpu monitor] ignoring node %s with URI %s" % (node, node_api))
        continue

      try:
        resp = ServerProxy(node_api).getPid('/NODEINFO')
      except:
        rospy.logerr("[cpu monitor] failed to get pid of node %s (api is %s)" % (node, node_api))
      else:
        try:
          pid = resp[2]
        except:
          rospy.logerr("[cpu monitor] failed to get pid for node %s from NODEINFO response: %s" % (node, resp))
        else:
          node_map[node] = Node(name=node, pid=pid)
          rospy.loginfo("[cpu monitor] adding new node %s" % node)
    
    time_me.acquire()
    usage_monitor.loc[time,'gazebo_cpu'] = 0
    usage_monitor.loc[time,'gazebo_mem'] = 0

    for node_name, node in list(node_map.items()):
      if node.alive():
        for r in robots:
          if '{}/supervisor'.format(r) in node.name:
            usage_monitor.loc[time,'{}_sup_cpu'.format(r)] = node.proc.cpu_percent() / psutil.cpu_count()
            usage_monitor.loc[time,'{}_sup_mem'.format(r)] = node.proc.memory_percent()
        if 'gazebo' in node.name:
          usage_monitor.loc[time,'gazebo_cpu'] += node.proc.cpu_percent() / psutil.cpu_count()
          usage_monitor.loc[time,'gazebo_mem'] += node.proc.memory_percent()
      else:
        rospy.logwarn("[cpu monitor] lost node %s" % node_name)
        del node_map[node_name]

    cpu_usage = psutil.cpu_percent()
    vm = psutil.virtual_memory()

    usage_monitor.loc[time,'total_cpu'] = cpu_usage
    usage_monitor.loc[time,'total_mem'] = vm.percent
    usage_monitor.to_csv('usage_monitor.csv')

    time_me.release()
    rospy.sleep(poll_period)
