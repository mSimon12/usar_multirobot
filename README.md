# USAR_multirrobot
This is the implementation of a high-level behavior supervisor for coordination of multirrobots in USAR (Urban Search and Rescue) applications.

To run the world with multiple robots:
```
source devel/setup.bash
roslaunch usar_gazebo post-disaster.launch
```
or
```
roslaunch usar_gazebo post-disaster.launch
```


To control the a robot position:
```
source devel/setup.bash
rosrun controllers client.py robot_name x y rot
```
'robot_name' pode ser: pioneer2dx_1, pioneer2dx_2, pioneer3at_1, pioneer3at_2

x, y e rot representam a localização desejada e orientação final


To remove a victim:
```
source devel/setup.bash
rosrun mypack_pkg rescue_victim.py victim_name
```
'victim_name' pode ser: victim1 (woman), victim2 (man), victim3 (girl) or victim4 (boy)
