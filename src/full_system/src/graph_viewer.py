
import matplotlib.pyplot as plt
from numpy.core.numeric import NaN
import pandas as pd 
import sys
import os

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

print(df.head())
   
#    top=0.88,
# bottom=0.235,
# left=0.11,
# right=0.9,
# hspace=0.2,
# wspace=0.2

######################################################################################################
# Graph one
plt.figure()
# ax1 = plt.subplot(311)
plt.plot(df.index, df['allocated_robots'].values, 'b')
# plt.setp(ax1.get_xticklabels(), visible=False)
plt.xlabel('Time (s)')
plt.xticks(df[df['event'].notnull()].index, df[df['event'].notnull()]['event'].values, rotation ='vertical')
plt.ylabel('Allocated Robots')
plt.tight_layout()
plt.title('Robots allocated to a task')

plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/robots_allocation.png')

######################################################################################################
# Graph two
plt.figure()
# ax2 = plt.subplot(312)
plt.plot(df.index, df['available_robots'].values, 'r')
# plt.setp(ax2.get_xticklabels(), visible=False)
plt.xlabel('Time (s)')
plt.xticks(df[df['event'].notnull()].index, df[df['event'].notnull()]['event'].values, rotation ='vertical')
plt.ylabel('Available Robots')
plt.tight_layout()
plt.title('Robots available to executa a task')

plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/available_robots.png')

######################################################################################################
# Graph three
plt.figure()
# plt.subplot(313)
plt.plot(df.index, df['teleoperations'].values, 'yellow')
plt.xticks(df[df['event'].notnull()].index, df[df['event'].notnull()]['event'].values, rotation ='vertical')
plt.xlabel('Time (s)')
plt.ylabel('Number of\nteleoperations\nexecuted')
plt.tight_layout()
plt.title('Robots available to execute a task')

plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/teleoperations.png')

######################################################################################################
# Graphs of current maneuver
plt.figure()
x=0
for r_i in df.columns:
    if 'cur_maneuver' in r_i:
        x += 1
        ax = plt.subplot(4,1,x)
        # plt.plot(df[df.iloc[:,x_axis_index].notnull()].iloc[:,x_axis_index].index, df[df.iloc[:,x_axis_index].notnull()][r_i].values)
        plt.plot(df.iloc[:,0].index, df[r_i].values)
        if x < 4:
            plt.setp(ax.get_xticklabels(), visible=False)
        else:
            plt.xlabel('Time (s)')
        # leg.append(r_i.replace('_cur_maneuver',''))

        plt.legend([r_i.replace('_cur_maneuver','')])
        plt.title('Maneuver executed by the robots along time')
        plt.xticks(df[df['event'].notnull()].index, df[df['event'].notnull()]['event'].values, rotation ='vertical')
        plt.ylabel('Current task')

plt.tight_layout()
plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/current_maneuvers.png')

######################################################################################################
#Graphs of robots tasks counters
plt.figure()
leg = []
for r_i in df.columns:
    if 'tasks_counter' in r_i:
        plt.plot(df.index, df[r_i].values)
        leg.append(r_i.replace('_tasks_counter',''))

plt.legend(leg)
plt.title('Tasks finished by the robot')
plt.xticks(df[df['event'].notnull()].index, df[df['event'].notnull()]['event'].values, rotation ='vertical')
plt.xlabel('Time (s)')
plt.ylabel('Number of tasks')

plt.tight_layout()
plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/tasks_counters.png')
elif action == 'show':
    plt.show()
    