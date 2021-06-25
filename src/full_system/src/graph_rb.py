
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from numpy.core.numeric import NaN
from numpy.lib.function_base import rot90
import pandas as pd 
import sys
import os
import ast

import copy as cp
import numpy as np
from pandas.core import series


# filename = 'Jun-20-2021  19:13:01/__Jun-20-2021  19:13:01'
filename = 'Jun-20-2021  20:09:54/__Jun-20-2021  20:09:54'

df = pd.read_csv(filename + '.csv')
df_events = pd.read_csv(filename + '-events.csv')
df_missions = pd.read_csv(filename + '-missions.csv')

try:
    action = sys.argv[2]
except:
    action = 'show'

if action == 'save':
    output_dir = filename.replace('.csv','')
    try:
        os.stat(output_dir)
    except:
        os.mkdir(output_dir)

try:
    x_axis_type = sys.argv[3]
except:
    x_axis_type = 'time'

if x_axis_type not in ['events','time']:
    print('Wrong argument for x axis. Assuming time')
    x_axis_type = 'time'

# print(df.head())
# print(df_events.head())
# print(df_missions.head())

#####################################################################################
MAX_TIME = 2300
robots = ['pioneer3at_1', 'pioneer3at_2', 'UAV_1', 'UAV_2']
bat_low = {'pioneer3at_1': [(1628.86,24.66)], 'pioneer3at_2': [(1600.14,24.19)], 'UAV_1': [(2252.93,24.32)], 'UAV_2': [(1698.99,24.96)]}
fail = {'pioneer3at_1': [], 'pioneer3at_2': [461.18], 'UAV_1': [1426.93,2083.82], 'UAV_2': []}
victim = {'pioneer3at_1': [1518.94], 'pioneer3at_2': [1255.51], 'UAV_1': [806.29], 'UAV_2': []}

## List of events by robot
events = {}
events['pioneer3at_1']  = pd.Series(index = [1518.94,1628.86], data = ['v_found','bat_low'])
events['pioneer3at_2']  = pd.Series(index = [461.18,1255.51,1600.14], data = ['fail','v_found','bat_low'])
events['UAV_1']         = pd.Series(index = [806.29,1426.93,2083.82,2252.93], data = ['uav_v_found','uav_fail', 'uav_fail','uav_bat_low'])
events['UAV_2']         = pd.Series(index = [1698.99], data = ['uav_bat_low'])


