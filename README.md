# USAR_multirrobot
This is the implementation of a high-level behavior supervisor for coordination of multirrobots in USAR (Urban Search and Rescue) applications.

First install all dependecies required for this project:
```
rosdep install --from-paths src --ignore-src -r -y
```


To use it you will need to build all the packages on the 'usar_multirobot' folder:
```
catkin_make
```


To run the world with multiple robots:
```
source devel/setup.bash
roslaunch full_system system.launch
```


To control the a pioneer3at position, in a new terminal:
```
source devel/setup.bash
rosrun pioneer3at_controllers pioneer3at_system.py robot_name x y rot
```
'robot_name' can be:  pioneer3at_1, pioneer3at_2 ...

'x', 'y' and 'rot' represent the desired position and orientation for the pioneer3at


To control the a drone position, in a new terminal:
```
source devel/setup.bash
rosrun quadrotor_controllers drone_system.py drone_name x y z rot
```
'drone_name' can be:  UAV_1, UAV_2 ...

'x', 'y', 'z' and 'rot' represent the desired position and orientation for the drone


To remove a victim:
```
source devel/setup.bash
rosrun human_teams rescue_victim.py victim_name
```
'victim_name' can be: victim1 (woman), victim2 (man), victim3 (girl) or victim4 (boy)
