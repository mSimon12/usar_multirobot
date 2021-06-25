
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from numpy.core.numeric import NaN
import pandas as pd 
import sys
import os
import ast

import numpy as np

try:
    filename = sys.argv[1]
except:
    # filename = 'samples/May-17-2021  22:29:22.csv'
    pass

df = pd.read_csv(filename)

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

print(df.head())
   
#    top=0.88,
# bottom=0.235,
# left=0.11,
# right=0.9,
# hspace=0.2,
# wspace=0.2

def put_ticks(base_col, plt):
    aux = df[df['event'].notnull()]
    df2 = aux
    for i in range(1,len(aux)+1):
        if ((i+1) < len(aux)) and (aux.iloc[i,:][base_col] == aux.iloc[i-1,:][base_col]):
            df2 = df2.drop(aux.index[i])

    plt.xticks(df2[df2['event'].notnull()].iloc[:,0], df2[df2['event'].notnull()]['event'].values, rotation ='vertical')


######################################################################################################
# Graph one - ALLOCATED ROBOTS
plt.figure()
# ax1 = plt.subplot(311)
plt.plot(df.iloc[:,0].values, df['allocated_robots'].values, 'b')
# plt.setp(ax1.get_xticklabels(), visible=False)
plt.xlabel('Time (s)')
plt.ylabel('Allocated Robots')
plt.title('Robots allocated to a task')

#Ticks
if x_axis_type != 'time':
    put_ticks('allocated_robots',plt)

plt.tight_layout()
plt.gcf().set_size_inches(18.5,10.5)

if action == 'save':
    plt.savefig(output_dir + '/robots_allocation.png')

# ######################################################################################################
# # Graph two - AVAILABLE ROBOTS
plt.figure()
# ax2 = plt.subplot(312)
plt.plot(df.iloc[:,0].values, df['available_robots'].values, 'r')
# plt.setp(ax2.get_xticklabels(), visible=False)
plt.xlabel('Time (s)')
plt.ylabel('Available Robots')
plt.title('Robots available to executa a task')

#Ticks
if x_axis_type != 'time':
    put_ticks('available_robots',plt)

plt.tight_layout()
plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/available_robots.png')

# ######################################################################################################
# Graph three - TELEOPERATIONS
plt.figure()
# plt.subplot(313)
plt.plot(df.iloc[:,0].values, df['teleoperations'].values, 'yellow')
plt.xlabel('Time (s)')
plt.ylabel('Number of\nteleoperations\nexecuted')
plt.title('Robots available to execute a task')

#Ticks
if x_axis_type != 'time':
    put_ticks('teleoperations',plt)

plt.tight_layout()
plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/teleoperations.png')

# ######################################################################################################
# # Graph four & five - CURRENT MANEUVERS

#PIONEERS
plt.figure()
x=0
for r_i in df.columns:
    if ('pioneer' in r_i) and ('cur_maneuver' in r_i):
        x += 1
        ax = plt.subplot(2,1,x)
        plt.plot(df.iloc[:,0].values, df[r_i].values)
        plt.xlabel('Time (s)')
        plt.ylabel('Current task')
        #Ticks
        if x_axis_type != 'time':
            put_ticks(r_i,plt)

        plt.legend([r_i.replace('_cur_maneuver','')])
plt.title('Maneuver executed by the robots along time')
        
plt.tight_layout()
plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/pioneers_current_maneuvers.png')

#UAVs
plt.figure()
x=0
for r_i in df.columns:
    if ('UAV' in r_i) and ('cur_maneuver' in r_i):
        x += 1
        ax = plt.subplot(2,1,x)
        plt.plot(df.iloc[:,0].values, df[r_i].values)
        plt.xlabel('Time (s)')
        plt.ylabel('Current task')
        #Ticks
        if x_axis_type != 'time':
            put_ticks(r_i,plt)

        plt.legend([r_i.replace('_cur_maneuver','')])
plt.title('Maneuver executed by the robots along time')    

plt.tight_layout()
plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/pioneers_current_maneuvers.png')

# ######################################################################################################
# Graph six - ROBOTS TASKS COUNTERS
plt.figure()
x=0
for r_i in df.columns:
    if 'tasks_counter' in r_i:
        x += 1
        ax = plt.subplot(2,2,x)
        plt.plot(df.iloc[:,0].values, df[r_i].values)
        plt.xlabel('Time (s)')
        plt.ylabel('Number of tasks')
        #Ticks
        if x_axis_type != 'time':
            put_ticks(r_i,plt)

        plt.legend([r_i.replace('_tasks_counter','')])
plt.title('Tasks finished by the robots')
        
plt.tight_layout()
plt.gcf().set_size_inches(18.5, 10.5)

# ######################################################################################################
# Graph seven - ROBOTS BATTERY LEVEL
plt.figure()
lines = ["-","--","-.",":"]
leg = []
for r_i in df.columns:
    if 'battery' in r_i:
        plt.plot(df.iloc[:,0].values, df[r_i].values, lines.pop())
        leg.append(r_i.replace('_battery',''))

plt.legend(leg)
plt.title('Robots battery level along time')
plt.xlabel('Time (s)')
plt.ylabel('Battery level (%)')

plt.tight_layout()
plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/battery_level.png')


# ######################################################################################################
# Graph eight - ROBOTS MOTIONS
# fig = plt.figure()

x = 0
for r_i in df.columns:
    if 'pose' in r_i:
        x += 1
        # ax = fig.add_subplot(2,2,x, projection = '3d')
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1, projection = '3d')
        positions = list(map(ast.literal_eval,df[df[r_i] != '[]'][r_i].values))
        X = []
        Y = []
        Z = []
        for row in positions:
            X.append(row[0])
            Y.append(row[1])
            Z.append(row[2])
        ax.plot3D(X,Y,Z)
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_xlim3d(0, 75)
        ax.set_ylim3d(0, 75)
        ax.set_zlim3d(0, 30)
        # plt.legend([r_i.replace('_pose','')])

        # plt.title('Robots trajectory')

        plt.title(r_i.replace('_pose',' trajectory'))
        plt.tight_layout()
        plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/battery_level.png')


#############################
# SHOW GRAPHS
if action == 'show':
    plt.show()
    