for r in robots:
    fig = plt.figure(constrained_layout=True, figsize=(18,10))
    fig.suptitle(r, fontsize="x-large")
    gs = fig.add_gridspec(3, 2)
    ax1 = fig.add_subplot(gs[0,0])
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.set_xlim(0, MAX_TIME)
    # ax1.set_title('Current maneuver')

    ax2 = fig.add_subplot(gs[1,0])
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.set_xlim(0, MAX_TIME)
    # ax2.set_title('Battery level (%)')
    
    ax3 = fig.add_subplot(gs[2,0])
    ax3.spines['right'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3.spines['left'].set_visible(False)
    ax3.set_ylim(-1, 4)
    ax3.set_xlim(0, MAX_TIME)
    # ax2.set_title('events (%)')
    
    ax4 = fig.add_subplot(gs[:, 1], projection = '3d')
    ax4.set_title('Robot trajectory')

    #####-- CURRENT MANEUVER GRAPH --###############################################################################
    ax1.plot(df.iloc[:,0].values, df['{}_cur_maneuver'.format(r)].values, 'k', label='_nolegend_')
    # ax1.tick_params(axis='x', rotation=90)
    ax1.set_xticks([])
    ax1.set_yticks(['None','teleoperation',
                    'return to base',
                    'surroundings verification',
                    'safe land',
                    'approach',
                    'exploration',
                    'assessment',
                    'victim search'])
    
    for e in events[r].index:
        ax1.axvline(e, color ='r', lw = 1.5, ls='-.', alpha = 0.75)
    
    ax1.set_ylabel('Current maneuver', rotation='vertical')
    # ax1.legend(loc = 'best')

    #####-- BATTERY LEVEL GRAPH --##################################################################################
    ax2.plot(df.iloc[:,0].values, df['{}_battery'.format(r)].values, 'b', label='_nolegend_')
    # ax2.tick_params(axis='x', rotation=90)
    # ax2.set_xticks(range(0,2400,100))
    ax2.set_xticks([])
    ax2.set_yticks(range(0,110,10))

    # ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Battery Level (%)', rotation='vertical')

    #Scatter points
    x = [b[0] for b in bat_low[r]]
    y = [b[1] for b in bat_low[r]]
    ax2.scatter(x, y, marker='o', color='r', zorder=10)

    for e in events[r].index:
        ax2.axvline(e, color ='r', lw = 1.5, ls='-.', alpha = 0.75)

    #####-- EVENTS TIMELINE GRAPH --################################################################################
    levels = np.tile([3.5, 4], int(np.ceil(len(events[r])/2)))[:len(events[r])]

    # Create figure and plot a stem plot with the date
    ax3.vlines(events[r].index, 0, levels, color="tab:red")  # The vertical stems.
    ax3.plot(events[r].index, np.zeros_like(events[r].index), "-o", color="k", markerfacecolor="w")  # Baseline and markers on it.

    # annotate lines
    for d, l, e in zip(events[r].index, levels, events[r].values):
        ax3.annotate(e, xy=(d, l),
                    xytext=(-3, np.sign(l)*3), rotation=90, textcoords="offset points",
                    horizontalalignment="right",
                    verticalalignment="top")

    ax3.tick_params(axis='x', rotation=90)
    ax3.set_xticks(range(0,MAX_TIME+100,100))
    ax3.set_yticks([])
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Event', rotation='vertical')


    #####-- ROBOTS TRAJECTORIES GRAPH --########################################################################### 
    graphs = {'normal': 'k', 'vsv': 'b', 'rb': 'r'}
    t = {'x':[], 'y':[], 'z':[]}
    m_trajectories = {'normal': [], 'vsv': [], 'rb': []}

    last_pose = None
    last_m_type = None
    for i in df[(df['{}_pose'.format(r)] != '[]')].index:
        pose = ast.literal_eval(df.loc[i, '{}_pose'.format(r)])
        if not df.loc[i,'{}_cur_maneuver'.format(r)] in ['surroundings verification', 'return to base']:
            m_type = 'normal'
        elif df.loc[i,'{}_cur_maneuver'.format(r)] == 'surroundings verification':
            m_type = 'vsv'
        elif df.loc[i,'{}_cur_maneuver'.format(r)] == 'return to base':
            m_type = 'rb'
        
        if (m_type != last_m_type) and (m_type != None):
            m_trajectories[m_type].append(cp.deepcopy(t))
            if last_pose:
                m_trajectories[m_type][len(m_trajectories[m_type])-1]['x'].append(last_pose[0])
                m_trajectories[m_type][len(m_trajectories[m_type])-1]['y'].append(last_pose[1])
                m_trajectories[m_type][len(m_trajectories[m_type])-1]['z'].append(last_pose[2])
        m_trajectories[m_type][len(m_trajectories[m_type])-1]['x'].append(pose[0])
        m_trajectories[m_type][len(m_trajectories[m_type])-1]['y'].append(pose[1])
        m_trajectories[m_type][len(m_trajectories[m_type])-1]['z'].append(pose[2])
        
        last_pose = pose
        last_m_type = m_type
             
    #Plot maneuvers trajectory
    for m in m_trajectories:
        for t in m_trajectories[m]:
            ax4.plot3D(t['x'], t['y'], t['z'], graphs[m])
    
    ax4.set_xlabel('X (m)')
    ax4.set_ylabel('Y (m)')
    ax4.set_zlabel('Z (m)')
    # ax4.set_xlim3d(0, 75)
    # ax4.set_ylim3d(0, 40)
    ax4.set_zlim3d(0, 15)

    # Save the figure
    if action == 'save':
        plt.savefig(output_dir + '/{}.png'.format(r))



#############################
# SHOW GRAPHS
if action == 'show':
    plt.show()
    