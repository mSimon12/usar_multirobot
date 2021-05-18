
import matplotlib.pyplot as plt
import pandas as pd 
import sys
import os

import numpy as np

try:
    filename = sys.argv[1]
except:
    # filename = 'samples/May-17-2021  22:29:22.csv'
    pass

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

df = pd.read_csv(filename)

print(df.head())

# Graph one
ax1 = plt.subplot(311)
plt.plot(df.iloc[:,0].values, df['allocated_robots'].values, 'b')
plt.setp(ax1.get_xticklabels(), visible=False)
# plt.xlabel('Time (s)')
plt.ylabel('Allocated Robots')
# plt.title('Robots allocated to a task')

# Graph two
ax2 = plt.subplot(312)
plt.plot(df.iloc[:,0].values, df['available_robots'].values, 'r')
plt.setp(ax2.get_xticklabels(), visible=False)
# plt.xlabel('Time (s)')
plt.ylabel('Available Robots')
# plt.title('Robots available to executa a task')

# Graph two
plt.subplot(313)
plt.plot(df.iloc[:,0].values, df['teleoperations'].values, 'yellow')
plt.xlabel('Time (s)')
plt.ylabel('Number of\nteleoperations\nexecuted')
# plt.title('Robots available to execute a task')

plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/general_info.png')

# Graphs of robots countings
plt.figure()
# Robots current maneuver

df2 = df.iloc[:, 4:]

leg = []
for r_i in df2.columns:
    if 'cur_maneuver' in r_i:
        plt.plot(df.iloc[:,0].values, df[r_i].values)
        leg.append(r_i.replace('_cur_maneuver',''))

plt.legend(leg)
plt.title('Maneuver executed by the robots along time')
plt.xlabel('Time (s)')
plt.ylabel('Current task')

plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/current_maneuvers.png')

plt.figure()
# Robots tasks counter

df2 = df.iloc[:, 4:]

leg = []
for r_i in df2.columns:
    if 'tasks_counter' in r_i:
        plt.plot(df.iloc[:,0].values, df[r_i].values)
        leg.append(r_i.replace('_tasks_counter',''))

plt.legend(leg)
plt.title('Tasks finished by the robot')
plt.xlabel('Time (s)')
plt.ylabel('Number of tasks')

plt.gcf().set_size_inches(18.5, 10.5)

if action == 'save':
    plt.savefig(output_dir + '/tasks_counters.png')
elif action == 'show':
    plt.show()
    