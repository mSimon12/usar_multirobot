# USAR_multirrobot
This is an implementation of a high-level behavior supervisor for coordination of multi-robots working on USAR (Urban Search and Rescue) applications.

It wa implemented with ROS melodic and Gazebo 9.0.

As the system implements a broad set of packages, we suggest you to first install all required dependecies by the following code:
```
rosdep install --from-paths src --ignore-src -r -y
```

After that, run ``` catkin_make``` to build all the packages on the 'usar_multirobot' folder:

If all packages have been build with no errors, you can now run the world with multiple robots doing:
```
source devel/setup.bash
roslaunch full_system system.launch
```

By this command you may start:
 - Simulation of a world with Gazebo;
 - Rviz with the main components of robots;
 - A Supervisory Control interface to monitor the robots models and simulate controllable and uncontrollable events.



To send a pioneer3at to a position, in a new terminal use:

```
rostopic pub -1 /robot/manouvers/in system_msgs/events_message 
"event: 'start_approach'
info: ''
param:
- 0
position:
- x: 10.0
  y: 10.0
  theta: 0.0" 
```
Where:
'robot' can be:  pioneer3at_1, pioneer3at_2 ...
'x', 'y' and 'theta' represent the desired position and orientation for the pioneer3at



To send a drone to a position, in a new terminal use:

```
rostopic pub -1 /drone/manouvers/in system_msgs/drone_events_message 
"event: 'start_approach'
info: ''
param:
- 0
position:
- linear:
    x: 0.0
    y: 0.0
    z: 0.0
  angular:
    x: 0.0
    y: 0.0
    z: 0.0"
```
Where:
'drone' can be:  UAV_1, UAV_2 ...
'linear.x', 'linear.y', 'linear.z' and 'angular.z' represent the desired position and orientation for the UAV.


To remove a victim:
```
source devel/setup.bash
rosrun human_teams rescue_victim.py victim_name
```
'victim_name' can be: victim1 (woman), victim2 (man), victim3 (girl) or victim4 (boy)
